import json
import requests
from flask import Flask, render_template, jsonify
from elasticsearch import Elasticsearch, helpers

app = Flask(__name__)


@app.route("/")
def index():
    cloud_id = "https://info624project.es.us-central1.gcp.cloud.es.io:9243/"
    user = "elastic"
    password = "E8ESWK45BvcnmYFrCmF7MNdW"

    es = Elasticsearch(
        hosts=cloud_id,
        basic_auth=(user, password)
    )

    elastiSearchInfo = es.info()
    print(elastiSearchInfo)
    json_data = elastiSearchInfo['cluster_name']
    cluster_name = json_data

    # Render HTML with count variable
    return render_template("index.html", cluster_name=cluster_name)

if __name__ == "__main__":
    app.run()
