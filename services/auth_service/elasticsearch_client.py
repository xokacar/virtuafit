from elasticsearch import Elasticsearch
from config import Config


es_host_url = f"https://{Config.ELASTICSEARCH_HOST}:{Config.ELASTICSEARCH_PORT}"


es = Elasticsearch(
    [es_host_url],
    http_auth=(Config.ELASTICSEARCH_USER, Config.ELASTICSEARCH_PASSWORD),
    verify_certs=False,  
    ssl_show_warn=False
)
