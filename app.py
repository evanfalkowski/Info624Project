import json
import requests
from flask import Flask, render_template,  request, url_for, flash, redirect, json
from elasticsearch import Elasticsearch, helpers

app = Flask(__name__)
cloud_id = "https://info624project.es.us-central1.gcp.cloud.es.io:9243/"
user = "elastic"
password = "E8ESWK45BvcnmYFrCmF7MNdW"
es = Elasticsearch(
    hosts=cloud_id,
    basic_auth=(user, password)
)
results = []


@app.route("/")
def index():
    elastiSearchInfo = es.info()
    print(elastiSearchInfo)
    cluster_name = elastiSearchInfo['cluster_name']

    return render_template("index.html", cluster_name=cluster_name)


@app.route('/search_page', methods=['GET', 'POST'])
def search_page():
    if request.method == 'GET':
        return render_template('search_page.html')

    if request.method == 'POST':
        query = request.form['ski_query']

        if not query:
            flash('Please Enter a query')
        else:
            all_docs = {}
            all_indices = es.indices.get_alias("*")

            # iterate over the index names
            for ind in all_indices:

                # skip hidden indices with '.' in name
                if "." not in ind[:1]:
                    # nest another dictionary for index inside
                    all_docs[ind] = {}

                    # print the index name
                    print("\nindex:", ind)

                    # get 20 of the Elasticsearch documents from index
                    docs = es.search(
                        from_=0,  # for pagination
                        index=ind,
                        body={
                            'size': 10,
                            'query': {
                                # pass query paramater
                                'match_all': query
                            }
                        })

                    # get just the doc "hits"
                    docs = docs["hits"]["hits"]

                    # print the list of docs
                    print("index:", ind, "has", len(docs), "num of docs.")

                    # put the list of docs into a dict key
                    all_docs[ind]["docs"] = docs

            return redirect(url_for('results'))

    return render_template('search_page.html')


@app.route('/results')
def results():
    return render_template('results')






if __name__ == "__main__":
    app.run()
