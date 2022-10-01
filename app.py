""" IMPORTANT
# Activate Virtual Environment: env/Scripts/activate 
# python app.py
"""

from flask import Flask 

app = Flask(__name__) 

@app.route('/') 
def index(): 
    return "Hello World" 

if __name__ == "__main__": 
    app.run(debug=True)