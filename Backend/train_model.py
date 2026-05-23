import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

import joblib

import os

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv(
    "spam.csv",
    encoding="latin-1"
)

# -----------------------------
# Keep Required Columns
# -----------------------------

df = df[["v1", "v2"]]

# -----------------------------
# Rename Columns
# -----------------------------

df.columns = ["label", "text"]

# -----------------------------
# Convert Labels
# spam = 1
# ham = 0
# -----------------------------

df["label"] = df["label"].map({
    "ham": 0,
    "spam": 1
})

# -----------------------------
# Show Dataset
# -----------------------------

print(df.head())

# -----------------------------
# Features and Labels
# -----------------------------

X = df["text"]

y = df["label"]

# -----------------------------
# TF-IDF Vectorization
# -----------------------------

vectorizer = TfidfVectorizer(
    stop_words="english"
)

X_vectorized = vectorizer.fit_transform(X)

# -----------------------------
# Split Dataset
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Train Model
# -----------------------------

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train, y_train)

# -----------------------------
# Predictions
# -----------------------------

predictions = model.predict(X_test)

# -----------------------------
# Accuracy
# -----------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# -----------------------------
# Create model folder
# -----------------------------

os.makedirs(
    "model",
    exist_ok=True
)

# -----------------------------
# Save Model
# -----------------------------

joblib.dump(
    model,
    "model/model.pkl"
)

joblib.dump(
    vectorizer,
    "model/vectorizer.pkl"
)

# -----------------------------
# Success Messages
# -----------------------------

print("\nModel saved successfully!")

print("Vectorizer saved successfully!")

# -----------------------------
# Test Predictions
# -----------------------------

sample_messages = [

    "Claim your reward now",

    "URGENT! You won a free lottery",

    "Hello friend how are you",

    "Free recharge available today",

    "Meeting at 5 pm"

]

print("\nSample Predictions:\n")

for message in sample_messages:

    transformed_message = vectorizer.transform([message])

    prediction = model.predict(transformed_message)[0]

    result = "Spam" if prediction == 1 else "Not Spam"

    print(f"Message: {message}")

    print(f"Prediction: {result}\n")