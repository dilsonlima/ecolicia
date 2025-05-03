# app.py
from flask import Flask
from extensions import db
import models  # Import para registrar modelos
import os

def create_app():
    # Configuração do Flask
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-segura'  # Melhor prática para secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializações
    db.init_app(app)

    # Criação do banco de dados
    with app.app_context():
        db.create_all()

    # Registro de rotas
    from routes import init_routes
    init_routes(app)

    from flask_login import LoginManager, UserMixin, current_user, login_required

    # Adicione após criar a aplicação
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Nome da rota de login

    # Modelo User deve herdar de UserMixin
    class User(UserMixin, db.Model):
        # ... (seus campos existentes)
        
        def get_id(self):
            return str(self.id)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
       #Registro de notificacoes em tempo real
    from flask_sse import sse
    app.register_blueprint(sse, url_prefix='/stream')

    @app.route('/notifications-stream')
    def notification_stream():
        return sse.stream()

    return app

 
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001, host='0.0.0.0')  # host='0.0.0.0' permite acesso externo