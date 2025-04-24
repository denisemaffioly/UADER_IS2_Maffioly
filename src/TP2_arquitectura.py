import openai
import readline  # Librería que agregué para utilizar el cursor up

# Inserta la API Key 
openai.api_key = "sk-123456789abcdef"  # Agregar API

try: 
    # Primer nido para la aceptación de la consulta
    userquery = input("You: ")  # Consulta del cliente
    readline.add_history(userquery)  # Guarda la última consulta

    if not userquery:
        raise ValueError("La consulta no puede estar vacía.")  # Verifica que la consulta no esté vacía
    
    # Segundo nido para la invocación de la API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Chat GPT responde la pregunta del usuario"},
                {"role": "user", "content": userquery}
            ]
        )
        print("chatGPT:", response['choices'][0]['message']['content'])  # Muestra la respuesta de la API
    except openai.error.OpenAIError as e:
        print(f"Error al llamar a la API: {e}")  # Muestra un error específico si hay un problema con la API

except ValueError as e:
    print(f"Error al procesar la consulta: {e}")  # Muestra un error si la consulta es vacía o tiene problemas
except Exception as e:  # Nido general para capturar cualquier otro error
    print(f"Error al ejecutar el programa: {e}")
