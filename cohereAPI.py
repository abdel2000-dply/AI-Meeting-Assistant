import cohere
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Cohere client with API key
API_KEY = os.getenv('COHERE_API')
co = cohere.Client(API_KEY)

# Generate Dareja to-dos from Dareja transcription
def generate_dareja_todos(transcription_text):
    # Define the prompt in Moroccan Dareja
    prompt = f"""خذ النص التالي المقتبس من اجتماع باللغة الدارجة المغربية، وحول الكلام إلى لائحة ديال المهام اللي خاص يتدار. 
اللائحة خاصها تكون مختصرة وكتبت بالدارجة المغربية، وكل مهمة تبدا بسطر جديد:

النص:
"{transcription_text}"

الجواب:"""
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

# Function to summarize a Moroccan Darija transcription
def summarize_darija(transcription_text):
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
    file_path = "transcription.txt"  # Replace with your file name
    try:
        with open(file_path, "r") as file:
            darija_transcription = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()

    print("=== Generating To-Dos ===")
    todos = generate_dareja_todos(darija_transcription)
    if todos:
        print("To-Dos in Darija:")
        print(todos)
    else:
        print("Failed to generate To-Dos.")

    print("\n=== Generating Summary ===")
    summary = summarize_darija(darija_transcription)
    if summary:
        print("Summary in Darija:")
        print(summary)
    else:
        print("Failed to generate Summary.")
