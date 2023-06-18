# API endpoints for the backend
# imports
from flask import Flask, request
from flask_cors import CORS, cross_origin
import openai
import numpy as np
import mindsdb_sdk

import json

# from config import OPENAI_API_KEY, MINDSDB_PASSWORD, MINDSDB_EMAIL

import numpy as np
from numpy.linalg import norm

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
    prompt = data["message"]

    MINDSDB_EMAIL = ""
    MINDSDB_PASSWORD = ""
    OPENAI_API_KEY = ""

    with open("config/config.json", "r") as d:
        jsondata = json.load(d)
        OPENAI_API_KEY = jsondata["OPENAI_API_KEY"]
        MINDSDB_PASSWORD = jsondata["MINDSDB_PASSWORD"]
        MINDSDB_EMAIL = jsondata["MINDSDB_EMAIL"]

    openai.api_key = OPENAI_API_KEY

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Is there a medical condition in this sentence? Say only 1 if Yes or 0 if No - "
                + prompt,
            }
        ],
    )["choices"][0]["message"]["content"]

    if res == "0":
        data = request.get_json()
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a clinicaltrials assistant trained by OpenAI",
                },
                {"role": "user", "content": data["message"]},
            ],
        )["choices"][0]["message"]["content"]
        return {"data": data, "message": response}

    server = mindsdb_sdk.connect(
        "https://cloud.mindsdb.com", login=MINDSDB_EMAIL, password=MINDSDB_PASSWORD
    )
    dbs = server.list_databases()
    db = dbs[0]
    query = db.query("SELECT * FROM clinical_trials_subset;")
    s = query.fetch()

    prefix_condition = "Derive only the clinical condition from the sentence - "
    # prompt = "I am conducting a clinical trial for Covid19. I'd like to know the potential adverse effects of this study based on the past trials"
    medical_condition = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prefix_condition + prompt}],
    )["choices"][0]["message"]["content"]

    print("Medical condition - ", medical_condition)
    input_embedding = openai.Embedding.create(
        input=[medical_condition.replace("\n", " ")], model="text-embedding-ada-002"
    )["data"][0]["embedding"]
    candidate_embeddings = openai.Embedding.create(
        input=s["Conditions"].tolist(), model="text-embedding-ada-002"
    )["data"]

    c_embeddings = []

    for embedding in candidate_embeddings:
        c_embeddings.append(embedding["embedding"])

    input_embedding = np.array(input_embedding)
    c_embeddings = np.array(c_embeddings)

    # compute cosine similarity
    cosine = np.sum(input_embedding * c_embeddings, axis=1) / (
        norm(c_embeddings) * norm(input_embedding)
    )
    ind = np.argmax(cosine)
    record = s.loc[[ind]]

    new_prompt = "What are some adverse effects of this clinical trial"

    record_str = (
        " " + str(record["Adverse Conditions"]) + " " + str(record["Outcome Measures"])
    )
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": new_prompt + record_str}],
    )["choices"][0]["message"]["content"]
    print(res)
    return {"data": data, "message": res}


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
