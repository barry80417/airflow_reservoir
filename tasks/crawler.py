import requests
url ='https://fhyv.wra.gov.tw/FhyWeb/v1/Api/Reservoir/Visual?$format=JSON'
r = requests.get(url)
response = r.text
import json
import pandas as pd
data = json.loads(response)
df = pd.json_normalize(data,record_path = ['ReservoirRealTimeInfos'])
from airflow.providers.mongo.hooks.mongo import MongoHook
hook = MongoHook(conn_id="mongo_default")
collection = hook.get_collection("reservoir", "airflow")
records = df.to_dict('records') 
collection.insert_many(records)
