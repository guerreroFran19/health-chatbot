# main.py
from fastapi import FastAPI
from routes import auth_routes, user_routes, medication_routes # Importar routers

app = FastAPI(
    title="Health Chatbot API",
    description="API para el chatbot de salud con Google Calendar integration",
    version="1.0.0"
)

# Incluir routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(medication_routes.router)

@app.get("/")
async def root():
    return {"message": "Health Chatbot API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)