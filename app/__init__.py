from flask import Flask

def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

    from .routes import main  # Importa as rotas
    app.register_blueprint(main)  # Registra o blueprint 'main'

    return app
