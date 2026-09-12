from flask import render_template, request
from flask_login import login_required, current_user

from . import cardapios_bp
from models import Paciente

@cardapios_bp.route("/montar/cardapio")
@login_required
def montar_cardapio():
    # 1. Trava de segurança por checkbox granular ou admin master
    if not current_user.eh_admin() and not current_user.pode_montar_cardapio:
        return (
            "<h1>Acesso Negado</h1><p>Seu perfil não possui permissão para criar cardápios.</p><a href='/'>Voltar</a>",
            403,
        )

    # 2. Captura o ID do paciente enviado pela barra de endereços (Ex: /montar/cardapio?paciente_id=1)
    paciente_id = request.args.get("paciente_id")
    paciente_selecionado = None

    if paciente_id:
        # O SQLAlchemy busca a ficha corporal do paciente direto no banco de dados pelo ID
        paciente_selecionado = Paciente.query.get(paciente_id)

    # 3. Renderiza o HTML passando o objeto do paciente encontrado para a tela clara
    return render_template("cardapios/cardapio.html", paciente=paciente_selecionado)
