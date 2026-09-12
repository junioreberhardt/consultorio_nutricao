from flask import render_template, request, url_for
from flask_login import current_user, login_required

from . import sistema_bp
from models import db, Usuario, Paciente


@sistema_bp.route('/')
def home():
    if current_user.is_authenticated:
        total_pacientes = Paciente.query.count()
        total_funcionarios = Usuario.query.filter_by(ativo=True).count()

        return render_template(
            'home/home.html',
            qtd_pacientes=total_pacientes,
            qtd_funcionarios=total_funcionarios
        )

    return redirect(url_for('usuarios.login'))


@sistema_bp.route("/atualizar/tema", methods=["POST"])
@login_required
def atualizar_tema():
    dados = request.get_json()
    novo_tema = dados.get("tema")

    if novo_tema in ["claro", "escuro"]:
        current_user.tema_preferido = novo_tema
        db.session.commit()
        return {"status": "sucesso", "tema": novo_tema}, 200

    return {"status": "erro", "mensagem": "Tema inválido"}, 400