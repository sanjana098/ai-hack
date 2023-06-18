# API endpoints for the backend
# imports
from flask import Flask, request
from flask_cors import CORS, cross_origin
import openai

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
MODEL = "gpt-4-0613"


# main route
@app.route("/")
def main():
    return {"success": True, "route": "main"}


# generate response route
@app.route("/api/response", methods=["POST"])
@cross_origin()
def generateResponse():
    data = request.get_json()
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a killer assistant trained by OpenAI"
            },
            {
                "role": "user",
                "content": data["message"]
            }
        ]
    )
    return {
        "data": data,
        "message": response
    }


# get clinical trials route
@app.route("/api/clinicalTrials")
@cross_origin()
def getClinicalTrials():
    return {"success": True, "route": "clinicalTrials"}


# main
if __name__ == "__main__":
    app.run(debug=True)
