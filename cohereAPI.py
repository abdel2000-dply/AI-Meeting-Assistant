import cohere
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Cohere client with API key
API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(API_KEY)
CHAT_API_ENDPOINT = "https://api.cohere.com/v1/chat"

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
            # Moroccan Arabic (Darija) Summary Prompt
            prompt = f"""لخص النص التالي المأخوذ من اجتماع مكتوب بالدارجة المغربية. 
خاص الملخص يكون واضح ومختصر، وكيهضر على الأفكار الرئيسية اللي تطرقات ليها الاجتماع بلا تقديم ولا كلام زائد.

النص:
"{transcription_text}"

الملخص:"""
        elif lang == "EN":
            # English Summary Prompt
            prompt = f"""Summarize the following text transcribed from a meeting in English. 
    Focus on the main points and ensure the summary is concise and clear.

    Text:
    "{transcription_text}"

    Summary:"""
        elif lang == "FR":
            # French Summary Prompt
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

# Function to chat with Cohere
def chat_with_cohere(message, context):
    headers = {
        "Authorization": f"BEARER {API_KEY}",
        "Content-Type": "application/json",
    }

    # Limit the length of the transcript included in the context
    transcript_excerpt = context['transcript'][:2000]  # Adjust the length as needed

    preamble = f"""You are an AI assistant helping summarize and analyze a meeting transcript. The user will ask questions about the transcript provided. Here is the transcript: {transcript_excerpt}. Respond clearly and concisely based on the user's query."""

    prompt = preamble + "\n\n" + message

    data = {
        "message": message,
        "chat_history": context.get("chat_history", []),
        "max_tokens": 100,  # Set a lower value for shorter responses
        "temperature": 0.2,  # Lower temperature for more direct responses
        "context": preamble,
        "documents": [{"text": context['transcript'], "title": "Meeting Transcript"}]
    }

    response = requests.post(CHAT_API_ENDPOINT, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        generated_response = response_data["text"]
        return generated_response
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
