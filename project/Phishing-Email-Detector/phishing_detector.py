
from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay
)

# 1. Find the dataset relative to this Python file
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Phishing_validation_emails.csv"

print("Dataset path:", DATA_PATH)
print("File exists:", DATA_PATH.exists())

if not DATA_PATH.exists():
    raise FileNotFoundError(
        "CSV file not found! Check the filename inside the data folder."
    )

# 2. Load dataset
df = pd.read_csv(DATA_PATH)

print("\nColumns:", df.columns.tolist())
print("Dataset shape:", df.shape)
print(df.head())

# 3. Identify text and label columns
def normalize_column(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())

columns = {
    normalize_column(col): col for col in df.columns
}

text_names = [
    "emailtext", "emailcontent", "emailbody",
    "email", "text", "body", "message", "content"
]

label_names = [
    "emailtype", "label", "class", "category",
    "emailcategory", "target", "emailclass"
]

text_col = next(
    (columns[name] for name in text_names if name in columns),
    None
)

label_col = next(
    (columns[name] for name in label_names if name in columns),
    None
)

if text_col is None or label_col is None:
    raise ValueError(
        "Could not identify text and label columns. "
        "Check the Columns output above."
    )

df = df[[text_col, label_col]].dropna().copy()
df.columns = ["email_text", "label"]

# 4. Convert labels into 0 = Safe, 1 = Phishing
def convert_label(value):
    value = str(value).strip().lower()

    if value in {"1", "phishing", "phishing email"}:
        return 1

    if value in {
        "0", "safe", "safe email",
        "legitimate", "legitimate email", "ham"
    }:
        return 0

    raise ValueError(f"Unknown label: {value}")

df["label"] = df["label"].apply(convert_label)
df["email_text"] = df["email_text"].astype(str)
df = df.drop_duplicates(subset=["email_text"])

if df["label"].nunique() != 2:
    raise ValueError("Dataset must contain both Safe and Phishing labels.")

if df["label"].value_counts().min() < 2:
    raise ValueError("Not enough examples in one of the classes.")

print("\nLabel counts:")
print(df["label"].value_counts())

# 5. Extract simple URL and keyword features
URL_PATTERN = re.compile(
    r"https?://[^\s<>\"']+|www\.[^\s<>\"']+",
    re.IGNORECASE
)

KEYWORDS = [
    "urgent", "verify", "password", "login",
    "account suspended", "click here",
    "confirm your account", "payment required"
]

SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "is.gd"]


def extract_features(email):
    email = str(email)
    lower = email.lower()
    urls = URL_PATTERN.findall(email)

    has_ip = int(bool(re.search(
        r"https?://(?:\d{1,3}\.){3}\d{1,3}",
        email,
        re.IGNORECASE
    )))

    keyword_count = sum(word in lower for word in KEYWORDS)
    shortener_count = sum(item in lower for item in SHORTENERS)
    https_count = sum(url.lower().startswith("https://") for url in urls)

    return [
        len(email),
        len(urls),
        has_ip,
        keyword_count,
        shortener_count,
        https_count
    ]


# 6. Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    df["email_text"],
    df["label"],
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)

# 7. Convert email text into numeric TF-IDF features
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_text = vectorizer.fit_transform(X_train)
X_test_text = vectorizer.transform(X_test)

# 8. Add URL and keyword features
X_train_extra = csr_matrix([
    extract_features(email) for email in X_train
])

X_test_extra = csr_matrix([
    extract_features(email) for email in X_test
])

X_train_final = hstack([X_train_text, X_train_extra])
X_test_final = hstack([X_test_text, X_test_extra])

# 9. Train the machine learning model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_final, y_train)

print("\nModel training completed!")

# 10. Evaluate the model
predictions = model.predict(X_test_final)

print(f"\nAccuracy: {accuracy_score(y_test, predictions):.2%}")

print("\nClassification report:")
print(classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Safe", "Phishing"],
    zero_division=0
))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    predictions,
    labels=[0, 1],
    display_labels=["Safe", "Phishing"],
    cmap="Blues"
)

plt.title("Phishing Email Detection")
plt.tight_layout()
plt.show()

# 11. Predict a new email
def predict_email(email):
    text_features = vectorizer.transform([email])
    extra_features = csr_matrix([extract_features(email)])

    combined = hstack([text_features, extra_features])
    prediction = model.predict(combined)[0]

    return "PHISHING" if prediction == 1 else "SAFE"


print("\n--- Test a new email ---")
email = input("Enter email text: ")
print("Prediction:", predict_email(email))
print("Note: This prediction does not guarantee email safety.")
