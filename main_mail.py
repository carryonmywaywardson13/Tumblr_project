from threading import Thread
from flask_mail import Mail, Message

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/flask_app_db'

manager = Manager(app)
manager.add_command('db', MigrateCommand)
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
mail = Mail(app)

app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = '://root:pass@localhost/flask_app_db'
app.config['MAIL_SERVER'] = 'googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'varya123@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'varya123@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'password'  # введите пароль

manager = Manager(app)
manager.add_command('db', MigrateCommand)
db = SQLAlchemy(app)
mail = Mail(app)


@app.route('/contact/', methods=['get', 'post'])
def contact():
    # ...
    db.session.commit()

    msg = Message("Feedback", recipients=[app.config['MAIL_USERNAME']])
    msg.body = "You have received a new feedback from {} <{}>.".format(name, email)
    mail.send(msg)

    print("\nData received. Now redirecting ...")


def shell_context():
    import os, sys
    return dict(app=app, os=os, sys=sys)

manager.add_command("shell",  Shell(make_context=shell_context))

def async_send_mail(app, msg):
    with app.app_context():
	mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject,      sender=app.config['MAIL_DEFAULT_SENDER'],  recipients=[recipient])
    msg.html = render_template(template,  **kwargs)
    thr = Thread(target=async_send_mail,  args=[app,  msg])
    thr.start()
    return thr

@app.route('/')
def index():
    return render_template('index.html', name='Jerry')