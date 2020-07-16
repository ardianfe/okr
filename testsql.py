from sqlalchemy import create_engine
from models import *
engine = create_engine('postgresql://localhost/okr')


kresults = KeyResult.query.all()
for kr in kresults:
    print (kr)


