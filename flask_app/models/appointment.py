from flask_app.config.mysqlconnexion import connectToMySQL
from flask_app.models import user

class Appointment:
    def __init__(self,data):
        self.id = data['id']
        self.task= data['task']
        self.date = data['date']
        self.status = data['status']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # user information
        self.user = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO appointments (task, date, status, user_id, created_at, updated_at) VALUES (%(task)s,%(date)s, %(status)s, %(user_id)s, NOW(),NOW());"
        return connectToMySQL('user_appointments').query_db(query,data)
    
    @classmethod
    def get_all_appointments(cls):
        query = "SELECT * FROM appointments;"
        appointments_from_db =  connectToMySQL('user_appointments').query_db(query)
        appointments =[]
        for a in appointments_from_db:
            appointments.append(cls(a))
        return appointments
    
    # for the join
    @classmethod
    def get_all_appointments_with_users(cls):
        query = "SELECT appointments.id, task, date, status, user_id, appointments.created_at, appointments.updated_at, first_name, last_name, email, password, users.created_at AS user_created_at, users.updated_at AS user_updated_at FROM appointments JOIN users ON appointments.user_id = users.id;"

        # Get all appointments alongside their creator's info
        appointments_from_db =  connectToMySQL('user_appointments').query_db(query)
        appointments =[]

        for appointment in appointments_from_db:
            appointment_obj = cls(appointment)

            appointment_obj.user = user.User({
                'id': appointment['user_id'],
                'first_name': appointment['first_name'],
                'last_name': appointment['last_name'],
                'email': appointment['email'],
                'password': appointment['password'],
                'created_at': appointment['user_updated_at'],
                'updated_at': appointment['user_updated_at']
            })
        


            # convert each appointment into appointment  object
            appointments.append(appointment_obj)
            # return a appointment list with creator info
        return appointments


    
# get one appointment from the table
    @classmethod
    def get_one_appointment(cls,data):
        query = "SELECT * FROM appointments WHERE appointments.id = %(id)s;"
        appointment_from_db = connectToMySQL('user_appointments').query_db(query,data)

        return cls(appointment_from_db[0])

# update appointment
    @classmethod
    def update_appointment(cls,data):
        query = "UPDATE appointments SET task=%(task)s, date=%(date)s, status=%(status)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('user_appointments').query_db(query,data)


# destroy appointment
    @classmethod
    def destroy_appointment(cls,data):
        query = "DELETE FROM appointments WHERE id = %(id)s;"
        return connectToMySQL('user_appointments').query_db(query,data)
 
    @classmethod
    def get_appointments(cls):
        query = "SELECT * FROM appointments WHERE date > '2023-01-02';"
        appointments_from_db =  connectToMySQL('user_appointments').query_db(query)
        appointments =[]

        for appointment in appointments_from_db:
            appointment_obj = cls(appointment)
            # convert each appointment into appointment  object
            appointments.append(appointment_obj)
            # return a appointment list with creator info
        return appointments