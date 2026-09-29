from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"


@app.route("/")
def home():
    return "SpeakSmart Cloud Backend is ONLINE"


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        mode = data.get("mode")
        transcript = data.get("transcript")

        if not mode or not transcript:
            return jsonify({
                "success": False,
                "error": "Missing mode or transcript"
            }), 400

        if mode == "grammar":

            prompt = f"""
You are SpeakSmart, an English learning assistant.

The student said:

"{transcript}"

Check the grammar.

Return ONLY:

TRANSCRIPT:
{transcript}

CORRECTION:
<corrected sentence>

FEEDBACK:
<one short explanation>
"""

        elif mode == "vocabulary":

            prompt = f"""
You are SpeakSmart, an English vocabulary teacher.

The student said:

"{transcript}"

Choose one useful word or phrase from the sentence.

Return ONLY:

TRANSCRIPT:
{transcript}

WORD:
<word>

MEANING:
<simple meaning>

SYNONYM:
<one synonym>

EXAMPLE:
<short example>
"""

        elif mode == "challenge":

            prompt = f"""
You are SpeakSmart, an English speaking coach.

The student said:

"{transcript}"

Evaluate the English.

Return ONLY:

TRANSCRIPT:
{transcript}

GRAMMAR:
<short feedback>

VOCABULARY:
<short feedback>

FEEDBACK:
<one short improvement tip>
"""

        else:

            return jsonify({
                "success": False,
                "error": "Invalid mode"
            }), 400


        result = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return jsonify({
            "success": True,
            "mode": mode,
            "result": result.text
        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )