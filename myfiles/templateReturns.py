from flask import render_template





#TEMPLATED RETURN 
def returnInterestTemplate(dataFromDatabase, delMsg): 
    return render_template("interest.html", interests = dataFromDatabase, deleteMessage=delMsg, numOfInterest = len(dataFromDatabase)) 
def returnSearchPageTemplate(search_result, msg="", dataFromDatabase="0"): 
    return render_template("index.html", resultCount = len(search_result['items']) , companies = search_result['items'], infoMessage = msg, numOfInterest = len(dataFromDatabase))        

