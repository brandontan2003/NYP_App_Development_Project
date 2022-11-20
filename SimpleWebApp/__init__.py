from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateEvent, CreateSingleEvent, CreateRecurringEvent, CreateAttendance
import shelve, SingleEvent, RecurringEvent, Attendance
import flask_excel as excel
import json
import plotly
import plotly.graph_objs as go
import plotly.graph_objects as px
import datetime

app = Flask(__name__)
app.secret_key = "hello"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

#Brandon
#Admin
@app.route('/createEvent', methods=['GET', 'POST'])
def create_event():
    create_event_form = CreateEvent(request.form)
    if create_event_form.data['event'] == "S":
        return redirect(url_for("create_single_event"))

    elif create_event_form.data['event'] == "R":
        return redirect(url_for('create_recurring_event'))

    return render_template('createEvent.html', form=create_event_form)


@app.route('/createSingleEvent', methods=['GET', 'POST'])
def create_single_event():
    create_single_form = CreateSingleEvent(request.form)
    date_error = None
    pax_error = None
    title_error = None
    try:
        event_dict = {}
        db = shelve.open('event.db', 'r')
        event_dict = db['Events']
        db.close()

        max_id = 0
        for id in event_dict:
            max_id = id

        max_id += 1
    except:
        max_id = 1

    if request.method == 'POST' and create_single_form.validate():
        event_dict = {}
        db = shelve.open('event.db', 'c')
        try:
            event_dict = db['Events']

        except:
            print("Error in retrieving Single Event from single_event.db.")
        if create_single_form.validate_date_on_submit() and create_single_form.validate_title_on_submit() and create_single_form.validate_registration_on_submit():
            single_event = SingleEvent.SingleEvent(max_id, create_single_form.event_type, create_single_form.title.data, create_single_form.start_date.data, create_single_form.end_date.data, create_single_form.start_time.data, create_single_form.end_time.data, create_single_form.category.data, create_single_form.location.data, create_single_form.description.data, create_single_form.image.data, create_single_form.price.data, create_single_form.registration.data, create_single_form.pax.data)

            event_dict[single_event.get_event_id()] = single_event
            db['Events'] = event_dict

            db.close()
            return redirect(url_for('retrieve_events'))

        elif create_single_form.validate_date_on_submit() is False:
            date_error = "Start date must be greater than today's date and smaller than End date"

        elif create_single_form.validate_registration_on_submit() is False:
            pax_error = 'The pax is required'

        elif create_single_form.validate_title_on_submit() is False:
            title_error = 'The event title is already have been used'

        return render_template('createSingleEvent.html', form=create_single_form, date_error=date_error, pax_error=pax_error, title_error=title_error)

    return render_template('createSingleEvent.html', form=create_single_form)


@app.route('/createRecurringEvent', methods=['GET', 'POST'])
def create_recurring_event():
    create_recurring_form = CreateRecurringEvent(request.form)
    date_error = None
    pax_error = None
    title_error = None
    try:
        event_dict = {}
        db = shelve.open('event.db', 'r')
        event_dict = db['Events']
        db.close()

        max_id = 0
        for id in event_dict:
            max_id = id

        max_id += 1

    except:
        max_id = 1

    if request.method == 'POST' and create_recurring_form.validate():
        event_dict = {}
        db = shelve.open('event.db', 'c')
        try:
            event_dict = db['Events']

        except:
            print("Error in retrieving Recurring Event from event.db.")
        if create_recurring_form.validate_date_on_submit() and create_recurring_form.validate_registration_on_submit() and create_recurring_form.validate_title_on_submit():
            recurring_event = RecurringEvent.RecurringEvent(max_id, create_recurring_form.event_type, create_recurring_form.title.data, create_recurring_form.start_date.data, create_recurring_form.end_date.data,create_recurring_form.start_time.data, create_recurring_form.end_time.data, create_recurring_form.category.data, create_recurring_form.location.data, create_recurring_form.description.data, create_recurring_form.image.data, create_recurring_form.price.data, create_recurring_form.registration.data, create_recurring_form.pax.data, create_recurring_form.occurrence.data)

            event_dict[recurring_event.get_event_id()] = recurring_event
            db['Events'] = event_dict

            db.close()

            return redirect(url_for('retrieve_events'))
        elif create_recurring_form.validate_date_on_submit() is False:
            date_error = "Start date must be greater than today's date and smaller than End date"

        elif create_recurring_form.validate_registration_on_submit() is False:
            pax_error = 'The pax is required'

        elif create_recurring_form.validate_title_on_submit() is False:
            title_error = 'The event title is already have been used'

        return render_template('createRecurringEvent.html', form=create_recurring_form, date_error=date_error, pax_error=pax_error, title_error=title_error)

    return render_template('createRecurringEvent.html', form=create_recurring_form)


@app.route('/retrieveEvent')
def retrieve_events():
    try:
        event_dict = {}
        db = shelve.open('event.db', 'r')
        event_dict = db['Events']
        db.close()
        try:
            attendance_dict = {}
            db = shelve.open('attendance.db', 'r')
            attendance_dict = db['Attendance']
            db.close()

        except:
            attendance_dict = {}

        date = datetime.date.today()
        events_list = []
        upcoming_events_list = []
        past_events_list = []
        attendance_list = []
        attending_dict = {}
        event_id_list = []
        # For Visualization
        title_list = []
        attend_list = []
        total_pax = []

        for key in event_dict:
            event = event_dict.get(key)
            events_list.append(event)
            if event.get_start_date() > date:
                upcoming_events_list.append(event)
            elif event.get_event_type() == "Recurring Event":
                upcoming_events_list.append(event)
            else:
                past_events_list.append(event)

            if event.get_registration() == "Y":
                pax = event.get_pax()
                item = event.get_title()
                title_list.append(item)
                attend = 0
                for key in attendance_dict:
                    attendance = attendance_dict.get(key)
                    event_id = attendance.get_event_id()
                    event_id_list.append(event_id)
                    attendance_list.append(attendance)
                    if attendance.get_event_id() == event.get_event_id():
                        attend += attendance.get_attending_pax()
                        attending_dict[attendance.get_event_id()] = attend

                attend_list.append(attend)

                if event.get_event_id() not in event_id_list:
                    attending_dict[event.get_event_id()] = 0
                total = int(pax) - int(attend)
                total_pax.append(total)
        plot = px.Figure(data=[
            go.Bar(
                name='Registered',
                x=title_list,
                y=attend_list),
            go.Bar(
                name='Remaining',
                x=title_list,
                y=total_pax)
        ])

        plot.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', barmode='stack')
        graphJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('retrieveEvents.html', count=len(events_list), upcoming_events_list=upcoming_events_list, past_events_list=past_events_list, attending_dict=attending_dict, graphJSON=graphJSON)
    except:
        event_id = []
        plot = px.Figure(data=[
            go.Bar(
                name='Registered',
                x=event_id,
                y=[]),
            go.Bar(
                name='Remaining',
                x=event_id,
                y=[])
        ])

        plot.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', barmode='stack')
        graphJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('retrieveEvents.html', count=0, graphJSON=graphJSON)


@app.route('/updateEvent/<int:id>/', methods=['GET', 'POST'])
def update_event(id):
    try:
        update_event_form = CreateRecurringEvent(request.form)
        date_error = None
        pax_error = None
        title_error = None
        attend_error = None
        if request.method == 'POST' and update_event_form.validate():
            event_dict = {}
            db = shelve.open('event.db', 'w')
            event_dict = db['Events']

            event = event_dict.get(id)
            event.set_title(update_event_form.title.data)
            event.set_start_date(update_event_form.start_date.data)
            event.set_end_date(update_event_form.end_date.data)
            event.set_start_time(update_event_form.start_time.data)
            event.set_end_time(update_event_form.end_time.data)
            event.set_category(update_event_form.category.data)
            event.set_location(update_event_form.location.data)
            event.set_description(update_event_form.description.data)
            event.set_image(update_event_form.image.data)
            event.set_price(update_event_form.price.data)
            event.set_registration(update_event_form.registration.data)
            event.set_pax(update_event_form.pax.data)
            event.set_occurrence(update_event_form.occurrence.data)
            if update_event_form.validate_date_on_submit() and update_event_form.validate_registration_on_submit() and update_event_form.validate_title_update() and update_event_form.validate_pax_update(id):
                db['Events'] = event_dict
                db.close()

            elif update_event_form.validate_date_on_submit() is False:
                date_error = "Start date must be greater than today's date and smaller than End date"
                return render_template('updateRecurringEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            elif update_event_form.validate_registration_on_submit() is False:
                pax_error = 'The pax is required'
                return render_template('updateRecurringEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            elif update_event_form.validate_title_update() is False:
                title_error = 'The event title is already have been used'
                return render_template('updateRecurringEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            elif update_event_form.validate_pax_update(id) is False:
                attend_error = 'The total number of pax must be greater than attendance'
                return render_template('updateRecurringEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            return redirect(url_for('retrieve_events'))

        else:
            event_dict = {}
            db = shelve.open('event.db', 'w')
            event_dict = db['Events']
            db.close()

            event = event_dict.get(id)
            update_event_form.title.data = event.get_title()
            update_event_form.start_date.data = event.get_start_date()
            update_event_form.end_date.data = event.get_end_date()
            update_event_form.start_time.data = event.get_start_time()
            update_event_form.end_time.data = event.get_end_time()
            update_event_form.category.data = event.get_category()
            update_event_form.location.data = event.get_location()
            update_event_form.description.data = event.get_description()
            update_event_form.image.data = event.get_image()
            update_event_form.price.data = event.get_price()
            update_event_form.registration.data = event.get_registration()
            update_event_form.pax.data = event.get_pax()
            update_event_form.occurrence.data = event.get_occurrence()

            return render_template('updateRecurringEvent.html', form=update_event_form)

    except:
        update_event_form = CreateSingleEvent(request.form)
        date_error = None
        pax_error = None
        title_error = None
        attend_error = None
        if request.method == 'POST' and update_event_form.validate():
            event_dict = {}
            db = shelve.open('event.db', 'w')
            event_dict = db['Events']

            event = event_dict.get(id)
            event.set_title(update_event_form.title.data)
            event.set_start_date(update_event_form.start_date.data)
            event.set_end_date(update_event_form.end_date.data)
            event.set_start_time(update_event_form.start_time.data)
            event.set_end_time(update_event_form.end_time.data)
            event.set_category(update_event_form.category.data)
            event.set_location(update_event_form.location.data)
            event.set_description(update_event_form.description.data)
            event.set_image(update_event_form.image.data)
            event.set_price(update_event_form.price.data)
            event.set_registration(update_event_form.registration.data)
            event.set_pax(update_event_form.pax.data)
            if update_event_form.validate_date_on_submit() and update_event_form.validate_registration_on_submit() and update_event_form.validate_title_update() and update_event_form.validate_pax_update(id):
                db['Events'] = event_dict
                db.close()

            elif update_event_form.validate_title_update() is False:
                title_error = 'The event title is already have been used'
                return render_template('updateSingleEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            elif update_event_form.validate_date_on_submit() is False:
                date_error = "Start date must be greater than today's date and smaller than End date"
                return render_template('updateSingleEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            elif update_event_form.validate_registration_on_submit() is False:
                pax_error = 'The pax is required'
                return render_template('updateSingleEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            elif update_event_form.validate_pax_update(id) is False:
                attend_error = 'The total number of pax must be greater than attendance'
                return render_template('updateSingleEvent.html', form=update_event_form, date_error=date_error, pax_error=pax_error, title_error=title_error, attend_error=attend_error)

            return redirect(url_for('retrieve_events'))

        else:
            event_dict = {}
            db = shelve.open('event.db', 'w')
            event_dict = db['Events']
            db.close()

            event = event_dict.get(id)
            update_event_form.title.data = event.get_title()
            update_event_form.start_date.data = event.get_start_date()
            update_event_form.end_date.data = event.get_end_date()
            update_event_form.start_time.data = event.get_start_time()
            update_event_form.end_time.data = event.get_end_time()
            update_event_form.category.data = event.get_category()
            update_event_form.location.data = event.get_location()
            update_event_form.description.data = event.get_description()
            update_event_form.image.data = event.get_image()
            update_event_form.price.data = event.get_price()
            update_event_form.registration.data = event.get_registration()
            update_event_form.pax.data = event.get_pax()

            return render_template('updateSingleEvent.html', form=update_event_form)


@app.route('/eventData/<int:id>/', methods=['GET', 'POST'])
def get_data(id):
    event_dict = {}
    db = shelve.open('event.db', 'r')
    event_dict = db['Events']
    db.close()
    try:
        attendance_dict = {}
        db = shelve.open('attendance.db', 'r')
        attendance_dict = db['Attendance']
        db.close()

    except:
        attendance_dict = {}

    event_list = []
    attendance_list = []
    if id in event_dict:
        event = event_dict.get(id)
        event_list.append(event)
    for key in attendance_dict:
        attend = attendance_dict.get(key)
        if attend.get_event_id() == event.get_event_id():
            attendance_list.append(attend)
    return render_template('eventData.html', event_list=event_list, attendance_list=attendance_list)


@app.route("/Export/<int:id>/", methods=['GET'])
def export_records(id):
    event_dict = {}
    db = shelve.open('event.db', 'r')
    event_dict = db['Events']
    db.close()
    try:
        attendance_dict = {}
        db = shelve.open('attendance.db', 'r')
        attendance_dict = db['Attendance']
        db.close()

    except:
        attendance_dict = {}

    event_list = []
    attendance_list = []
    if id in event_dict:
        event = event_dict.get(id)
        event_list.append(event)
    for key in attendance_dict:
        attend = attendance_dict.get(key)
        if attend.get_event_id() == event.get_event_id():
            attendance_list.append(attend)

    data = {'Booking ID': [],
            'Customer ID': [],
            'Number of Attending Pax': []}

    for attend in attendance_list:
        id = attend.get_id()
        data['Booking ID'].append(id)
        user_id = attend.get_session_user()
        data['Customer ID'].append(user_id)
        attending = attend.get_attending_pax()
        data['Number of Attending Pax'].append(attending)

    event_id = "Event " + str(event.get_event_id())
    return excel.make_response_from_dict(data, 'csv', file_name=event_id)


#Customer
@app.route('/customerEvent')
def customer_event():
    session['loginUser'] = 1
    try:
        event_dict = {}
        db = shelve.open('event.db', 'r')
        event_dict = db['Events']
        db.close()
        try:
            attendance_dict = {}
            db = shelve.open('attendance.db', 'r')
            attendance_dict = db['Attendance']
            db.close()

        except:
            attendance_dict = {}

        date = datetime.date.today()
        events_list = []
        upcoming_events_list = []
        past_events_list = []

        event_id_list = []
        attending_dict = {}
        for key in event_dict:
            event = event_dict.get(key)
            events_list.append(event)
            if event.get_start_date() > date:
                upcoming_events_list.append(event)
            elif event.get_event_type() == "Recurring Event":
                upcoming_events_list.append(event)

            else:
                past_events_list.append(event)

            if event.get_registration() == "Y":
                pax = event.get_pax()
                attend = 0
                for key in attendance_dict:
                    attendance = attendance_dict.get(key)
                    event_id = attendance.get_event_id()
                    event_id_list.append(event_id)
                    if attendance.get_event_id() == event.get_event_id():
                        attend += attendance.get_attending_pax()
                        attending_dict[attendance.get_event_id()] = attend

                if event.get_event_id() not in event_id_list:
                    attending_dict[event.get_event_id()] = 0

        return render_template('customerEvent.html', count=len(events_list), upcoming_events_list=upcoming_events_list, past_events_list=past_events_list, attending_dict=attending_dict)
    except:
        return render_template('customerEvent.html')


@app.route('/displayEvent/<int:id>/', methods=['GET', 'POST'])
def display_event(id):
    event_dict = {}
    db = shelve.open('event.db', 'r')
    event_dict = db['Events']
    db.close()

    events_list = []
    if id in event_dict:
        event = event_dict.get(id)
        events_list.append(event)

    return render_template('displayEvent.html', events_list=events_list)


@app.route('/registration/<int:id>/', methods=['GET', 'POST'])
def registration(id):
    event_dict = {}
    db = shelve.open('event.db', 'r')
    event_dict = db['Events']
    db.close()

    events_list = []
    if id in event_dict:
        event = event_dict.get(id)
        events_list.append(event)
    try:
        attendance_dict = {}
        db = shelve.open('attendance.db', 'r')
        attendance_dict = db['Attendance']
        db.close()

        max_id = 0
        for id in attendance_dict:
            max_id = id
        max_id += 1

    except:
        max_id = 1
    create_attendance_form = CreateAttendance(request.form)
    if request.method == 'POST' and create_attendance_form.validate():
        attendance_dict = {}
        db = shelve.open('attendance.db', 'c')
        try:
            attendance_dict = db['Attendance']

        except:
            print("Error in retrieving Attendance from attendance.db.")
        if create_attendance_form.validate_user_on_submit(event.get_event_id()):
            attendance = Attendance.Attendance(max_id, event.get_event_id(), session.get('loginUser'), create_attendance_form.attendance.data)

            attendance_dict[attendance.get_id()] = attendance
            db['Attendance'] = attendance_dict

            db.close()
            return redirect(url_for('customer_event'))
        else:
            error = 'You have already registered for this event'
            return render_template('Registration.html', form=create_attendance_form, count=len(events_list), events_list=events_list, error=error)
    return render_template('Registration.html', form=create_attendance_form, count=len(events_list), events_list=events_list)


@app.route('/userRegisteredEvent')
def registered_event():
    try:
        attendance_dict = {}
        db = shelve.open('attendance.db', 'r')
        attendance_dict = db['Attendance']
        db.close()

        event_dict = {}
        db = shelve.open('event.db', 'r')
        event_dict = db['Events']
        db.close()

        date = datetime.date.today()
        upcoming_events_list = []
        past_events_list = []
        attend_list = []
        for key in event_dict:
            event = event_dict.get(key)
            for items in attendance_dict:
                attendance = attendance_dict.get(items)
                attend_list.append(attendance)
                if attendance.get_session_user() == session.get('loginUser'):
                    if attendance.get_event_id() == event.get_event_id():
                        if event.get_start_date() > date:
                            upcoming_events_list.append(event)
                        else:
                            past_events_list.append(event)
        return render_template('userRegisteredEvent.html', upcoming_events_list=upcoming_events_list, past_events_list=past_events_list, attend_list=attend_list)
    except:
        return render_template('userRegisteredEvent.html')


@app.route('/deleteRegisteredEvent/<int:id>/', methods=['POST'])
def delete_registered_event(id):
    view_dict = {}
    db = shelve.open('attendance.db', 'r')
    view_dict = db['Attendance']
    db.close()

    attendance_dict = {}
    db = shelve.open('attendance.db', 'w')
    attendance_dict = db['Attendance']

    for key in view_dict:
        attend = view_dict.get(key)
        if id == attend.get_event_id():
            username = attend.get_id()
            attendance_dict.pop(username)
            break

    db['Attendance'] = attendance_dict
    db.close()

    return redirect(url_for('registered_event'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    excel.init_excel(app)
    app.run()
