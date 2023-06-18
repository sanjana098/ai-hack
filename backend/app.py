# API endpoints for the backend
# imports
from flask import Flask
from flask_cors import CORS
from langchain.llms import OpenAI

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = ""
llm = OpenAI(openai_api_key=OPENAI_API_KEY)


# main route
@app.route("/")
def main():
    return {"success": True, "route": "main"}


# generate response route
@app.route("/api/response")
def generateResponse():
    response = llm.predict("")
    return {"response": response}


# get clinical trials route
@app.route("/api/clinicalTrials")
def getClinicalTrials():
    return {"success": True, "route": "clinicalTrials"}


# main
if __name__ == "__main__":
    app.run(debug=True)
