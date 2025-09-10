import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.pause_threshold = 2
        print("Ya puedes hablar...")
        audio = r.listen(origen)

        try:
            pedido = r.recognize_google(audio, language="es-ES")
            print(f"Dijiste: {pedido}")
            return pedido
        except sr.UnknownValueError:
            print("Ups, no entendí")
            return ""
        except sr.RequestError:
            print("Ups, no hay servicio")
            return ""
        except:
            print("Ups, algo ha salido mal")
            return ""
