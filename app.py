from urllib import request
from flask import Flask, render_template, jsonify
import subprocess

# Func import
from func.deviceInfoManager import mobileIdentification

app = Flask(__name__)

@app.route('/')
def index():

    # Check for mobile / Database

    return render_template('index.html')

@app.route('/component')
def component():
    return render_template('blank.html')

@app.route('/sms')
def sms():
    return render_template('sms.html')

@app.route("/contacts")
def contacts():
    return render_template('contacts.html')

@app.route('/medias')
def medias():
    return render_template('medias.html')

@app.route('/callhistory')
def callhistory():
    return render_template('call_history.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/applications')
def applications():
    return render_template('applications.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/safari')
def safari():
    return render_template('safari.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/recording')
def recording():
    return render_template('recording.html')


##############################
###### AJAX REQUEST #########
############################
@app.route('/check_device')
def check_device():
    connected = mobileIdentification()
    return jsonify({'connected': connected})

@app.route('/create_backup')
@app.route('/create_backup/<password>')
def create_backup(password=None):
    if not mobileIdentification():
        return jsonify({'error': 'No Mobile Identification'})
    # If everything is alright, create a backup
    try:
        result = create_backup(password)
        if result is True:
            return jsonify({'result': True})
        else :
            return jsonify({'result': False})

    except Exception as e:
        return jsonify({'error': str(e)})

# BIG SOLO ROUTE
@app.route('/getData/<focus>')
def get_data(focus):
    if not mobileIdentification():
        return jsonify({'error': 'No Mobile Identification'})

    # Try the only route
    # In the focus, it'll be Message, Contacts...
    # Need to organize the func
    action = focus+'Acquisition'
    action()
    # Like this

    pass

if __name__ == '__main__' :
    app.run(debug=True)