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
        prompt = f"""خذ النص التالي المقتبس من اجتماع مكتوب بالدارجة المغربية، وحوله إلى لائحة ديال المهام اللي خاص يتدارو بعد الاجتماع. 
خاص كل خطوة تكون واضحة وسهلة للتنفيذ، مع ذكر شكون المسؤول على كل خطوة إلى كان ممكن، وزيد وقت محدد لإنجازها إلا كانت ضرورية.
تجنب تكرار المهام اللي راهي تدارو فالاجتماع.

النص:
"{transcription_text}"

الجواب:"""
    elif lang == "EN":
        prompt = f"""Transform the following meeting transcript into a list of follow-up actions. 
Each task should:
- Focus on actionable steps to be taken after the meeting.
- Specify who is responsible for the task.
- Include deadlines or timeframes where relevant.
- Avoid repeating tasks already completed during the meeting.

Text:
"{transcription_text}"

Response:"""
    elif lang == "FR":
        prompt = f"""Prenez le texte suivant, transcription d'une réunion en français, et transformez-le en une liste d'actions de suivi à réaliser après la réunion. 
Chaque tâche doit :
- Se concentrer sur des étapes concrètes à effectuer après la réunion.
- Indiquer la personne responsable de chaque tâche si possible.
- Inclure des échéances ou des délais lorsqu'ils sont pertinents.
- Éviter de répéter les tâches déjà accomplies pendant la réunion.

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
