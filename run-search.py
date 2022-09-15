from utils import elasticUtils
from pprint import pprint

search = '"Bênção da Dragoa Rainha" dano aumento "Varinha de aço rubi"'
results = elasticUtils.search_documents(search)
pprint(results)