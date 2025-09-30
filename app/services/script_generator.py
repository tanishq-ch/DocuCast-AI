import os
import google.generativeai as genai

def generate_podcast_script(text_content):
    """
    Uses the Gemini API to convert a block of text into a conversational script.

    Args:
        text_content (str): The source text extracted from the uploaded file.

    Returns:
        str: A formatted script with speaker tags, or an error message.
    """
    try:
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
        Based on the following text, generate an engaging and informative podcast script for two speakers, a Host and an Expert.
        The script should cover all the necessary information from the content, including minute details.
        Format the script clearly with speaker labels (e.g., "Host:", "Expert:").
        Make the conversation sound natural, with emotions and feelings where appropriate.
        The entire output should be only the script itself.

        --- TEXT CONTENT ---
        {text_content}
        --- END OF TEXT ---
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error generating script with Gemini: {e}")
        return f"Error: Could not generate script. Details: {str(e)}"