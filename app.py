#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from azure.storage.blob import *
import string
import random
import requests
import configparser
from azure.cosmos import exceptions, CosmosClient, PartitionKey
sno = 0
app = Flask(__name__, instance_relative_config=True)
Config = configparser.ConfigParser()
Config.read("config.py")
endpoint = "https://mydemocosmosdb0303.documents.azure.com:443/"
key = '1fNXku9KwhWiWYqLyfj6cEdMw4epNrys7mcqVF6TRxRa1B4RwxOMos6c9b8khI0yevWk3itxJDqyrDROmXVqeg=='
client = CosmosClient(endpoint, key)
database_name = 'id'
container_name = 'con1'
database = client.create_database_if_not_exists(id=database_name)
container1 = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/lastName"),
    offer_throughput=400
)
# Account name
account = Config.get('DEFAULT', 'account')
# Azure Storage account access key
key = Config.get('DEFAULT', 'key')
# Container name
container = Config.get('DEFAULT', 'container')


blob_service = BlockBlobService(account_name=account, account_key=key)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        fileextension = filename.rsplit('.', 1)[1]
        global sno
        sno += 1
        file_item = {
            'id': str(sno),
            'filename': filename

        }
        try:
            blob_service.create_blob_from_stream(container, filename, file)
            container1.create_item(body=file_item)

        except Exception:
            print('Exception=' + Exception)
            pass
        ref = 'http://' + account + '.blob.core.windows.net/' + container + '/' + filename

    return render_template('uploadfile.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


# In[ ]:
