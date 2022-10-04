from array import array
from curses import flash
from email.policy import strict
from itertools import product
from math import prod
from operator import methodcaller
from xml.sax.handler import all_properties
from django.shortcuts import redirect
from flask import Flask, render_template, url_for, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os, json, sys, requests, time
from django.shortcuts import redirect


from myfiles.templateReturns import *
from myfiles.inputSearchResults import * 





 

#API 
API_KEY = "e2d9c1cf-15c9-438d-97c2-d305834265bb"
query_search_result = ""


#Init app
app = Flask(__name__, template_folder='template') 
basedir = os.path.abspath(os.path.dirname(__file__)) 

#Init Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#Init db 
db = SQLAlchemy(app) 
#Init marshmallow 
ma = Marshmallow(app) 


#Company class 
class CompanyIntersts(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    company_name = db.Column(db.String(200))

    def __init__(self, company_name): 
        self.company_name = company_name

#Company Schema
class CompanySchema(ma.Schema): 
    class Meta: 
        fields  = ('id', 'company_name')

#Init Schema 
company_schema = CompanySchema() 
companies_schema = CompanySchema(many=True)








#RETURNS the user interest data that is stored in the database. 
def get_interest_from_database(): 
    all_company= CompanyIntersts.query.all() 
    result = companies_schema.dump(all_company)
    return result

def get_search_results_from_API(query): 
    params = {'limit':50}
    url = "https://api.companieshouse.gov.uk/search/companies?q={}"
    #query = str(request.form["company_search_content"])
    response = requests.get(url.format(query),auth=(API_KEY,''), params=params)
    json_search_result = response.text
    search_result = json.JSONDecoder().decode(json_search_result)
    return search_result



#Get the searched result and displays it here.
@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method=='POST':
        write_search_result(str(request.form["company_search_content"]))
        query_search_result = str(request.form["company_search_content"])
        search_result = get_search_results_from_API(query_search_result)
        return returnSearchPageTemplate(search_result,"",get_interest_from_database())  
    return render_template("index.html", companies = [], numOfInterest = len(get_interest_from_database()))
 






#Create a fake company and add the data to the database, not from API. 
@app.route('/companies/<companyName>', methods=["POST", "GET"]) 
def add_company_to_database(companyName): 
    try:
        new_company = CompanyIntersts(companyName)
        db.session.add(new_company) 
        db.session.commit()
        query_search_result = read_search_result() #
        search_result = get_search_results_from_API(query_search_result)
        return returnSearchPageTemplate(search_result, str(companyName + "Added to your interest!"),get_interest_from_database() )  
    except:
        search_result = get_search_results_from_API(query_search_result)
        return returnSearchPageTemplate(search_result, str(companyName + " " + "Added to your interest!"),get_interest_from_database())  

    # return company_schema.jsonify(new_company)

#Get the product, also option to delete, thus POST 
@app.route('/interest', methods=['GET', 'POST']) 
def get_companies(): 
    return returnInterestTemplate(get_interest_from_database(), "")
#    return jsonify(result[0]["company_name"])



#DELETE COMPANY from interest
#TODO: should redirect to /interest instead /interest/id
@app.route('/interest/<int:id>') 
def delete_interest_from_database(id): 
    company_delete = CompanyIntersts.query.get_or_404(id) 
    # #company= CompanyIntersts.query.get(id) 
    try: 
        db.session.delete(company_delete) 
        db.session.commit()
        Flask.flash(f"Sucessfully Deleted!")
        #return Flask.redirect(url_for("interest"))
        time.sleep(10)
        return returnInterestTemplate(get_interest_from_database(), "Sucessfully deleted!")
    except:
        return returnInterestTemplate(get_interest_from_database(), "Sucessfully deleted!")








if __name__ == "__main__": 
    app.run(debug=True)

