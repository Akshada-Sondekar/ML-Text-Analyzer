from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import joblib

# -----------------------------
# Initialize Flask App
# -----------------------------

app = Flask(__name__)

# Enable CORS
CORS(app)

# -----------------------------
# Load ML Model
# -----------------------------

model = joblib.load("model/model.pkl")

vectorizer = joblib.load("model/vectorizer.pkl")

# -----------------------------
# Initialize Database
# -----------------------------

def init_db():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            prediction TEXT
        )
    """)

    conn.commit()

    conn.close()

# Create database table
init_db()

# -----------------------------
# Home Route
# -----------------------------

@app.route("/")

def home():

    return "Spam Classifier API Running Successfully"

# -----------------------------
# Prediction Route
# -----------------------------

@app.route("/predict", methods=["POST"])

def predict():

    try:

        # Get JSON data
        data = request.get_json()

        text = data.get("text")

        # Validation
        if not text:

            return jsonify({
                "error": "Text is required"
            }), 400

        # Convert text to vector
        transformed_text = vectorizer.transform([text])

        # Prediction
        prediction = model.predict(transformed_text)[0]

        # Convert output
        result = "Spam" if prediction == 1 else "Not Spam"

        # -----------------------------
        # Save to Database
        # -----------------------------

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO history (text, prediction) VALUES (?, ?)",
            (text, result)
        )

        conn.commit()

        conn.close()

        # -----------------------------
        # Return Response
        # -----------------------------

        return jsonify({
            "prediction": result
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# History Route
# -----------------------------

@app.route("/history", methods=["GET"])

def history():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    conn.close()

    history_data = []

    for row in rows:

        history_data.append({
            "id": row[0],
            "text": row[1],
            "prediction": row[2]
        })

    return jsonify(history_data)

# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":

    app.run(debug=True)