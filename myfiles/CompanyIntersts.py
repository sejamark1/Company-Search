


#Company class 
class CompanyIntersts(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    company_name = db.Column(db.String(200))

    def __init__(self, company_name): 
        self.company_name = company_name


        