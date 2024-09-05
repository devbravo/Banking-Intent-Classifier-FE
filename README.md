# Banking Intent Classifier Frontend

This repository contains the front-end of the **Banking Intent Classifier** project, which interacts with a backend API to predict customer intent based on their queries and also allows users to submit feedback about the predictions.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Frontend](#running-the-frontend)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This front-end allows users to interact with the **Banking Intent Classifier** via a web-based interface. Users can enter queries, view the predicted intent, and provide feedback if the predicted intent is incorrect.

The frontend communicates with the backend using two key API endpoints:
1. **Inference**: Takes user input and returns the predicted intent along with confidence scores.
2. **Feedback**: Collects user feedback about the prediction and logs it to improve future model performance.

## Tech Stack

- **Framework**: Streamlit (Python)
- **API Communication**: Requests to the backend (BentoML REST API)
- **Frontend Deployment**: Docker/Google Cloud

## Prerequisites

Before running the project locally, ensure you have the following installed:

- Python 3.8 or higher
- Streamlit
- Docker (optional, if containerizing the frontend)
- Google Cloud SDK (optional, if deploying on GCP)

## Installation

To set up the project locally:

1. Clone this repository:

    ```bash
    https://github.com/devbravo/Banking-Intent-Classifier-FE.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Banking-Intent-Classifier-FE
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables by creating a `.env` file in the root directory and adding the API URL:

    ```bash
    API_URL=http://localhost:8080  # or your production API URL
    ```

## Running the Frontend

You can run the front-end locally by executing the following command:

```bash
streamlit run src/app.py
```

The front-end will be accessible at `http://localhost:8501`.

### Docker Setup (Optional)

If you prefer to run the front-end in a Docker container:

1. Build the Docker image:

    ```bash
    docker build -t banking-intent-classifier-frontend .
    ```

2. Run the container:

    ```bash
    docker run -p 8501:8501 banking-intent-classifier-frontend
    ```

The front-end will be accessible at `http://localhost:8501`.

## Usage

1. Enter a customer service-related query in the input field.
2. Click the **Classify Intent** button.
3. The predicted intent and confidence score will be displayed below the input field.
4. If the prediction is incorrect, select the correct intent from the dropdown and submit feedback.
5. Feedback will be logged and displayed in a success message.

## Environment Variables

Make sure to configure the following environment variables:

- **`API_URL`**: The URL of the backend API where the inference and feedback endpoints are exposed.

Example `.env` file:

```bash
API_URL=http://localhost:8080
```

## API Endpoints

The front-end interacts with two API endpoints exposed by the backend:

1. **`/inference`**: Used to classify the user's input and return the predicted intent.
   - **Method**: `POST`
   - **Input**: 
     ```json
     {
       "text": "Why hasn't my card arrived yet?"
     }
     ```
   - **Response**:
     ```json
     {
       "predicted_intent": "card_not_received",
       "confidence_score": 0.95,
       "query_id": 123
     }
     ```

2. **`/submit_feedback`**: Used to submit feedback about the prediction's correctness.
   - **Method**: `POST`
   - **Input**:
     ```json
     {
       "query_id": 123,
       "is_correct": false,
       "corrected_intent": "tracking_my_card"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Feedback submitted successfully"
     }
     ```

## Contributing

If you'd like to contribute to the project, feel free to open an issue or submit a pull request on the repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or feedback, feel free to reach out via [diegofranco711@gmail..com](mailto:diegofranco711@gmail.com).

