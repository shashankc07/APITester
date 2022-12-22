import sqlite3 as sq
from flask import Flask, render_template, request, url_for, flash, redirect
from ApiTester import test_url, test_payload

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            user = request.form['user']
            password = request.form['pass']

            with sq.connect("test.db") as con:
                cur = con.cursor()
                check_password = cur.execute('SELECT password FROM Users WHERE user_id=?', (user,)).fetchone()[0]
                if check_password is None or check_password != password:
                    flash('Invalid Credentials !')
                    return redirect(url_for('index'))
                else:
                    if user == 'brftester':
                        return redirect(url_for('tester_page'))
                    elif user == 'brfadmin':
                        return redirect(url_for('admin_page'))

        except Exception as e:
            flash('Invalid Credentials !')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route("/Tester")
def tester_page():
    user = 'Tester'
    return render_template('TesterHome.html', user=user)


@app.route("/Admin")
def admin_page():
    user = 'Admin'
    return render_template('AdminHome.html', user=user)


@app.route("/<user>/<server_type>")
def server_type_dashboard(user, server_type):
    with sq.connect("test.db") as con:
        cur = con.cursor()
        rows = cur.execute('SELECT DISTINCT environment FROM Endpoints WHERE server_type=?', (server_type,)).fetchall()
    # server_type = "Realtime"
    if user == 'Tester':
        return render_template('Tester_ServerType.html', user=user, server_type=server_type, rows=rows)
    else:
        return render_template('Admin_ServerType.html', user=user, server_type=server_type, rows=rows)


@app.route("/<server_type>/AddUrl", methods=["POST", "GET"])
def add_url(server_type):
    if request.method == "POST":
        endpoint = request.form['endpoint']
        env = request.form['environment']
        with sq.connect("test.db") as con:
            cur = con.cursor()
            cur.execute('''INSERT INTO Endpoints (endpoint, server_type, environment)
            VALUES (?, ?, ?) ''', (endpoint, server_type, env))
            con.commit()
        flash("URL added successfully !", "success")
        return redirect(url_for('server_type_dashboard', user='Admin', server_type=server_type))

    return redirect(url_for('server_type_dashboard', user='Admin', server_type=server_type))


@app.route("/<user>/CustomTest", methods=["POST", "GET"])
def custom_test(user):
    if request.method == "POST":
        url = request.form['url']
        payload = request.form['payload']
        response = test_payload(url, payload)
        return render_template('CustomTest.html', user=user, response=response)
    else:
        return render_template('CustomTest.html', user=user)


@app.route("/<user>/<server_type>/<env>", methods=['POST', 'GET'])
def environment(user, server_type, env):
    with sq.connect("test.db") as con:
        cur = con.cursor()
        rows = cur.execute('''SELECT endpoint FROM Endpoints WHERE server_type=? AND environment=?''',
                            (server_type, env)).fetchall()
    if request.method == 'POST':
        flag = True
        for row in rows:
            if test_url(row[0]) > 300:
                flag = False
        if flag is True:
            flash("{}  Validated Successfully !".format(env), "success")
        else:
            flash("{}  Have some issues ! Reach out to BRF Team !".format(env), "error")
    if user == 'Tester':
        return redirect(url_for('server_type_dashboard', user=user, server_type=server_type))
    else:
        return render_template('Admin_environment.html', user=user, server_type=server_type, env=env, rows=rows)


@app.route('/<user>/<server_type>/<env>/run_test', methods=["POST", "GET"])
def run_test(user, server_type, env):
    if request.method == "POST":
        endpoint = request.form['endpoint']
        resp = test_url(endpoint)
        if resp < 300:
            flash("{} Validated Successfully !".format(endpoint), "success")
        else:
            flash("Oops ! something went wrong with {}!".format(endpoint), "error")
        return redirect(url_for('environment', user=user, server_type=server_type, env=env))
    else:
        return redirect(url_for('environment', user=user, server_type=server_type, env=env))


if __name__ == "__main__":
    app.run()
