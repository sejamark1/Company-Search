import requests
import json
import sys

url = "https://api.companieshouse.gov.uk/search/companies?q={}"
query = "tesco"
api_key = "e2d9c1cf-15c9-438d-97c2-d305834265bb"

response = requests.get(url.format(query),auth=(api_key,''))
json_search_result = response.text
search_result = json.JSONDecoder().decode(json_search_result)

#print(search_result)



for company in search_result['items']:
    print(company['title'])