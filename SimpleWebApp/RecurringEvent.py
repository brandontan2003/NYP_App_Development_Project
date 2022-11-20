from SingleEvent import *


class RecurringEvent(SingleEvent):
    def __init__(self, id, event_type, title, start_date, end_date, start_time, end_time, category, location, description, image, price, registration, pax, occurrence):
        super().__init__(id, "Recurring Event", title, start_date, end_date, start_time, end_time,  category, location, description, image, price, registration, pax)
        self.__occurrence = occurrence

    def get_occurrence(self):
        return self.__occurrence

    def set_occurrence(self, occurrence):
        self.__occurrence = occurrence
