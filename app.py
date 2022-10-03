""" TASK
To build a Web Application which allows a user to search for Companies using the
Companies House API and save companies of interest.

NOT FRONT END QUERY, SHOULD BE SERVER SIDE. 
"""

""" IMPORTANT
# Activate Virtual Environment: env/Scripts/activate 
# python app.py
"""


from array import array
from email.policy import strict
from itertools import product
from math import prod
from operator import methodcaller
from xml.sax.handler import all_properties

from django.shortcuts import redirect
from flask import Flask, render_template, url_for, request, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os, json, sys, requests
from django.shortcuts import redirect

#API 
API_KEY = "e2d9c1cf-15c9-438d-97c2-d305834265bb"


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

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method=='POST':
        url = "https://api.companieshouse.gov.uk/search/companies?q={}"
        query = str(request.form["company_search_content"])
        api_key = "e2d9c1cf-15c9-438d-97c2-d305834265bb"

        response = requests.get(url.format(query),auth=(api_key,''))
        json_search_result = response.text
        search_result = json.JSONDecoder().decode(json_search_result)

        return render_template("index.html", companies = search_result['items'])
    
        
    return render_template("index.html", companies = [])
 

#if request is made to (/), get method will return the following. 
def get(): 
    return jsonify({'msg', 'Hola '})



# @app.route('/interest')
# def view_or_remove_interest(): 
#     return render_template("interest.html")


#Create a fake company and add the data to the database, not from API. 
@app.route('/companies', methods=['POST']) 
def add_company(): 
    cName = request.json['company_name'] 
    new_company = CompanyIntersts(cName)
    db.session.add(new_company) 
    db.session.commit()

    return company_schema.jsonify(new_company)

#Get the product, also option to delete, thus POST 
@app.route('/interest', methods=['GET', 'POST']) 
def get_companies(): 
    all_company= CompanyIntersts.query.all() 
    result = companies_schema.dump(all_company)
    return render_template("interest.html", interests = result) 
#    return jsonify(result[0]["company_name"])





#Get a single company, many be used to delete purposes. 
@app.route('/myinterst/<id>', methods=['GET', 'POST']) 
def get_company(id): 
    company= CompanyIntersts.query.get(id) 
    return company_schema.jsonify(company)


#DELETE COMPANY 
@app.route('/interest/<int:id>', methods=['DELETE']) 
def delete_company(id): 
    company_delete = CompanyIntersts.query.get_or_404(id) 
    #company= CompanyIntersts.query.get(id) 
    db.session.delete(company_delete) 
    db.session.commit()
    return redirect("/")



#SERVER
if __name__ == "__main__": 
    app.run(debug=True)

