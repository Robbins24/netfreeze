from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from jinja2 import Template
from netmiko import Netmiko                                                                                                                    
from getpass import getpass                                                                                                                    

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(50))
    config = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)
    # python 3 - from app import db - db.create_all()
                                                                                                                                             
cisco1 = {                                                                                                                                     
    "host": "10.0.1.170",                                                                                                                      
    "username": "cisco",                                                                                                                       
    "password": "cisco",                                                                                                                     
    "device_type": "cisco_ios",                                                                                                                
}                                                                                                                                              

@app.route('/')
def index():
    #return render_template('index.html')
    return ("<html><head><title>Config</title></head><body><h1>Network Configuration Backup Tool</h1></body></html>")

@app.route('/backup')
def backup():
    net_connect = Netmiko(**cisco1)                                                                                                                
    command = "show run"                                                                                                                           

    #print(net_connect.find_prompt())                                                                                                               
    output = net_connect.send_command(command)
    confvar = output
    net_connect.disconnect()
    conf = Config(device="CiscoIOS", config=confvar)
    db.session.add(conf)
    db.session.commit()
    #return render_template('index.html')
    return ("<html><head><title>Config</title></head><body><pre>Configuration has been saved to the database.</pre></body></html>")

@app.route('/configs')
def getconf():
    conf = Config.query.all()
    return render_template('backup/configs.html', conf=conf)
    for item in conf:
        print (f'<h1>Configuration backup: { item.date_created } </h1>')

@app.route('/config/<id>')
def fullconf(id):
    conf = Config.query.filter_by(id=id).first()
    return render_template('backup/config-full.html', conf=conf)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
 
 
