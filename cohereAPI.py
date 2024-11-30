import cohere
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Cohere client with API key
API_KEY = os.getenv("COHERE_API")
co = cohere.Client(API_KEY)

# Generate to-dos from transcription
def generate_todos(transcription_text, lang):
    # Define the prompt based on the lang
    if lang == "AR":
        prompt = f"""خذ النص التالي المقتبس من اجتماع باللغة الدارجة المغربية، وحول الكلام إلى لائحة ديال المهام اللي خاص يتدار. 
اللائحة خاصها تكون مختصرة وكتبت بالدارجة المغربية، وكل مهمة تبدا بسطر جديد:

النص:
"{transcription_text}"

الجواب:"""
    elif lang == "EN":
        prompt = f"""Take the following text transcribed from a meeting in English and turn it into a to-do list. 
The list should be concise and written in clear English. Each task should start on a new line:

Text:
"{transcription_text}"

Response:
"""
    elif lang == "FR":
        prompt = f"""Prenez le texte suivant transcrit d'une réunion en français et transformez-le en une liste de tâches à accomplir. 
La liste doit être concise et écrite en français clair. Chaque tâche doit commencer sur une nouvelle ligne :

Texte :
"{transcription_text}"

Réponse :
"""
    else:
        raise ValueError("Unsupported language")
        exit()

    try:
        # Call Cohere's generate endpoint
        response = co.generate(
            model="command-r-plus-08-2024",
            prompt=prompt,
            max_tokens=400,
            temperature=0.7,
        )
        # Extract and return the generated to-do list
        todos = response.generations[0].text.strip()
        return todos
    except Exception as e:
        print("Error generating to-dos:", e)
        return None

# Function to summarize transcription
def summarize_text(transcription_text, lang):
    try:
        # Call Cohere's summarize endpoint
        response = co.summarize(
            text=transcription_text,
            length="medium",
            format="bullets",
            model="command-r-plus-08-2024",
            temperature=0.5,
        )
        # Return the generated summary
        return response.summary
    except Exception as e:
        print("Error using co.summarize:", e)
        return None

if __name__ == "__main__":
    file_path = "transcription.txt"
    try:
        with open(file_path, "r") as file:
            transcription = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()

    lang = "AR"  # Example language
    print("=== Generating To-Dos ===")
    todos = generate_todos(transcription, lang)
    if todos:
        print("To-Dos:")
        print(todos)
    else:
        print("Failed to generate To-Dos.")

    print("\n=== Generating Summary ===")
    summary = summarize_text(transcription, lang)
    if summary:
        print("Summary:")
        print(summary)
    else:
        print("Failed to generate Summary.")
