import threading

import uvicorn
from fastapi import FastAPI

from controllers.assistant_controller import start_assistant
from routes import auth_routes, medication_routes

app = FastAPI()

# Incluir routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(medication_routes.router, prefix="/medications", tags=["medications"])

@app.get("/")
def read_root():
    return {"message": "Health Chatbot API está funcionando"}

def run_assistant():
    start_assistant()

if __name__ == "__main__":
    # Hilo para el chatbot
    t = threading.Thread(target=run_assistant, daemon=True)
    t.start()

    # Levantar FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)