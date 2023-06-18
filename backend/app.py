# API endpoints for the backend
# imports
from flask import Flask, request
from flask_cors import CORS
from langchain.llms import OpenAI

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = "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"
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
MODEL = "gpt-4-0613"


# main route
@app.route("/")
def main():
    return {"success": True, "route": "main"}


# generate response route
@app.route("/api/response", methods=["POST"])
def generateResponse():
    data = request.get_json()
    response = OpenAI.generate(llm, MODEL, data)
    return {"message": data, "response": response}


# get clinical trials route
@app.route("/api/clinicalTrials")
def getClinicalTrials():
    return {"success": True, "route": "clinicalTrials"}


# main
if __name__ == "__main__":
    app.run(debug=True)
