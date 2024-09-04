import os
import streamlit as st
import requests
from dotenv import load_dotenv
from src.utils.label_mapping import label_mapping

# Load environment variables
load_dotenv()
API_URL = os.getenv('API_URL')


if 'classification_done' not in st.session_state:
    st.session_state.classification_done = False


@st.cache_data()
def classify_intent(user_text):
    try:
        response = requests.post(f'{API_URL}/inference', json=user_text)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API error: {response.status_code}'}
    
    except Exception as e:
        return {'error': str(e)}


def submit_feedback(query_id, is_correct, corrected_intent=None):
    """
    Submit user feedback to the API.
    Args:
        query_id (int): The ID of the query for which feedback is being 
                        submitted.
        is_correct (bool): Whether the prediction was correct.
        corrected_intent (Optional[str]): The corrected intent if the 
                                          prediction was incorrect.
    Returns:
        str: The result of the feedback submission.
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
            return "error", f'API error: {response.status_code} - {response.text}'
    
    except requests.exceptions.RequestException as e:
        return f'Error: {e}'


if __name__ == '__main__':
    st.header('Banking Intent Classifier', divider='rainbow')
    
    text_input = st.text_input("Enter some text 👇")
    submit_btn = st.button('Classify Intent', type='secondary')
    
    if submit_btn:
        result = classify_intent(text_input)
        
        if 'error' in result:
            st.error(result['error'])
        else:
            st.session_state.classification_done = True
            st.session_state.query_id = result['query_id']
            st.session_state.predicted_intent = result['predicted_intent']
            st.session_state.confidence_score = result['confidence_score']
            print(st.session_state.query_id)
            
            st.subheader('Prediction Result')
            st.write(f"**Predicted Intent:** {result['predicted_intent']}")
            st.write(f"**Confidence Score:** {result['confidence_score']:.2f}")
    
    if st.session_state.get('classification_done', False):
        st.subheader('Was this prediction correct?')
        feedback_option = st.radio("Please select an option:", ('Yes', 'No'), 
                                   label_visibility="visible")
        
        if feedback_option == 'No':
            st.subheader('Please select the correct intent:')
            corrected_intent = st.selectbox('Correct Intent:', 
                                            list(label_mapping.values()), 
                                            label_visibility="visible")
        
        feedback_submit_btn = st.button('Submit Feedback', 
                                        key='feedback_submit_btn')
        
        if feedback_submit_btn:
            if feedback_option == 'No':
                status, feedback_message = submit_feedback(
                                          st.session_state.query_id, 
                                          is_correct=False, 
                                          corrected_intent=corrected_intent)
            else:
                status, feedback_message = submit_feedback(
                  st.session_state.query_id, 
                  is_correct=True)
            
            if status == "success":
                st.success(feedback_message)
            else:
                st.error(feedback_message)



