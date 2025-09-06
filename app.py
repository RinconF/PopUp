from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.auth import login, get_user_name

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura'

@app.route('/')
def index():
    return redirect(url_for('login_view'))

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        print(f"Intentando login con usuario: {username}, password: {password}")  # Debug
        
        if login(username, password):
            session['username'] = username
            session['user_fullname'] = get_user_name(username)
            print(f"Login exitoso para: {username}")  # Debug
            return redirect(url_for('welcome'))
        else:
            print(f"Login fallido para: {username}")  # Debug
            flash('Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login_view'))
    return render_template('dashboard.html', 
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
    session.pop('user_fullname', None)
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('login_view'))

if __name__ == '__main__':
    app.run(debug=True)