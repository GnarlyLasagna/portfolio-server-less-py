# atexuguinho
#

import azure.functions as func
import logging
import os
import json
from azure.cosmos import CosmosClient

URL = os.getenv("CosmosDBURL")
KEY = os.getenv("CosmosDBKey")

client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'azureresume'
database = client.get_database_client(DATABASE_NAME)
CONTAINER_NAME = 'counter'
container = database.get_container_client(CONTAINER_NAME)


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route("HttpTrigger", methods=['GET', 'POST'])
def HttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        new_count = update_counter()
        return func.HttpResponse(json.dumps(new_count), status_code=200)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)

def update_counter():
    query = 'SELECT * FROM c WHERE c.id = "1"'
    results = container.query_items(query=query, enable_cross_partition_query=True)
    count_value = None

    for item in results:
        count_value = item.get('count')
        updated_count = count_value + 1
        item['count'] = updated_count
        container.upsert_item(item)

    if count_value is None:
        raise Exception("No item found with id = '1'")

    logging.info(f"Updated count: {updated_count}")
    return {"count": updated_count}
