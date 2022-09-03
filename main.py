from flask import Flask, redirect, render_template, request, session, url_for
from deta import Deta


app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True

# CREATE DB
deta = Deta()
form_db = deta.Base('form_submissions')
# KEY NAME = nm8cui
# PROJECT KEY = a07a51xw_KKtv7CTeqx36pq1GohkzuQSyhhRWy9ov


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


@app.route('/forms')
def forms():
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


# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         if request.form['username'] == 'ttbb' and request.form['password'] == 'p@$s|v/ord':
#             session['logged_in'] = True
#             return redirect(url_for('forms'))
#         else:
#             return render_template('login.html')
#     else:
#         return redirect(url_for('index'))
#
# @app.route("/logout")
# def logout():
#     session['logged_in'] = False
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
