from flask import session
from wtforms import Form, StringField, RadioField, DecimalField, SelectField, TextAreaField, validators
from wtforms.fields import DateField, TimeField, IntegerField, FileField
import datetime
import shelve

date = datetime.date.today()


class CreateEvent(Form):
    event = SelectField('Events', [validators.DataRequired()], choices=[('S', 'Single Event'), ('R', 'Recurring Event')], default='')


class CreateSingleEvent(Form):
    event_type = "Single Event"
    title = StringField('Title', [validators.length(min=1, max=150), validators.DataRequired()])
    start_date = DateField('Start Date', [validators.InputRequired()], default=datetime.date.today(), format='%Y-%m-%d')
    end_date = DateField('End Date', [validators.InputRequired()], default=datetime.date.today(), format='%Y-%m-%d')
    start_time = TimeField('Start Time', [validators.DataRequired()], format='%H:%M')
    end_time = TimeField('End Time', [validators.DataRequired()], format='%H:%M')
    category = SelectField('Category', [validators.DataRequired()], choices=[('S', 'Sales'), ('F', 'Fashion Show'), ('W', 'Workshop')], default='')
    location = StringField('Location', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    image = FileField('Image', [validators.DataRequired()])
    price = DecimalField('Price per Ticket', [validators.InputRequired()], places=2)
    registration = RadioField("Registration", [validators.DataRequired()], name='register', choices=[('Y', 'Required'), ('N', 'Not Required')])
    pax = IntegerField("Total Pax Available", [validators.Optional()])

    def validate_date_on_submit(self):
        result = super(CreateSingleEvent, self).validate()
        if self.start_date.data <= date or (self.start_date.data > self.end_date.data):
            return False
        else:
            return result

    def validate_registration_on_submit(self):
        registration = super(CreateSingleEvent, self).validate()
        if self.registration.data == "Y" and self.pax.data is None:
            return False
        elif self.registration.data == "N":
            return registration
        else:
            return registration

    def validate_title_on_submit(self):
        title = super(CreateSingleEvent, self).validate()
        try:
            check_dict = {}
            db = shelve.open('event.db', 'r')
            check_dict = db['Events']
            db.close()
        except:
            check_dict = {}
        title_list = []
        for key in check_dict:
            check = check_dict.get(key)
            title = check.get_title()
            title_list.append(title)
        if self.title.data in title_list:
            return False

        else:
            return title

    def validate_title_update(self):
        title = super(CreateSingleEvent, self).validate()
        check_dict = {}
        db = shelve.open('event.db', 'r')
        check_dict = db['Events']
        db.close()
        title_list = []
        for key in check_dict:
            check = check_dict.get(key)
            title = check.get_title()
            title_list.append(title)
        count = 0
        for item in title_list:
            if item == self.title.data:
                count += 1
        if count > 1:
            return False
        else:
            return title

    def validate_pax_update(self, id):
        pax = super(CreateSingleEvent, self).validate()
        try:
            attendance_dict = {}
            db = shelve.open('attendance.db', 'r')
            attendance_dict = db['Attendance']
            db.close()

        except:
            return pax

        check_dict = {}
        db = shelve.open('event.db', 'r')
        check_dict = db['Events']
        db.close()
        attending_dict = {}

        attendance_list = []
        attend = 0
        for key in attendance_dict:
            attendance = attendance_dict.get(key)
            event_id = attendance.get_event_id()
            attendance_list.append(event_id)
            if attendance.get_event_id() == id:
                attend += attendance.get_attending_pax()
                attending_dict[attendance.get_event_id()] = attend
        if id in attendance_list:
            number = attending_dict[id]
            if self.pax.data < number:
                return False

            else:
                return pax


class CreateRecurringEvent(Form):
    event_type = "Recurring Event"
    title = StringField('Title', [validators.length(min=1, max=150), validators.DataRequired()])
    start_date = DateField('Start Date', [validators.DataRequired()], default=datetime.date.today(), format='%Y-%m-%d')
    end_date = DateField('End Date', [validators.DataRequired()], default=datetime.date.today(), format='%Y-%m-%d')
    start_time = TimeField('Start Time', [validators.DataRequired()], format='%H:%M')
    end_time = TimeField('End Time', [validators.DataRequired()], format='%H:%M')
    occurrence = SelectField("Occurrence", [validators.DataRequired()], choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('A', 'Annually')])
    category = SelectField('Category', [validators.DataRequired()], choices=[('S', 'Sales'), ('F', 'Fashion Show'), ('W', 'Workshop')], default='')
    location = StringField('Location', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    image = FileField('Image', [validators.DataRequired()])
    price = DecimalField('Price per Ticket', [validators.InputRequired()], places=2)
    registration = RadioField("Registration", [validators.DataRequired()], name='register', choices=[('Y', 'Required'), ('N', 'Not Required')])
    pax = StringField("Total Pax Available", [validators.Optional()])

    def validate_date_on_submit(self):
        result = super(CreateRecurringEvent, self).validate()
        if self.start_date.data <= date or (self.start_date.data > self.end_date.data):
            return False
        else:
            return result

    def validate_registration_on_submit(self):
        registration = super(CreateRecurringEvent, self).validate()
        if self.registration.data == "Y" and self.pax.data is None:
            return False
        elif self.registration.data == "N":
            return registration
        else:
            return registration

    def validate_title_on_submit(self):
        title = super(CreateRecurringEvent, self).validate()
        try:
            check_dict = {}
            db = shelve.open('event.db', 'r')
            check_dict = db['Events']
            db.close()
        except:
            check_dict = {}
        title_list = []
        for key in check_dict:
            check = check_dict.get(key)
            title = check.get_title()
            title_list.append(title)
        if self.title.data in title_list:
            return False

        else:
            return title

    def validate_title_update(self):
        title = super(CreateRecurringEvent, self).validate()
        check_dict = {}
        db = shelve.open('event.db', 'r')
        check_dict = db['Events']
        db.close()
        title_list = []
        for key in check_dict:
            check = check_dict.get(key)
            title = check.get_title()
            title_list.append(title)
        count = 0
        for item in title_list:
            if item == self.title.data:
                count += 1
        if count > 1:
            return False
        else:
            return title

    def validate_pax_update(self, id):
        pax = super(CreateRecurringEvent, self).validate()
        try:
            attendance_dict = {}
            db = shelve.open('attendance.db', 'r')
            attendance_dict = db['Attendance']
            db.close()

        except:
            return pax

        check_dict = {}
        db = shelve.open('event.db', 'r')
        check_dict = db['Events']
        db.close()
        attending_dict = {}
        attendance = 0
        a_list = []
        for key in attendance_dict:
            attend = attendance_dict.get(key)
            attendance += attend.get_attending_pax()
            attending_dict[attend.get_event_id()] = attendance
            attend_id = attend.get_event_id()
            a_list.append(attend_id)

        if id in a_list:
            number = attending_dict[id]
            if self.pax.data < number:
                return False

            else:
                return pax


class CreateAttendance(Form):
    attendance = IntegerField("Number of Pax Attending", [validators.InputRequired(), validators.NumberRange(min=1, max=1)], default='1')

    def validate_user_on_submit(self, id):
        user = super(CreateAttendance, self).validate()
        try:
            attendance_dict = {}
            db = shelve.open('attendance.db', 'r')
            attendance_dict = db['Attendance']
            db.close()

        except:
            return user
        attend_list = []
        for items in attendance_dict:
            attendance = attendance_dict.get(items)
            if attendance.get_event_id() == id:
                attend = attendance.get_session_user()
                attend_list.append(attend)
        if session.get('loginUser') in attend_list:
            return False
        else:
            return user

