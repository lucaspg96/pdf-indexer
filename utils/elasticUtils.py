from elasticsearch import Elasticsearch, exceptions
from json import load
from elasticsearch.helpers import bulk
from .configUtils import get_config
import re

client = None

config = get_config("elastic")
index_name = config.get("index_name","documents")

def get_client():
    global client
    if client is None:
        print("Instantiating ES client...")
        client = Elasticsearch(hosts=config.get("host","http://localhost:9200"))   
        print(client.info())   
    
    return client

def create_index():
    mappings = load(open("index-mappings.json"))
    settings = load(open("index-settings.json"))
    try:
        get_client().indices.create(index=index_name, mappings=mappings, settings=settings)
    except exceptions.RequestError as ex:
        if ex.error == 'resource_already_exists_exception':
            pass # Index already exists. Ignore.
        else: # Other exception - raise it
            raise ex

def get_indexed_files():
    aggs = {
        "files" : {
            "terms" : { "field" : "file.keyword",  "size" : 500 }
        }
    }

    indexed_files = set(
        map(
            lambda f: f["key"].split("/")[-1],
            dict(get_client().search(index=index_name,size=0,aggs=aggs))["aggregations"]["files"]["buckets"])
    )

    return indexed_files

def insert_document_pages(pages):
    pages = [{
            "_index": index_name,
            "_source": page
        } for page in pages]

    bulk(get_client(), pages)

def parse_search_text(search):
    phrases = re.findall(r'"(.+?)"', search)
    query_string = re.sub(r'"(.+?)"','', search).strip()
    return phrases, query_string    

def search_documents(search_text):
    phrases,query_string = parse_search_text(search_text)

    should = []
    for phrase in phrases:
        should.append({
            "match_phrase_prefix": {
                "content": {
                "query": phrase
                }
            }
            })
        
    if not query_string == "":
        should.append({
            "query_string": {
                "query": query_string,
                "default_field": "content"
            }
            })

    query = {
        "bool": {
        "should": should
        }
    }

    highlight = {
        "fields": {
        "content": {}
        },
        "pre_tags": config.get("preTags","<strong>"),
        "post_tags": config.get("postTags","</strong>"),
        "fragment_size": config.get("highlightFragmentSize",300)
    }

    fields = ["file","page"]

    size = config.get("maxResultsSize", 10)

    results = dict(get_client().search(index=index_name, query=query, 
    highlight=highlight, source=fields, size=10))["hits"]["hits"]

    results_by_file = {}
    for result in results:
        file = result["_source"]["file"]
        if not file in results_by_file:
            results_by_file[file] = []
        
        results_by_file[file].append({
            "page":result["_source"]["page"],
            "highlight": result["highlight"]['content']}
        )

    return results_by_file