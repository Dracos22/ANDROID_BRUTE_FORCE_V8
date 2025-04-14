# ANDROID_BRUTE_FORCE_V8
🔐 Android ADB PIN Brute Forcer – Versión V5 (GUI + CLI)

Android_bruteforceV5.py es una herramienta de fuerza bruta desarrollada en Python con PyQt5, diseñada para probar PINs en dispositivos Android conectados mediante ADB (Android Debug Bridge).
Está dirigida a pentesters, investigadores en ciberseguridad y analistas forenses móviles que necesiten validar la seguridad de bloqueos por PIN en entornos controlados y con autorización.


🎯 Características principales
✅ Interfaz Gráfica Moderna con modo claro y oscuro

📱 Visualización en tiempo real del dispositivo usando scrcpy

🔁 Soporte completo para ataque por fuerza bruta a bloqueos PIN (4, 6, u 8 dígitos)

📊 Barra de progreso con porcentaje central y registros en vivo

📦 Compatible con modo CLI (consola/shell) para automatización o scripting

🔍 Muestra información del dispositivo conectado: modelo, número de serie, versión de Android

🔧 Ajustes de espera (anti-lockout) entre intentos

☑️ Comprobación de dependencias al iniciar (ADB, scrcpy, etc.)

# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar ADB y scrcpy
sudo apt install adb scrcpy -y

# Instalar Python y pip si no están
sudo apt install python3 python3-pip -y

# Instalar PyQt5
pip3 install PyQt5
