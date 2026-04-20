# Ceres

Sistema para monitoreo y control de cultivo hidroponico con interfaz grafica, lectura de sensores, control de actuadores y API Flask para consulta de datos.

## Tabla de contenido

- [Descripcion general](#descripcion-general)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalacion](#instalacion)
- [Configuracion](#configuracion)
- [Ejecucion](#ejecucion)
- [API disponible](#api-disponible)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Problemas comunes](#problemas-comunes)

## Descripcion general

Ceres integra 4 capas principales:

1. Interfaz de escritorio con CustomTkinter para visualizacion y configuracion.
2. Capa de datos con MySQL para plantas, parametros, mediciones y alertas.
3. Automatizacion de hardware en Raspberry Pi (GPIO) y lectura serial de Arduino.
4. API Flask para exponer datos a clientes externos.

## Arquitectura del proyecto

### Entradas principales

- `main.py`: inicia la aplicacion GUI.
- `mail.py`: API Flask principal con endpoints de datos en `:5000`.
- `app.py`: API Flask minima de prueba en `:8080`.
- `hardware_manager.py`: ejecuta hilos de lectura de sensores y control automatico.

### Componentes clave

- `gui/`: interfaz, navegacion y vistas (`home`, `sensores`, `actuadores`, `plantas`, `configuracion`).
- `models/`: acceso a base de datos y reglas CRUD.
- `controllers/`: control de actuadores via GPIO.
- `utils/arduino.py`: lectura de datos por puerto serial.
- `utils/raspberry.py`: logica de automatizacion para bomba, pH y solucion.
- `utils/config.json`: configuracion operativa (planta, sensores, actuadores, email, password).

## Requisitos

## Software

- Python 3.10+ (recomendado 3.11).
- MySQL/MariaDB en ejecucion.
- Linux con Raspberry Pi para funciones GPIO reales.
- Arduino conectado por serial (en Linux normalmente `/dev/ttyUSB0`) para lectura de sensores.

## Librerias Python usadas en el codigo

El archivo `requirements.txt` actual solo contiene `flask`, pero en el codigo se usan ademas:

- flask
- flask-cors
- mysql-connector-python
- customtkinter
- pillow
- matplotlib
- pyserial
- RPi.GPIO (solo Raspberry Pi)

## Instalacion

1. Clona el repositorio y entra al directorio:

```bash
git clone <url-del-repo>
cd Ceres
```

2. Crea y activa entorno virtual.

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
pip install flask-cors mysql-connector-python customtkinter pillow matplotlib pyserial
```

Nota: `RPi.GPIO` debe instalarse en Raspberry Pi con un sistema compatible.

## Configuracion

## 1) Base de datos MySQL

Este proyecto espera una base de datos llamada `Ceres`.

Credenciales en codigo:

- `config/Database.py`: host `localhost`, puerto `3306`, user `root`, password `2675`, database `Ceres`.
- `mail.py`: host `localhost`, user `root`, password `pi2090`, database `Ceres`.

Se recomienda unificar y mover estas credenciales a variables de entorno.

Tablas usadas en el codigo:

- `plantas`
- `parametros`
- `mediciones`
- `alertas`
- `actuadores`

## 2) Configuracion de aplicacion

Edita `utils/config.json` para ajustar:

- Planta activa (`planta.id`, fechas y litros).
- Intervalo de lectura de sensores (`sensores.tiempo_lectura`, en segundos).
- Pines GPIO y tiempos de actuadores (`actuadores`).
- Email de notificacion.
- Password para cambios de configuracion en la GUI.

## 3) Hardware

- GPIO: el codigo usa `controllers/Controller.py` con `RPi.GPIO`.
- Arduino: lectura serial definida en `utils/arduino.py` (puerto por defecto `/dev/ttyUSB0`).

## Ejecucion

## Opcion A: Interfaz grafica (escritorio)

```bash
python main.py
```

## Opcion B: API Flask principal

```bash
python mail.py
```

Servidor por defecto: `0.0.0.0:5000`.

## Opcion C: API minima de prueba

```bash
python app.py
```

Servidor por defecto: `0.0.0.0:8080`.

## Opcion D: Automatizacion de hardware

```bash
python hardware_manager.py
```

Inicia hilos para:

- Lectura Arduino.
- Bomba automatica.
- Dosificacion de solucion.
- Ajuste de pH/pH-.

## Script auxiliar Linux

Existe `start_flask.sh` con ruta fija al entorno virtual en `/home/jademajesty/Ceres/...`.
Si tu ruta es distinta, actualizala antes de usarlo.

## API disponible

Endpoints expuestos por `mail.py`:

- `GET /api/planta`: lista plantas.
- `POST /api/planta`: crea planta con `nombre` y `valor`.
- `GET /api/parametros`: lista parametros.
- `GET /api/mediciones`: lista mediciones.
- `GET /api/alertas`: lista alertas no resueltas (`resuelta = 0`).

Endpoints expuestos por `app.py` (prueba):

- `GET /`: estado basico de API.
- `POST /datos`: recibe payload JSON y devuelve eco.

## Estructura del repositorio

```text
Ceres/
|- main.py
|- mail.py
|- app.py
|- hardware_manager.py
|- plant_manager.py
|- requirements.txt
|- start_flask.sh
|- config/
|- controllers/
|- gui/
|  |- app.py
|  |- views/
|- models/
|- utils/
|  |- config.json
|  |- arduino.py
|  |- raspberry.py
```

