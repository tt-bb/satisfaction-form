from flask import Flask, redirect, render_template, request, session, url_for
from deta import Deta
import bcrypt
import os


app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = False
# Use to authorize us using session
app.secret_key = os.getenv('FLASK_KEY')

# CREATE DBS
deta = Deta()
form_db = deta.Base('form_submissions')
admins = deta.Base('admins')

# CREATE ADMINS
salt = os.getenv('SALT')
salt = salt.encode("utf-8")
admin_name = 'Tiffanie'
password = 'Agdl98jfsmpAq555'.encode('utf-8')
hashed = bcrypt.hashpw(password, salt)
hashed = str(hashed)
admins.put({'admin_name':admin_name, 'password': hashed})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # GET FORM FIELDS
        user_name = request.form['name']
        dealer_name = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']

        # PUT FORM IN DB
        form_db.put({'user_name':user_name, 'dealer_name':dealer_name, 'rating':rating, 'comments':comments})

        return render_template('submit.html')


# ASK ADMIN ACCESS
@app.route('/forms')
def forms():
    if not session.get('logged_in'):
        return render_template('login.html', message=None)
    else:
        # all_forms=[
        #     {
        #         'user_name': 'TTBB',
        #         'dealer_name': 'Benjamin',
        #         'rating': '10',
        #         'comments': 'Comment'
        #     }
        # ]
        forms_object = form_db.fetch()
        all_forms = forms_object.items
        return render_template('forms.html', forms=all_forms)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        admins_object = admins.fetch()
        all_admins = admins_object.items
        if request.form['username'] in all_admins:
            password = request.form['password']
            password_bytes = password.encode("utf-8")


            bcrypt.checkpw(password_bytes, )
            session['logged_in'] = True
            return redirect(url_for('forms'))
        else:
            message = 'Wrong username or password...'
            return render_template('login.html', message=message)
    else:
        return redirect(url_for('index'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
