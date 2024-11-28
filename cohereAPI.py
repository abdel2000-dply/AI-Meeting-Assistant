import cohere

# cohere client eith api key
co = cohere.client()

# Generate Dareja to-dos from Dareja transciption
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

