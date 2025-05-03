from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, UserMixin, logout_user, login_user # Adicione aqui
from extensions import db
from models import User

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            # Implementação do registro
            pass
        return render_template('register.html')
    
    @app.route('/dashboard')
    @login_required  # Requer autenticação
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/mapa')
    def map():
        return render_template('map.html')

    @app.route('/impacto')
    def impact():
        return render_template('impact.html')

    @app.route('/notificacoes')
    def notifications():
        return render_template('notifications.html')
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Busca o usuário no banco de dados (note o uso de User, não user)
            user_obj = User.query.filter_by(username=username).first()
            
            if user_obj and user_obj.check_password(password):
                login_user(user_obj)  # Agora usando a variável definida (user_obj)
                return redirect(url_for('dashboard'))
            
            flash('Usuário ou senha inválidos')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))