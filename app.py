from flask import Flask, redirect, url_for, request
from flask_login import LoginManager
from models import db, Usuario
from usuarios.routes import usuarios_bp
from pacientes.routes import pacientes_bp
from cardapios.routes import cardapios_bp
from sistema.routes import sistema_bp
from flask_migrate import Migrate

from lucide.jinja import lucide as lucide_icon

app = Flask(__name__)

app.config["SECRET_KEY"] = "chave-super-secreta-do-junior"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///consultorio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.jinja_env.globals.update(lucide=lucide_icon)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

# Configuração de redirecionamento do gerenciador de acessos
login_manager.login_view = "usuarios.login"


# --- TRATAMENTO PROFISSIONAL E SILENCIOSO PARA QUEM NÃO ESTÁ LOGADO ---
@login_manager.unauthorized_handler
def tratar_acesso_nao_autorizado():
    if request.path == "/":
        return redirect(url_for("usuarios.login"))

    from flask import flash

    flash("Acesso restrito. Por favor, faça o login para continuar.", "info")
    return redirect(url_for("usuarios.login"))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


# Registro do Blueprint de usuários
app.register_blueprint(usuarios_bp)

# Registro do Blueprint de pacientes
app.register_blueprint(pacientes_bp)

# Registro do Blueprint de cardapios
app.register_blueprint(cardapios_bp)

# Registro do Blueprint de sistema
app.register_blueprint(sistema_bp)


if __name__ == '__main__':
    app.run(debug=True)