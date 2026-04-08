from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests


app = Flask(__name__)


FASTAPI_URL = "http://127.0.0.1:8000/predict"


# Load dataset for dropdown values
df = pd.read_csv("artifacts/data_ingestion/raw.csv")

transaction_types = sorted(df["TransactionType"].dropna().unique())

locations = sorted(df["Location"].dropna().unique())


@app.route("/")
def landing():

    return render_template("landing.html")


@app.route("/predict_page", methods=["GET", "POST"])
def predict_page():

    if request.method == "POST":

        data = {

            "TransactionID": int(request.form["TransactionID"]),
            "TransactionDate": request.form["TransactionDate"],
            "Amount": float(request.form["Amount"]),
            "MerchantID": int(request.form["MerchantID"]),
            "TransactionType": request.form["TransactionType"],
            "Location": request.form["Location"]

        }

        response = requests.post(FASTAPI_URL, json=data)

        prediction = response.json()["message"]

        return render_template("result.html", prediction=prediction)


    return render_template(
        "predict.html",
        transaction_types=transaction_types,
        locations=locations
    )


if __name__ == "__main__":

    app.run(debug=True)