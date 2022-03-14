import json
import requests
from flask import Flask, render_template,  request, url_for, flash, redirect, json
from elasticsearch import Elasticsearch, helpers

app = Flask(__name__)
cloud_id = "https://info624project.es.us-central1.gcp.cloud.es.io:9243/"
user = "elastic"
api_key = 'search-bcz4qrvbu6v1xrbzxigm4pky'
password = "E8ESWK45BvcnmYFrCmF7MNdW"

es = Elasticsearch(
    hosts=cloud_id,
    basic_auth=(user, password)
)
results = []
engine_name = "info624-skisearch"

states = ["", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


@app.route("/")
def index():
    elastiSearchInfo = es.info()
    print(elastiSearchInfo)
    cluster_name = elastiSearchInfo['cluster_name']

    return render_template("index.html", cluster_name=cluster_name)


@app.route('/search_page', methods=['GET', 'POST'])
def search_page():
    if request.method == 'GET':
        return render_template('search_page.html', states=states)

    if request.method == 'POST':

        print(request.form['ski_query'])
        print(request.form['selected_state'])

        print(request.form['snowfall_slider_min'])
        print(request.form['snowfall_slider_max'])

        #the name of the index
        #enterprise-search-engine-info624-skisearch

        #gets all the docs
        # {
        #     "query": {
        #         "bool": {
        #             "must": {
        #                 "match_all": {}
        #             },
        #             "filter": {
        #                 "term": {
        #                     "status": "active"
        #                 }
        #             }
        #         }
        #     }
        # }

        #build the query
        built_query = {
            "bool": {

            }
        }

        if request.form['ski_query'] != "":
            built_query["bool"]["filter"] = {"term": {"data": request.form['ski_query']}}

        if request.form['selected_state'] != "":
            built_query["bool"]["must"] = {"term": {"state": request.form['selected_state']}}

        if request.form['snowfall_slider_min'] != "":
            built_query["bool"]["must"] = {"term": {"state": request.form['selected_state']}}

        if request.form['snowfall_slider_max'] != "":
            built_query["bool"]["must"] = {"term": {"state": request.form['selected_state']}}

        result = es.search(
            index='enterprise-search-engine-info624-skisearch',
            query=built_query
        )

        all_docs = result['hits']['hits']

        return render_template('results.html', all_docs=all_docs)


@app.route('/results')
def results():
    return render_template('results')



if __name__ == "__main__":
    app.run()
