# importing libraries   
from flask import Flask, request, abort
from flask_mail import Mail, Message 
from flask_cors import CORS
   
app = Flask(__name__) 
mail = Mail(app) # instantiate the mail class 
# adding cors config
app.config['CORS_HEADERS'] = 'Content-Type'
# we can set origins => * but this isn't recommended
cors = CORS(app, resources={r"/sendEmail": {"origins": "your_path"}})
   
# configuration of mail 
# hotmail, outlook => smtp.office365.com
# gmail => smtp.gmail.com
app.config['MAIL_SERVER']='my.smtp.com'
app.config['MAIL_USERNAME'] = 'myemail@domain.com'
app.config['MAIL_PASSWORD'] = 'mypassword'
# if you use gmail MAIL_PORT => 465
# if you use hotmail, outlook MAIL_PORT => 587
app.config['MAIL_PORT'] = 587
# if you use gmail MAIL_USE_TLS => False
# if you use hotmail, outlook MAIL_USE_TLS => True
app.config['MAIL_USE_TLS'] = False
# if you use gmail MAIL_USE_SSL => True
# if you use hotmail, outlook MAIL_USE_SSL => False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

# message object mapped to a particular URL ‘/’ 
@app.route('/')
def index():
    return 'Running...'

@app.route('/sendEmail', methods=['POST']) 
@cross_origin(origin='ftinoco.github.io',headers=['Content-Type','Authorization'])
def send_email(): 
    if not request.json or not 'name' in request.json:
        abort(400)
    # getting request object    
    json = request.json
    message = json.get('message')
    _replyto =json.get('_replyto')
    subject = json.get('Subject')
    name = json.get('name')
    # building mail
    msg = Message(subject, 
                sender=(name, 'senderemail@domain.com'), 
                recipients = ['recipient@domain.com']) 
    msg.html = f'<p>Hello yourname, my name is {name}</p><br/>'\
               f'<p>{message}</p><br/>'\
               f'<p>If you want to contact me, please email me at {_replyto}</p><br/>'\
               f'<small>This mail has been sent from the portfolio site</small>'
    # sending
    mail.send(msg) 
    return 'Sent'
   
if __name__ == '__main__': 
    app.run(debug = True) 