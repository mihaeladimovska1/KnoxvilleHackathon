from flask import render_template, url_for, flash, redirect
from flask_pot import app, db
from flask_pot.forms import RegistrationForm, LoginForm, DriverForm, PotholeCompletedForm
from flask_pot.models import Potholes, Drivers
import datetime
from flask_pot.routing import calculate_optimal_tours


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pothole = Potholes(location=form.location.data, size=form.size.data, depth=form.depth.data, photo=form.photo.data, serviced=0)
        db.session.add(pothole)
        db.session.commit()
        flash(f'Request submitted for pothole at {form.location.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Report Pothole', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'driver' and form.password.data == 'driving':

            flash('You have been logged in!', 'success')
            #query that gets the potholes requests that are not serviced with timestamp up to yesterday
            '''relevant_potholes = Potholes.query.all()
            current_date = datetime.datetime.now().date()
            pothole_locations = []
            for rp in relevant_potholes:
                if rp.serviced==0 and rp.date_created < current_date:
                    pothole_locations.append(rp.location)
            #print(len(pothole_locations))
            #flash('Potholes locations: '+ str(pothole_locations))
            trucks_start_location = "415 W Governor John Sevier Hwy, Knoxville"
            optimal_tours = calculate_optimal_tours(trucks_start_location, pothole_locations)
            flash('Your tour for today is: ')
            flash(str(optimal_tours["distance"]["tour"]))
            #call the calculate route method
            #flash the route'''
            return redirect(url_for('driver'))
        else:
            flash('Login Unsuccessful. Please check username and password with your admin', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/driver", methods=['GET', 'POST'])
def driver():
    form = DriverForm()

    if form.validate_on_submit():
        if form.submitroute.data:

            #query that gets the potholes requests that are not serviced with timestamp up to yesterday
            relevant_potholes = Potholes.query.all()

            current_date = datetime.datetime.now().date()
            pothole_locations = []
            for rp in relevant_potholes:
                if rp.serviced==0 and rp.date_created < current_date:
                    pothole_locations.append(rp.location)
            print("hereee: ", len(pothole_locations))
            flash("Num potholes: " + str(len(pothole_locations)))
            #print(len(pothole_locations))
            #flash('Potholes locations: '+ str(pothole_locations))
            trucks_start_location = "415 W Governor John Sevier Hwy, Knoxville"
            optimal_tours = calculate_optimal_tours(trucks_start_location, pothole_locations)
            flash('Your tour with shortest distance for today is: ')
            flash(str(optimal_tours["distance"]["tour"]))

            flash('Your tour with shortest duration for today is: ')
            flash(str(optimal_tours["duration"]["tour"]))
            #flash(str("Total distance: " + str(optimal_tours)))
            #call the calculate route method
            #flash the route
            return redirect(url_for('driver'))
        elif form.submitcompleted.data and ~form.submitroute.data:
            wo = form.pothole_number.data
            print(type(wo))
            #wo=int(wo)
            pt = Potholes.query.filter_by(id=wo).first()
            pt.serviced = 1
            #db.session.commit()
            flash(f'Pothole with id: ' +str(pt) + ' completed!', 'success')
            return redirect(url_for('driver'))


    return render_template('driver.html', title='Driver', form=form)



@app.route("/completed_pothole", methods=['GET', 'POST'])
def completed_pothole():
    form = PotholeCompletedForm()

    if form.validate_on_submit():
        pt = Potholes.query.filter_by(id=form.pothole_number).first()
        pt.serviced=1
        db.session.commit()

        flash(f'Pothole completed!', 'success')
        return redirect(url_for('driver'))
    return render_template('driver.html', title='Driver', form=form)