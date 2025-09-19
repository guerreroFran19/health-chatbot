from controllers.assistant_controller import start_assistant
from controllers import user_controller
from services import user_service

if __name__ == "__main__":
    # --- OPCIÓN 1: probar el asistente ---
    # start_assistant()

    # --- OPCIÓN 2: probar el controlador de usuarios ---
    result = user_controller.create_user_controller(
        name="Santi",
        email="santi@example.com",
        password="12345"
    )
    print("🎯 Resultado del controller:", result)

    # --- OPCIÓN 3: probar directo el servicio ---
    try:
        new_user = user_service.register_user(
            name="Ana",
            email="ana@example.com",
            password="abcd1234"
        )
        print("✅ Usuario creado:", new_user)
    except Exception as e:
        print("❌ Error:", e)
