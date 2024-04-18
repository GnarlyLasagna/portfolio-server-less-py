import azure.functions as func
# Your existing code here

import os
#from azure.cosmos import CosmosClient, exceptions, PartitionKey
from azure.cosmos.aio import CosmosClient 
import json
import asyncio
import azure.functions as func


URL = os.getenv("CosmosDBURL")  # Retrieve URL from environment variables
KEY = os.getenv("CosmosDBKey")  # Retrieve key from environment variables

client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'azureresume'
database = client.get_database_client(DATABASE_NAME)
CONTAINER_NAME = 'counter'
container = database.get_container_client(CONTAINER_NAME)

## Queries with the asynchronous client
async def create_lists():

    query = 'SELECT * FROM counter c WHERE c.id = "1"'
    results = container.query_items(query=query)

    async for item in results:
        # Get the current count value
        count_value = item.get('count')

        # Increment the count value by 1
        updated_count = count_value + 1

        # Update the item in the container with the new count value
        item['count'] = updated_count
        await container.upsert_item(item)
        
        print(f"Updated count: {updated_count}")





async def update_counter(req: func.HttpRequest) -> func.HttpResponse:
    try:
        query = 'SELECT * FROM counter c WHERE c.id = "1"'
        results = container.query_items(query=query)

        async for item in results:
            count_value = item.get('count')
            updated_count = count_value + 1
            item['count'] = updated_count
            await container.upsert_item(item)
            
            return func.HttpResponse(f"Updated count: {updated_count}", status_code=200)
        
        return func.HttpResponse("No item found with id = '1'", status_code=404)
    
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)

