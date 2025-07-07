# 🚗 TigMotors - Sistema de Gestión de Trabajos

Bienvenido al sistema de gestión de trabajos de **TigMotors**, una aplicación de escritorio desarrollada en Python con PyQt5 y Firebase para administrar clientes, trabajos, fechas, precios y más.

---

## 📦 Requisitos del sistema

- Python 3.10 o superior  
- Git  
- Sistema operativo: Windows (para .exe) o multiplataforma (para ejecutar desde código)

---

## 📁 Clonar el repositorio

```bash
git clone https://github.com/Washitox/TigMotors-Python.git
cd TigMotors-Python
```

---

## 🔧 Instalación de dependencias

Instala los paquetes necesarios con pip:

```bash
pip install -r requirements.txt
```

Si no tienes `PyQt5`:

```bash
pip install pyqt5
```

---

## 🔥 Configuración de Firebase

El sistema utiliza Firebase Firestore como base de datos. Sigue estos pasos para configurarlo:

### 1. Crear proyecto en Firebase

- Ve a [https://console.firebase.google.com](https://console.firebase.google.com)
- Crea un nuevo proyecto llamado `TigMotors` (o cualquier nombre)

### 2. Habilitar Firestore

- Ve a **Build > Firestore Database**
- Haz clic en **Crear base de datos**
- Selecciona el modo de prueba o producción

### 3. Crear claves de acceso

- Ve a **Project Settings > Cuentas de servicio**
- Clic en **Generar nueva clave privada**
- Guarda el archivo como `firebase_key.json`

> ⚠️ **IMPORTANTE:** Este archivo no puede ser subido GitHub.

### 4. Agregar el archivo al proyecto

Coloca `firebase_key.json` en la raíz del proyecto, junto a `firebase_config.py`.

Estructura esperada:

```
TigMotors-Python/
├── gui/
├── assets/
├── firebase_config.py
├── firebase_key.json  ✅
├── main.py
└── requirements.txt
```

---

## ⚙️ Estructura general del proyecto

```
TigMotors-Python/
├── gui/                   # Interfaces gráficas PyQt5
├── assets/                # Imágenes como el logo
├── firebase_config.py     # Inicialización de Firebase
├── firebase_key.json      # 🔐 Tu clave privada (no se sube al repo)
├── main.py                # Punto de entrada
├── README.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

---

## ▶️ Ejecutar la aplicación

```bash
python main.py
```

---

## 🧪 Crear ejecutable (.exe) (opcional)

Si deseas generar el `.exe`, usa el siguiente comando:

```bash
pyinstaller --onefile --add-data "assets;assets" --add-data "firebase_key.json;." main.py
```

El archivo estará en `dist/TigMotors.exe`.

---

## 📥 Descargar instalador

> Puedes descargar directamente el instalador sin necesidad de clonar el repositorio:

📦 [**Descargar instalador TigMotors (.exe)**](https://www.mediafire.com/file/tw1elfa680hh5y3/TigMotorsSetup.exe/file)  


---

## 📌 Notas

- La clave de acceso al sistema es `134679`
- El logo de TigMotors está incrustado en el fondo de todas las ventanas
- Los trabajos pueden filtrarse por nombre, fechas y ID
- Los precios solo aceptan números (hasta 4 dígitos)
- El ejecutable puede ejecutarse sin necesidad de tener Python instalado

---

## 📫 Contacto

Desarrollado por **Washington Villares**  
Correo: [washovilla78@email.com](mailto:washovilla78@email.com)

---

## 🛡️ Licencia

Este proyecto es de uso académico y está creado en otro repositorio privado para el uso de la empresa **TigMotors**.
