from elasticsearch import Elasticsearch, helpers
from config import *

client = Elasticsearch(
    hosts = [os.getenv('ELASTIC_ENDPOINT')],
    http_auth = (os.getenv('ELASTIC_ID'), os.getenv('ELASTIC_PASSWORD'))
)

if __name__ == "__main__":
    print(client.info())