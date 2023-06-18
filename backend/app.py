# API endpoints for the backend
# imports
from flask import Flask, request
from flask_cors import CORS, cross_origin
import openai

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = ""
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
                "content": "You are a clinical trials assistant trained by OpenAI",
            },
            {"role": "user", "content": data["message"]},
        ],
    )
    return {"data": data, "message": response}


# get clinical trials route
@app.route("/api/clinicalTrials")
@cross_origin()
def getClinicalTrials():
    return {"success": True, "route": "clinicalTrials"}


# get chances for certain health issues route
@app.route("/api/chances", methods=["GET", "POST"])
def getChances():
    age = None
    birthGender = None
    userInput = "I'm male, 16 with a headache"
    if request.method == "GET":
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {
                    "role": "system",
                    "content": "Assistant is a large language model trained by OpenAI.",
                },
                {
                    "role": "user",
                    "content": userInput
                    + "only give chances in percentages (out of 100%) in valid python dictionary format (don't include escape characters) { issue: percentage } and nothing else",
                },
            ],
        )
        filter = (
            response["choices"][0]["message"]["content"]
            .replace("\n", "")
            .replace("\\", "")
        )
        print(filter)
    return {"response": response}


# main
if __name__ == "__main__":
    app.run(debug=True)
