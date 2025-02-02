from flask import render_template, redirect, url_for, request, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Vote
from defs import descriptions, topics
from forms import LoginForm, RegisterForm
from server import login_manager, load_user, session, user_query, vote_query
import operator, interface


blueprint = Blueprint("app", __name__)

# VIEWS
@blueprint.route('/index.html')
@blueprint.route('/')
def index():
    print(interface.get_rand_bill_ids(vote_query, None, 10))
    return render_template('index.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = user_query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flask.flash('Logged in successfully.')
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        print("signed up")
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user = User()
        new_user.username=form.username.data
        new_user.email=form.email.data
        new_user.password=hashed_password

        session.add(new_user)
        session.commit()
        return render_template('login.html',form=form)
    else:
        print("error")

    return render_template('signup.html', form=form)


@blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@blueprint.route('/profile', methods = ['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        result = request.form
        return render_template("profile.html", result = result)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@blueprint.route('/bills', methods = ['POST', 'GET'])
def bills():
    MIN_QUESTIONS = 5

    data = request.form.get("data")
    arr = data.split(",")
    print(arr)

    topics_arr = []
    ids = []

    for i in range(9):
        if arr[i] is '':
            continue
        else:
            val = int(arr[i])

        topic = topics[i]
        ids += interface.get_rand_bill_ids(vote_query, topic, val)
        

    if (MIN_QUESTIONS-len(ids) > 0):
        diff = MIN_QUESTIONS-len(ids)
        ids += interface.get_rand_bill_ids(vote_query, None, diff)

    names = [interface.get_bill_name(vote_query, i) for i in ids]
    descriptions = [interface.get_bill_description(vote_query, i) for i in ids]
    topics_arr = [interface.get_bill_topic(vote_query, i) for i in ids]


    return render_template("bills.html", len=len(ids), names=names, descriptions=descriptions, topics = topics_arr, ids=ids)

@blueprint.route('/values')
def values():

    return render_template("values.html", len=9 ,titles=topics, descriptions=descriptions)

@blueprint.route('/senators')
def senators():
    return render_template("senators.html")

@blueprint.route('/results', methods = ['POST', 'GET'])
def results():

    # array of bill ids (integers)
    ids = request.form.get("bill_ids").split(",")
    # array of user answers (strings)
    answers = request.form.get("user_answers").split(",")
    
    with open("senators.txt", "r") as fp:
        senators = [name.rstrip() for name in fp.readlines()]
 

    mydict={}

    for i in range(len(ids)):
        userInput = answers[i];
        for senator in senators:
            v = vote_query.get(int(ids[i])) #returns voting record for all senators on that bill
            similarity = 0;
            if(v[senator] == userInput and userInput != None): #checking if they match and not null
                similarity += 1
            elif (v[senator] != userInput):
                similarity -= 1

            if (senator in mydict): #setting senator matching score
                mydict[senator] += similarity
            else:
                mydict[senator] = similarity

    sortedDict = sorted(mydict.items(), key=operator.itemgetter(1), reverse=True) 
    keys = []
    values = []
    for key, value in sortedDict:
        keys.append(key)
        values.append(value)

    return render_template('results.html', keys = keys, values = values, len = len(keys))