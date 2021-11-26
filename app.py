#coding=utf-8
from flask_backend import create_app
from flask import render_template
from flask_socketio import send
from flask_backend.medicine_proc.medicine import MedicineApp
import json

app, socketio = create_app()
@app.route('/MedicineView')
def home_view():
    return render_template("MedicineView.html", caseNum='病歷號1228584')




@socketio.on('connect_event', namespace='/MedicineView')
def connected_msg(msg):
    data = json.loads(msg['data'])
    #medicine = Medicine() #progress
    #medicine.process()

@socketio.on('disconnect', namespace='/MedicineView')
def disconnec_msg():
    send('socketIO is disconnected')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port= 5000,
        debug=True
    )






