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
```
sudo apt update && sudo apt upgrade -y
```

# Instalar ADB y scrcpy

```
sudo apt install adb scrcpy -y
```

# Instalar Python y pip si no están
```
sudo apt install python3 python3-pip -y
```

# Instalar PyQt5
```
pip3 install PyQt5
```

# CAPTURA
<p>
	Este programa incluye el modo >> python Android_bruteforceV8.py --gui un modo grafico.
</p>


<br>
<img  align="center" src="Captura de pantalla_2025-04-14_03-41-51.png" alt="">


# DEMO

```
 python Android_bruteforceV8.py --help 
```

```

  ▄▖   ▌    ▘ ▌  ▄     ▗     ▄▖        
  ▌▌▛▌▛▌▛▘▛▌▌▛▌▄▖▙▘▛▘▌▌▜▘█▌▄▖▙▖▛▌▛▘▛▘█▌
  ▛▌▌▌▙▌▌ ▙▌▌▙▌  ▙▘▌ ▙▌▐▖▙▖  ▌ ▙▌▌ ▙▖▙▖
        Android Brute Force Tool - V5

usage: Android_bruteforceV8.py [-h] [-i I] [-w W] [--pin4] [--pin6] [--pin8] [-V] [--sleep SLEEP] [--gui]

Android ADB PIN Brute Forcer

options:
  -h, --help     show this help message and exit
  -i I           ID del dispositivo ADB
  -w W           Ruta del archivo wordlist
  --pin4         PINs de 4 dígitos
  --pin6         PINs de 6 dígitos
  --pin8         PINs de 8 dígitos
  -V, --verbose  Verbose
  --sleep SLEEP  Tiempo de espera en milisegundos entre lotes
  --gui          Lanzar modo gráfico
```
