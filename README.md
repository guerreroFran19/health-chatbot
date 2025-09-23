# 🤖 Chatbot de Asistencia en Salud

Este proyecto es un **asistente virtual de salud**, desarrollado en **Python** como parte de un trabajo universitario. El chatbot permite interactuar con el usuario mediante voz y texto, ofreciendo funciones útiles para el cuidado personal y la organización de la salud.

---

## 🚀 Funcionalidades Principales

* **Recordatorio de turnos médicos**: Integración con Google Calendar para no olvidar tus citas.
* **Recordatorio de medicación**: Te avisa cuándo es el momento de tomar tus medicamentos.
* **Consultas en Wikipedia**: Obtén información básica y rápida sobre medicamentos de venta libre.
* **Conversación hablada**: Interactúa con el asistente de forma natural, ya que puede escuchar y responder con voz.

### Funciones Adicionales

* **Contar chistes**: Para un momento de distracción y buen humor (usando `pyjokes`).
* **Reproducir música en YouTube**: Pon tu música favorita directamente desde el asistente (con `pywhatkit`).
* **Consultar datos financieros**: Accede a información financiera básica (con `yfinance`).
* **Abrir sitios web**: Navega por la web sin salir del asistente.
* **Decir fecha y hora actual**: Mantente al tanto de la información temporal.

---

## 🛠️ Tecnologías y Librerías Utilizadas

* [pyttsx3](https://pypi.org/project/pyttsx3/): Para la síntesis de voz (Texto a Voz - TTS).
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/): Para el reconocimiento de voz (Voz a Texto - STT).
* [pywhatkit](https://pypi.org/project/pywhatkit/): Para reproducir música en YouTube y otras utilidades.
* [yfinance](https://pypi.org/project/yfinance/): Para obtener datos financieros.
* [pyjokes](https://pypi.org/project/pyjokes/): Para generar chistes.
* [wikipedia](https://pypi.org/project/wikipedia/): Para realizar consultas en Wikipedia.
* [webbrowser](https://docs.python.org/3/library/webbrowser.html): Para abrir páginas web en el navegador.
* [datetime](https://docs.python.org/3/library/datetime.html): Para manejar fechas y horas.

---

## 📦 Instalación

Sigue estos pasos para poner en marcha el asistente:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/guerreroFran19/health-chatbot.git](https://github.com/guerreroFran19/health-chatbot.git)
    cd health-chatbot
    ```

2.  **Crear y activar un entorno virtual (recomendado):**
    * En Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    * En Linux/macOS:
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```

3.  **Instalar las dependencias:**
    Asegúrate de tener el archivo `requirements.txt` en la raíz del proyecto.
    ```bash
    pip install -r requirements.txt
    
    ```
    3.1 **Instalar las dependencias de la API google calendar:**
    ```bash
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib    
    ```
---

### Ejecución
sigue estos pasos para inicar la app
1. **Ejectura el archivo main.py**
    ```bash
      main.py
    ```
2. **Levanta la DB en un entorno virtual activado**
    ```bash
      docker-compose up -d
    ```
---
3. **Ejecutar este comando en un entorno virtual activado**
    ```bash
      uvicorn app:app --reload
    ```

## 🏗️ Arquitectura por capas
La arquitectura del proyecto está organizada en capas para mantener el código modular, mantenible y escalable.
```bash
project/
│── main.py                # Punto de entrada principal de la aplicación.
│── requirements.txt       # Lista de dependencias del proyecto.
│
├── core/                  # Contiene la lógica central y las abstracciones.
│   ├── speech/            # Módulos para el manejo de STT (Speech-to-Text) y TTS (Text-to-Speech).
│   ├── nlp/               # Lógica para el Procesamiento del Lenguaje Natural y la interpretación de comandos.
│   └── utils/             # Funciones de utilidad genéricas (ej: logging, configuración, manejo de errores).
│
├── services/              # Capa responsable de interactuar con servicios externos.
│   ├── wikipedia_service.py # Servicio para realizar consultas en Wikipedia.
│   ├── jokes_service.py     # Servicio para obtener chistes.
│   ├── finance_service.py   # Servicio para consultar datos financieros.
│   ├── browser_service.py   # Servicio para interactuar con el navegador web.
│   └── calendar_service.py  # Servicio para la integración con Google Calendar (requiere API externa).
│
└── controllers/           # Orquesta el flujo principal del asistente.
    └── assistant_controller.py # Maneja la lógica de alto nivel, coordinando el uso de core y serv
   ```
## Endpoints 
1. **Autenticación** 
    ```bash
   Loguearse 
   POST /auth/login
   
   body requerido 
   {
      "email": "emailTest@email",
      "password": "123456"
    }
   
   ```
   ```bash
   Registrarse
    POST /register
   
   body requerido 
   {
      "name":"test",
      "email": "emailTest@email",
      "password": "123456"
    }
   
   ```
2. **Medicamentos**
    ```bash
   crear medicamentos 
   
   POST /medications/
   ```
   ```bash
   headers requeridos
   
   Authorization: Bearer tu_token_jwt_aqui
    Content-Type: application/json
   ```
   ```bash
   body requerido 
   {
      "name": "Paracetamol",
      "dosage": "500mg",
      "frequency_hours": 8,
      "instructions": "Tomar después de comer"
    }
   
   body opcional 
   
   {
      "name": "Ibuprofeno",
      "dosage": "400mg", 
      "frequency_hours": 12,
      "end_date": "2024-12-31T23:59:59",
      "instructions": "Tomar con alimentos"
    }
   ```
   ```bash
   Listar medicamentos
   GET /medications/
   ```
   ```bash
   Headers requeridos:
    Authorization: Bearer tu_token_jwt_aqui
   ```

   