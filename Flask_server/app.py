#!/usr/bin/python3
from flask import Flask
from Bleuprints.auth import auth_bp
from Bleuprints.general import general
from Bleuprints.first_responder import first_responder
from Bleuprints.investigator import investigator
from Bleuprints.lawyer import lawyer
from flask_mail import Mail, Message

app = Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hidoussiabdou5@gmail.com'
app.config['MAIL_PASSWORD'] = 'gjkmthtnarzyijls'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = 'secret_key'
app.register_blueprint(auth_bp)
app.register_blueprint(general)

app.register_blueprint(first_responder)
app.register_blueprint(investigator)
app.register_blueprint(lawyer)



if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)