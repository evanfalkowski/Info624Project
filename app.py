import json
import requests
from flask import Flask, render_template,  request
from elasticsearch import Elasticsearch
from dataclasses import dataclass

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
engine_name = "info-skiingweather"
es_index = "enterprise-search-engine-info-skiingweather"
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
        #enterprise-search-engine-info-skiingweather

        #build the query
        built_query = {
            "query": {
                "bool": {

                }
            }

        }
        built_query["query"]["bool"]["must"] = []

        if request.form['ski_query'] != "":
            built_query["query"]["bool"]["must"].append({"multi_match": {
                  "query": request.form['ski_query'],
                  "fields": [
                    "query",
                    "weather_desc",
                    "query_type",
                    "chance_of_snow",
                    "totalsnowfall_cm"
                  ]
                }
            })

        if request.form['selected_state'] != "":
            built_query["query"]["bool"]["must"].append({"term": {"query": request.form['selected_state']}})

        if request.form['snowfall_slider_min'] != "" and request.form['snowfall_slider_max'] != "":
            # if "must" not in built_query["query"]["bool"].keys():
            #     built_query["query"]["bool"]["must"] = []

            built_query["query"]["bool"]["must"].append({"range": {"totalsnowfall_cm": {"gte": request.form['snowfall_slider_min'], "lte": request.form['snowfall_slider_max']}}})

        print(built_query)

        result = es.search(
            index=es_index,
            body=built_query
        )

        all_docs = result['hits']['hits']
        print(all_docs)

        #convert the docs to html readable
        # {'_index': '.ent-search-engine-documents-info-skiingweather', '_id': 'doc-622fc597bfd9d5740f933c13',
        #  '_score': 3.1589372,
        #  '_ignored': ['query_type.location', 'totalsnowfall_cm.location', 'totalsnowfall_cm.date', 'weather_desc.float',
        #               'chance_of_snow.date', 'query_type.date', 'query.date', 'weather_desc.date',
        #               'weather_desc.location', 'windspeed_mph.date', 'temp_f.date', 'query.location', 'query.float',
        #               'query_type.float'],
        #  '_source': {'query': 'Kirkwood,CA', 'query_type': 'City', 'weather_desc': 'Clear', 'chance_of_snow': '0',
        #              'totalsnowfall_cm': '0.0', 'temp_f': '36', 'windspeed_mph': '6',
        #              'id': 'doc-622fc597bfd9d5740f933c13'}}

        formatted_docs = []
        for doc in all_docs:
            formatted_docs.append({
                "Location": doc['_source']['query'],
                "Weather": doc['_source']['weather_desc'],
                "SnowChance": doc['_source']['chance_of_snow'],
                "SnowAmount": doc['_source']['totalsnowfall_cm'],
                "Temp": doc['_source']['temp_f'],
                "Wind": doc['_source']['windspeed_mph'],
                "Score": doc['_score']
            })

        return render_template('results.html', docs=formatted_docs)


@app.route('/results')
def results():
    return render_template('results')



if __name__ == "__main__":
    app.run()
