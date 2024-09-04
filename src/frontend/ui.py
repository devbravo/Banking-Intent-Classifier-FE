import streamlit as st
from src.utils.api_requests import classify_intent, submit_feedback
from src.utils.label_mapping import label_mapping


def render_header():
    """Render the header of the Streamlit app."""
    st.header('Banking Intent Classifier', divider='rainbow')


def render_text_input():
    """Render the text input and classify button."""
    text_input = st.text_input("Enter some text 👇")
    submit_btn = st.button('Classify Intent', type='secondary')

    return text_input, submit_btn


def render_prediction_result():
    """Render the prediction result and confidence score."""
    st.subheader('Prediction Result')
    st.write(f"**Predicted Intent:** {st.session_state.predicted_intent}")
    st.write(f"**Confidence Score:** {st.session_state.confidence_score:.2f}")


def render_feedback_section():
    """Render the feedback section and handle feedback submission."""
    st.subheader('Was this prediction correct?')
    feedback_option = st.radio("Please select an option:", ('Yes', 'No'),
                               label_visibility="visible")

    if feedback_option == 'No':
        st.subheader('Please select the correct intent:')
        corrected_intent = st.selectbox('Correct Intent:',
                                        list(label_mapping.values()),
                                        label_visibility="visible")
    else:
        corrected_intent = None

    feedback_submit_btn = st.button('Submit Feedback', 
                                    key='feedback_submit_btn')

    if feedback_submit_btn:
        status, feedback_message = submit_feedback(
            st.session_state.query_id,
            is_correct=(feedback_option == 'Yes'),
            corrected_intent=corrected_intent
        )

        if status == "success":
            st.success(feedback_message)
        else:
            st.error(feedback_message)


def render_ui():
    """Main UI function that combines all components."""
    render_header()

    text_input, submit_btn = render_text_input()

    if submit_btn:
        result = classify_intent(text_input)

        if 'error' in result:
            st.error(result['error'])
        else:
            st.session_state.classification_done = True
            st.session_state.query_id = result['query_id']
            st.session_state.predicted_intent = result['predicted_intent']
            st.session_state.confidence_score = result['confidence_score']
            render_prediction_result()

    if st.session_state.get('classification_done', False):
        render_feedback_section()