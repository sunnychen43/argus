from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import  create_session
from models import User, Vote
from defs import descriptions, topics
from forms import LoginForm, RegisterForm
import flask, os


# FLASK INIT
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12);



# LOGIN INIT
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return user_query.get(int(user_id))



# BOOTSTRAP INIT
bootstrap = Bootstrap(app)



# SQLALCHEMY INIT
user_db = create_engine("sqlite:///database.db")
metadata = MetaData(bind = user_db)
metadata.create_all()
session = create_session(bind=user_db, autocommit=False, autoflush=True)
user_query = session.query(User)
vote_query = session.query(Vote)



if __name__ == '__main__':
    from views import blueprint
    app.register_blueprint(blueprint)
    app.run(host='0.0.0.0')

    
    
    
    
    
    
    