from airflow.providers.mongo.hooks.mongo import MongoHook

def extract(**kwargs):
    hook = MongoHook(conn_id="mongo_default")
    collections = hook.get_collection("samples", "airflow")
    documents = list(collections.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    hook.close_conn()
    return documents

def transform(**kwargs):
    documents = kwargs.get("ti").xcom_pull(task_ids="t1")
    data = []
    for doc in documents:
        data.append({"mid": doc["_id"], "name": doc["name"]})
    return data

def load(**kwargs):
    data = kwargs.get("ti").xcom_pull(task_ids=kwargs.get("t2"))
    if not data:
        return data
    hook = MongoHook(conn_id="mongo_default")
    collections = hook.get_collection("destination", "airflow")
    collections.insert_many(data)
    hook.close_conn()
    return 'done'