
def write_search_result(data):
    with open("search.txt", "w") as searchFile: 
        searchFile.write(data)

def read_search_result():
    with open("search.txt", "r") as searchFile: 
        return searchFile.read()
