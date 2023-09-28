from flask_app import app
from flask import redirect, request,session, render_template
from flask_app.models.appointment import Appointment
from flask_app.models.user import User


@app.route('/process_appointment', methods=['POST'])
def process_appointment():
    data = {
        "task": request.form['task'],
        "date": request.form['date'],
        "status": request.form['status'],
        "user_id": session['user_id']
    }
    Appointment.save(data)
    
    return redirect('/appointments')

@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('appointment.html', user=User.get_user_by_id(data), all_appointments = Appointment.get_all_appointments_with_users(), appointments= Appointment.get_appointments())


@app.route('/appointments/add')
def new_appointment():
    return render_template('appointment_form.html')


#create edit appointment form
@app.route('/appointments/<int:appointment_id>')
def edit_appointment(appointment_id):
    data={
        'id': appointment_id
    }
    return render_template('edit_appointment.html', details = Appointment.get_one_appointment(data))

# process appointment update
@app.route('/process_update', methods=['POST'])
def process_update():
    data ={
        'id': request.form['id'],
        "task":request.form['task'],
        "date": request.form['date'],
        "status": request.form['status']
    }
    Appointment.update_appointment(data)
    return redirect('/appointments')

# details of a specific appointment
@app.route('/appointments/destroy/<int:appointment_id>')
def destroy_appointment(appointment_id):
    data ={
        'id': appointment_id
    }
    Appointment.destroy_appointment(data)
    return redirect('/appointments')


