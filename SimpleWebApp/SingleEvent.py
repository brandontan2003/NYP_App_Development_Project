class SingleEvent:
    def __init__(self, id, event_type, title, start_date, end_date, start_time, end_time, category, location, description, image, price, registration, pax):
        self.__single_id = id
        self.__event_type = event_type
        self.__title = title
        self.__start_date = start_date
        self.__end_date = end_date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__category = category
        self.__location = location
        self.__description = description
        self.__image = image
        self.__price = price
        self.__registration = registration
        self.__pax = pax

    def set_title(self, title):
        self.__title = title

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def set_start_time(self, start_time):
        self.__start_time = start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time

    def set_category(self, category):
        self.__category = category

    def set_location(self, location):
        self.__location = location

    def set_description(self, description):
        self.__description = description

    def set_image(self, image):
        self.__image = image

    def set_price(self, price):
        self.__price = price

    def set_registration(self, registration):
        self.__registration = registration

    def set_pax(self, pax):
        self.__pax = pax

    def get_title(self):
        return self.__title

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_category(self):
        return self.__category

    def get_location(self):
        return self.__location

    def get_description(self):
        return self.__description

    def get_image(self):
        return self.__image

    def get_price(self):
        return self.__price

    def get_registration(self):
        return self.__registration

    def get_pax(self):
        return self.__pax

    def get_event_id(self):
        return self.__single_id

    def get_event_type(self):
        return self.__event_type

