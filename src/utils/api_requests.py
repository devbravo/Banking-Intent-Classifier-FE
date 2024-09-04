import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_URL = os.getenv('API_URL')


def classify_intent(user_text):
    """
    Sends a text input to the API to classify the intent.
    Args:
        user_text (str): The input text from the user.
    Returns:
        dict: The API response containing the predicted intent or an error.
    """
    try:
        response = requests.post(f'{API_URL}/inference', json=user_text)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API error: {response.status_code}'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
      

def submit_feedback(query_id, is_correct, corrected_intent=None):
    """
    Submits feedback to the API.
    Args:
        query_id (int): ID of the query to which the feedback relates.
        is_correct (bool): Whether the predicted intent was correct.
        corrected_intent (str, optional): The corrected intent, if applicable.
    Returns:
        tuple: (status, message) indicating success or failure.
    """
    try:
        feedback_data = {
            'query_id': query_id,
            'is_correct': is_correct,
            'corrected_intent': corrected_intent
        }
        response = requests.post(f'{API_URL}/submit_feedback', 
                                 json=feedback_data)
        if response.status_code == 200:
            return "success", "Feedback submitted successfully!"
        else:
            return "error", f"Error {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return "error", f'Error: {e}'