from flask import Flask, render_template, request, redirect, url_for, flash
from utils.auth import login

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def welcome():
    return render_template('welcome_popup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)