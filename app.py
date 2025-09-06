from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.auth import login, get_user_name

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def index():
    return redirect(url_for('login_view'))

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            session['username'] = username
            # Determinar el nombre para mostrar
            if username == 'admin':
                session['user_fullname'] = 'Administrador'
            elif username == '12345678':
                session['user_fullname'] = 'Juan Pérez'
            elif username == '87654321':
                session['user_fullname'] = 'María García'
            elif username == '11111111':
                session['user_fullname'] = 'Carlos López'
            elif username == '22222222':
                session['user_fullname'] = 'Ana Rodríguez'
            else:
                session['user_fullname'] = username
            return redirect(url_for('welcome'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login_view'))
    return render_template('welcome_popup.html', 
                         username=session.get('user_fullname', session['username']))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_view'))
    return render_template('dashboard.html', 
                         username=session.get('user_fullname', session['username']))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_view'))

if __name__ == '__main__':
    app.run(debug=True)