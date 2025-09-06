# Base de datos simple de usuarios (en producción usarías una base de datos real)
USERS = {
    'admin': {'password': 'admin', 'name': 'Administrador'},
    '12345678': {'password': '12345', 'name': 'Juan Pérez'},
    '87654321': {'password': 'password', 'name': 'María García'},
    '11111111': {'password': '11111', 'name': 'Carlos López'},
    '22222222': {'password': '22222', 'name': 'Ana Rodríguez'},
}

def login(username, password):
    # Usuarios válidos con sus contraseñas
    valid_users = {
        'admin': 'admin',
        '12345678': '12345',
        '87654321': 'password',
        '11111111': '11111',
        '22222222': '22222'
    }
    
    return username in valid_users and valid_users[username] == password

def get_user_name(username):
    """
    Obtiene el nombre completo del usuario
    """
    user = USERS.get(username)
    if user:
        return user['name']
    return username