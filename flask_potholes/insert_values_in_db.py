from flask_pot import db
from flask_pot.models import Potholes
import datetime

#db.create_all()
potholes_locations = ['1700 Cumberland Ave., Knoxville']
for pl in potholes_locations:
    pothole = Potholes(location=pl, size=0.5, depth=0.3, serviced=0,  date_created=datetime.datetime.now().date()- datetime.timedelta(days=2))
    db.session.add(pothole)
    db.session.commit()

print(Potholes.query.all())

