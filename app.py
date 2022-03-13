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


#id, data, state, snowfall

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
        # result = es.search(
        #         index='enterprise-search-engine-info624-skisearch',
        #         query={
        #             'match_all': {}
        #         }
        #     )

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
            query={
                "match": {
                    "content": "dog"
                }
            }
        )


        # print(result['hits']['hits'])
        all_docs = {}

        return render_template('results.html', all_docs=all_docs)

        # query = request.form['ski_query']
        #
        # if not query:
        #     flash('Please Enter a query')
        # else:
        #     result = es.search(
        #         index='lord-of-the-rings',
        #         query={
        #             'match': {'quote': 'late'}
        #         }
        #     )
        #
        #     result['hits']['hits']
            # all_docs = {}
            # all_indices = es.indices.get_alias("*")
            #
            # # iterate over the index names
            # for ind in all_indices:
            #
            #     # skip hidden indices with '.' in name
            #     if "." not in ind[:1]:
            #         # nest another dictionary for index inside
            #         all_docs[ind] = {}
            #
            #         # print the index name
            #         print("\nindex:", ind)
            #
            #         # get 20 of the Elasticsearch documents from index
            #         docs = es.search(
            #             from_=0,  # for pagination
            #             index=ind,
            #             body={
            #                 'size': 10,
            #                 'query': {
            #                     # pass query paramater
            #                     'match_all': query
            #                 }
            #             })
            #
            #         # get just the doc "hits"
            #         docs = docs["hits"]["hits"]
            #
            #         # print the list of docs
            #         print("index:", ind, "has", len(docs), "num of docs.")
            #
            #         # put the list of docs into a dict key
            #         all_docs[ind]["docs"] = docs

            #return redirect(url_for('results'))

   # return render_template('search_page.html')


@app.route('/results')
def results():
    return render_template('results')



if __name__ == "__main__":
    app.run()
