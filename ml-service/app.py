from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "ML Service Running 🚀"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    resume_text = data.get("text", "")

    skills = []

    # Simple skill detection (we will improve later)
    if "python" in resume_text.lower():
        skills.append("Python")
    if "java" in resume_text.lower():
        skills.append("Java")
    if "sql" in resume_text.lower():
        skills.append("SQL")

    return jsonify({
        "skills": skills,
        "message": "Analysis complete"
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)