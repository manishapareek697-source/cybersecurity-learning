# Phishing Email Detection Model

## About the Project
This is a beginner-friendly cybersecurity and machine learning project that classifies email text as **Phishing** or **Safe** using Python and Scikit-learn.

## Features
- Email text classification
- TF-IDF text feature extraction
- URL and suspicious keyword feature extraction
- Logistic Regression machine learning model
- Accuracy and classification report
- Confusion matrix visualization
- Prediction for user-provided email text

## Technologies Used
- Python
- Pandas
- Scikit-learn
- Matplotlib
- SciPy

## Project Structure
```text
Phishing-Email-Detector/
├── data/
│   └── Phishing_validation_emails.csv
├── phishing_detector.py
├── requirements.txt
└── README.md
```

## Installation
Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## How to Run
Run the following command from the project directory:

```bash
python phishing_detector.py
```

## Model Evaluation
The model is evaluated using accuracy, precision, recall, F1-score, and a confusion matrix.

Actual evaluation results will be added after running the model successfully.

## Limitations
- Predictions are not a guarantee that an email is safe.
- Missing or suspicious keywords alone cannot confirm phishing.
- Dataset quality and class balance affect model performance.
- This is an educational project, not a production email security system.

## Responsible Use
Use public datasets responsibly. Do not publish private emails, personal information, passwords, or confidential data.

## Author
Cybersecurity Learning Project
