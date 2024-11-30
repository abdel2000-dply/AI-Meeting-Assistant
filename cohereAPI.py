import cohere
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Cohere client with API key
API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(API_KEY)

# Generate to-dos from transcription
def generate_todos(transcription_text, lang):
    # Define the prompt based on the language
    if lang == "AR":
        prompt = f"""خذ النص التالي المقتبس من اجتماع مكتوب بالدارجة المغربية، وحوله إلى قائمة واضحة ومختصرة للمهام. 
يرجى التأكد من وضوح النص وسهولة الفهم. كل مهمة جديدة يجب أن تبدأ في سطر جديد.

النص:
"{transcription_text}"

الجواب:"""
    elif lang == "EN":
        prompt = f"""Transform the following text, which is a transcription from a meeting in English, into a clear and concise to-do list. 
Each task should be actionable and start on a new line. Ensure precision and clarity in task descriptions.

Text:
"{transcription_text}"

Response:"""
    elif lang == "FR":
        prompt = f"""Prenez le texte suivant, transcription d'une réunion en français, et transformez-le en une liste de tâches concise et claire. 
Assurez-vous que chaque tâche est bien définie, facilement compréhensible et commence sur une nouvelle ligne.

Texte :
"{transcription_text}"

Réponse :"""
    else:
        raise ValueError("Unsupported language")

    # Dynamic temperature and token management
    max_tokens = min(400, len(transcription_text.split()) * 2)  # 2 tokens per word approx.
    temperature = 0.7 if len(transcription_text.split()) < 100 else 0.5

    try:
        # Call Cohere's generate endpoint
        response = co.generate(
            model="command-r-plus-08-2024",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        # Extract and return the generated to-do list
        todos = response.generations[0].text.strip()
        return todos
    except Exception as e:
        print("Error generating to-dos:", e)
        return None

# Function to summarize transcription
def summarize_text(transcription_text, lang):
    # Dynamic temperature and token management
    max_tokens = min(400, len(transcription_text.split()) * 2)  # 2 tokens per word approx.
    temperature = 0.7 if len(transcription_text.split()) < 100 else 0.5

    try:
        # Define the model and language-specific parameters
        if lang == "AR":
            prompt = f"""لخص النص التالي المستخلص من اجتماع مكتوب بالدارجة المغربية. 
يرجى كتابة الملخص بشكل مختصر وواضح مع التركيز على الأفكار الرئيسية.

النص:
"{transcription_text}"

الملخص:"""
        elif lang == "EN":
            prompt = f"""Summarize the following text transcribed from a meeting in English. 
Focus on the main points and ensure the summary is concise and clear.

Text:
"{transcription_text}"

Summary:"""
        elif lang == "FR":
            prompt = f"""Résumez le texte suivant transcrit d'une réunion en français. 
Veuillez rédiger un résumé clair et concis en mettant en avant les idées principales.

Texte :
"{transcription_text}"

Résumé :"""
        else:
            raise ValueError("Unsupported language")
            return None

        # Call Cohere's generate endpoint with language-specific parameters
        response = co.generate(
            model="command-r-plus-08-2024",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        # Return the generated summary
        summary = response.generations[0].text.strip()
        return summary
    except Exception as e:
        print(f"Error using co.summarize for {lang}: {e}")
        return None
