class Attendance:
    def __init__(self, id, event_id, session_user, attending_pax, ticket_id):
        self.__id = id
        self.__event_id = event_id
        self.__session_user = session_user
        self.__attending_pax = attending_pax
        self.__ticket_id = ticket_id

    def set_attending_pax(self, attending_pax):
        self.__attending_pax = attending_pax

    def get_attending_pax(self):
        return self.__attending_pax

    def get_event_id(self):
        return self.__event_id

    def get_session_user(self):
        return self.__session_user

    def get_id(self):
        return self.__id

    def get_ticket_id(self):
        return self.__ticket_id
