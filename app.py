from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from utils.auth import login, get_user_name
from datetime import datetime
import json
import os
import random

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

# NUEVAS RUTAS PARA EL POPUP MENSUAL
@app.route('/check_monthly_popup')
def check_monthly_popup():
    username = session.get('username')
    if not username:
        return jsonify({'show': False})
    
    # Verificar si ya se mostró este mes
    last_shown = get_last_popup_date(username)
    current_month = datetime.now().strftime('%Y-%m')
    
    if last_shown != current_month:
        # Generar estadística de puntualidad
        punctuality = generate_punctuality_stat()
        message = generate_motivational_message(punctuality)
        return jsonify({
            'show': True, 
            'punctuality': punctuality,
            'message': message
        })
    
    return jsonify({'show': False})

@app.route('/mark_popup_shown', methods=['POST'])
def mark_popup_shown():
    username = session.get('username')
    if username:
        save_popup_shown(username)
        return jsonify({'success': True})
    return jsonify({'success': False})

def get_last_popup_date(username):
    """Obtiene la última fecha en que se mostró el popup para este usuario"""
    file_path = 'popup_tracking.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get(username)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    return None

def save_popup_shown(username):
    """Guarda que el popup fue mostrado este mes para este usuario"""
    file_path = 'popup_tracking.json'
    data = {}
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}
    
    data[username] = datetime.now().strftime('%Y-%m')
    
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error guardando popup tracking: {e}")

def generate_punctuality_stat():
    """Genera un porcentaje de puntualidad realista"""
    # Generar entre 87% y 98% para mantener positividad
    return random.randint(87, 98)

def generate_motivational_message(punctuality):
    """Genera un mensaje motivacional basado en el porcentaje"""
    messages = [
        f"Gracias a empleados como tú, ETIB mantiene {punctuality}% de puntualidad",
        f"Tu compromiso ayuda a que ETIB tenga {punctuality}% de eficiencia operacional",
        f"¡Increíble! Juntos logramos {punctuality}% de puntualidad este mes",
        f"El {punctuality}% de puntualidad de ETIB es gracias a tu dedicación",
        f"Tu profesionalismo contribuye al {punctuality}% de excelencia en ETIB"
    ]
    return random.choice(messages)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_fullname', None)
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('login_view'))

if __name__ == '__main__':
    app.run(debug=True)