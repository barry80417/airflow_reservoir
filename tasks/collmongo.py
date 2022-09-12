from airflow.providers.mongo.hooks.mongo import MongoHook

def extract(**kwargs):
    hook = MongoHook(conn_id="mongo_default")
    collections = hook.get_collection("reservoir", "airflow")
    documents = list(collections.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    hook.close_conn()
    return documents

def transform(**kwargs):
    documents = kwargs.get("ti").xcom_pull(task_ids="t1")
    data = []
    for doc in documents:
        data.append({"No":doc['StationNo'], "name": doc['StationName.zh_TW'], "Storage": doc['EffectiveStorage'],"Percentage": doc['PercentageOfStorage']})

    return data

def load(**kwargs):
    data = kwargs.get("ti").xcom_pull(task_ids=kwargs.get("t2"))
    if not data:
        return data
    hook = MongoHook(conn_id="mongo_default")
    collections = hook.get_collection("final", "airflow")
    collections.insert_many(data)
    hook.close_conn()
    return 'done'