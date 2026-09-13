import unicodedata
from datetime import date, datetime

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from models import Anamnese, ConsultaAntropometrica, Paciente, db

from . import pacientes_bp


def usuario_pode_cadastrar_paciente():
    return current_user.eh_admin() or current_user.pode_cadastrar_paciente


def remover_acentos(texto):
    return "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )


# ==========================================================
# LISTAGEM DE PACIENTES
# ==========================================================
@pacientes_bp.route("/listar/pacientes", methods=["GET"])
@login_required
def listar_pacientes():
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return (
            "<h1>Acesso Negado</h1>"
            "<p>Seu perfil não tem permissão para visualizar pacientes.</p>",
            403,
        )

    busca = request.args.get("busca", "").strip()

    opcoes_por_pagina = {10, 20, 50, 100}

    try:
        por_pagina = int(request.args.get("por_pagina", 20))
    except (TypeError, ValueError):
        por_pagina = 20

    if por_pagina not in opcoes_por_pagina:
        por_pagina = 20

    try:
        pagina = int(request.args.get("pagina", 1))
    except (TypeError, ValueError):
        pagina = 1

    if pagina < 1:
        pagina = 1

    consulta = Paciente.query

    if busca:
        busca_normalizada = remover_acentos(busca).lower()
        nome_normalizado = func.lower(Paciente.nome)

        for acentuado, normal in [
            ("á", "a"),
            ("à", "a"),
            ("ã", "a"),
            ("â", "a"),
            ("ä", "a"),
            ("é", "e"),
            ("è", "e"),
            ("ê", "e"),
            ("ë", "e"),
            ("í", "i"),
            ("ì", "i"),
            ("î", "i"),
            ("ï", "i"),
            ("ó", "o"),
            ("ò", "o"),
            ("õ", "o"),
            ("ô", "o"),
            ("ö", "o"),
            ("ú", "u"),
            ("ù", "u"),
            ("û", "u"),
            ("ü", "u"),
            ("ç", "c"),
        ]:
            nome_normalizado = func.replace(
                nome_normalizado,
                acentuado,
                normal,
            )

        consulta = consulta.filter(nome_normalizado.like(f"%{busca_normalizada}%"))

    consulta = consulta.order_by(
        Paciente.nome.asc(),
        Paciente.id.asc(),
    )

    total_pacientes = consulta.count()

    total_paginas = max(
        1,
        (total_pacientes + por_pagina - 1) // por_pagina,
    )

    if pagina > total_paginas:
        pagina = total_paginas

    pacientes_do_banco = (
        consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
    )

    if total_pacientes == 0:
        inicio = 0
        fim = 0
    else:
        inicio = ((pagina - 1) * por_pagina) + 1
        fim = min(
            pagina * por_pagina,
            total_pacientes,
        )

    return render_template(
        "pacientes/pacientes.html",
        todos_pacientes=pacientes_do_banco,
        busca=busca,
        pagina=pagina,
        total_paginas=total_paginas,
        total_pacientes=total_pacientes,
        inicio=inicio,
        fim=fim,
        por_pagina=por_pagina,
    )


# ==========================================================
# NOVO PACIENTE — TELA
# ==========================================================
@pacientes_bp.route("/novo/paciente", methods=["GET"])
@login_required
def cadastrar_paciente_tela():
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return (
            "<h1>Acesso Negado</h1>"
            "<p>Seu perfil não tem permissão para cadastrar pacientes.</p>",
            403,
        )

    return render_template("pacientes/novo_paciente.html")


# ==========================================================
# NOVO PACIENTE — SALVAR
# ==========================================================
@pacientes_bp.route("/novo/paciente", methods=["POST"])
@login_required
def cadastrar_paciente_salvar():
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return "<h1>Acesso Negado</h1>", 403

    nome = request.form.get("nome", "").strip()
    data_nascimento_str = request.form.get(
        "data_nascimento",
        "",
    ).strip()
    genero = request.form.get("genero")
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip()

    try:
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))

        data_nascimento = datetime.strptime(
            data_nascimento_str,
            "%Y-%m-%d",
        ).date()

        hoje = date.today()

        if data_nascimento > hoje:
            return (
                "<h1>Data inválida</h1>"
                "<p>A data de nascimento não pode estar no futuro.</p>",
                400,
            )

        idade = (
            hoje.year
            - data_nascimento.year
            - (
                (hoje.month, hoje.day)
                < (
                    data_nascimento.month,
                    data_nascimento.day,
                )
            )
        )

        if idade < 0 or idade > 150:
            return (
                "<h1>Data inválida</h1>"
                "<p>Verifique a data de nascimento informada.</p>",
                400,
            )

        novo_paciente = Paciente(
            nome=nome,
            data_nascimento=data_nascimento,
            genero=genero,
            peso=peso,
            altura=altura,
            telefone=telefone or None,
            email=email or None,
        )

        db.session.add(novo_paciente)
        db.session.commit()

    except (TypeError, ValueError):
        db.session.rollback()

        return (
            "<h1>Dados inválidos</h1>"
            "<p>Verifique os dados informados e tente novamente.</p>",
            400,
        )

    return redirect(url_for("pacientes.listar_pacientes"))


# ==========================================================
# GERENCIAR PACIENTE
# ==========================================================
@pacientes_bp.route(
    "/gerenciar/paciente/<int:paciente_id>",
    methods=["GET"],
)
@login_required
def gerenciar_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    anamnese = Anamnese.query.filter_by(paciente_id=paciente.id).first()

    aba = request.args.get(
        "aba",
        "dados-gerais",
    )

    abas_validas = {
        "dados-gerais",
        "avaliacao-fisica",
        "dietas",
        "anamnese",
    }

    if aba not in abas_validas:
        aba = "dados-gerais"

    return render_template(
        "pacientes/gerenciar_paciente.html",
        paciente=paciente,
        anamnese=anamnese,
        aba_inicial=aba,
    )


# ==========================================================
# EDITAR DADOS GERAIS DO PRONTUÁRIO
# ==========================================================
@pacientes_bp.route(
    "/gerenciar/paciente/<int:paciente_id>/dados-gerais",
    methods=["POST"],
)
@login_required
def atualizar_dados_gerais(paciente_id):
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        flash(
            "Você não tem permissão para editar pacientes.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
            )
        )

    paciente = Paciente.query.get_or_404(paciente_id)

    nome = request.form.get(
        "nome",
        "",
    ).strip()

    data_nascimento_str = request.form.get(
        "data_nascimento",
        "",
    ).strip()

    genero = request.form.get("genero")

    telefone = request.form.get(
        "telefone",
        "",
    ).strip()

    email = request.form.get(
        "email",
        "",
    ).strip()

    if not nome:
        flash(
            "Informe o nome do paciente.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
            )
        )

    try:
        data_nascimento = datetime.strptime(
            data_nascimento_str,
            "%Y-%m-%d",
        ).date()

    except (TypeError, ValueError):
        flash(
            "Informe uma data de nascimento válida.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
            )
        )

    hoje = date.today()

    if data_nascimento > hoje:
        flash(
            "A data de nascimento não pode estar no futuro.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
            )
        )

    idade = (
        hoje.year
        - data_nascimento.year
        - (
            (hoje.month, hoje.day)
            < (
                data_nascimento.month,
                data_nascimento.day,
            )
        )
    )

    if idade < 0 or idade > 150:
        flash(
            "Verifique a data de nascimento informada.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
            )
        )

    if genero not in ["F", "M"]:
        flash(
            "Selecione o sexo do paciente.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
            )
        )

    try:
        paciente.nome = nome
        paciente.data_nascimento = data_nascimento
        paciente.genero = genero
        paciente.telefone = telefone or None
        paciente.email = email or None

        db.session.commit()

    except Exception:
        db.session.rollback()

        flash(
            "Não foi possível salvar os dados do paciente.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
            )
        )

    flash(
        "Dados atualizados com sucesso.",
        "success",
    )

    return redirect(
        url_for(
            "pacientes.gerenciar_paciente",
            paciente_id=paciente_id,
        )
    )


# ==========================================================
# EDITAR PACIENTE — TELA
# ==========================================================
@pacientes_bp.route(
    "/editar/paciente/<int:paciente_id>",
    methods=["GET"],
)
@login_required
def editar_paciente(paciente_id):
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return (
            "<h1>Acesso Negado</h1>"
            "<p>Seu perfil não tem permissão para editar pacientes.</p>",
            403,
        )

    paciente = Paciente.query.get_or_404(paciente_id)

    return render_template(
        "pacientes/editar_paciente.html",
        paciente=paciente,
    )


# ==========================================================
# EDITAR PACIENTE — SALVAR
# ==========================================================
@pacientes_bp.route(
    "/editar/paciente/<int:paciente_id>",
    methods=["POST"],
)
@login_required
def editar_paciente_salvar(paciente_id):
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return jsonify(
            {
                "sucesso": False,
                "mensagem": "Você não tem permissão para editar pacientes.",
            }
        ), 403

    paciente = Paciente.query.get_or_404(paciente_id)

    secao = request.form.get(
        "secao",
        "",
    ).strip()

    if secao == "dados-pessoais":
        nome = request.form.get(
            "nome",
            "",
        ).strip()

        data_nascimento_str = request.form.get(
            "data_nascimento",
            "",
        ).strip()

        genero = request.form.get(
            "genero",
            "",
        ).strip()

        if not nome:
            return jsonify(
                {
                    "sucesso": False,
                    "mensagem": "Informe o nome completo do paciente.",
                }
            ), 400

        if genero not in {"M", "F"}:
            return jsonify(
                {
                    "sucesso": False,
                    "mensagem": "Selecione um sexo válido.",
                }
            ), 400

        try:
            data_nascimento = datetime.strptime(
                data_nascimento_str,
                "%Y-%m-%d",
            ).date()

        except (TypeError, ValueError):
            return jsonify(
                {
                    "sucesso": False,
                    "mensagem": "Informe uma data de nascimento válida.",
                }
            ), 400

        hoje = date.today()

        if data_nascimento > hoje:
            return jsonify(
                {
                    "sucesso": False,
                    "mensagem": "A data de nascimento não pode estar no futuro.",
                }
            ), 400

        idade = (
            hoje.year
            - data_nascimento.year
            - (
                (hoje.month, hoje.day)
                < (
                    data_nascimento.month,
                    data_nascimento.day,
                )
            )
        )

        if idade < 0 or idade > 150:
            return jsonify(
                {
                    "sucesso": False,
                    "mensagem": "Verifique a data de nascimento informada.",
                }
            ), 400

        paciente.nome = nome
        paciente.data_nascimento = data_nascimento
        paciente.genero = genero

        try:
            db.session.commit()

        except Exception:
            db.session.rollback()

            return jsonify(
                {
                    "sucesso": False,
                    "mensagem": "Não foi possível salvar os dados pessoais.",
                }
            ), 500

        return jsonify(
            {
                "sucesso": True,
                "secao": "dados-pessoais",
                "mensagem": "Dados pessoais atualizados com sucesso.",
                "paciente": {
                    "nome": paciente.nome,
                    "data_nascimento": paciente.data_nascimento.strftime("%d/%m/%Y"),
                    "data_nascimento_input": paciente.data_nascimento.strftime(
                        "%Y-%m-%d"
                    ),
                    "genero": paciente.genero,
                    "genero_texto": (
                        "Masculino" if paciente.genero == "M" else "Feminino"
                    ),
                    "idade": paciente.idade_atual,
                },
            }
        )

    if secao == "contato":
        telefone = request.form.get(
            "telefone",
            "",
        ).strip()

        email = request.form.get(
            "email",
            "",
        ).strip()

        paciente.telefone = telefone or None
        paciente.email = email or None

        try:
            db.session.commit()

        except Exception:
            db.session.rollback()

            return jsonify(
                {
                    "sucesso": False,
                    "mensagem": "Não foi possível salvar os dados de contato.",
                }
            ), 500

        return jsonify(
            {
                "sucesso": True,
                "secao": "contato",
                "mensagem": "Dados de contato atualizados com sucesso.",
                "paciente": {
                    "telefone": paciente.telefone or "",
                    "email": paciente.email or "",
                },
            }
        )

    return jsonify(
        {
            "sucesso": False,
            "mensagem": "Seção de edição inválida.",
        }
    ), 400


# ==========================================================
# ANAMNESE — EXIBIR / SALVAR
# ==========================================================
@pacientes_bp.route(
    "/paciente/<int:paciente_id>/anamnese",
    methods=["POST"],
)
@login_required
def salvar_anamnese(paciente_id):
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return "<h1>Acesso Negado</h1>", 403

    paciente = Paciente.query.get_or_404(paciente_id)

    anamnese = Anamnese.query.filter_by(paciente_id=paciente.id).first()

    if anamnese is None:
        anamnese = Anamnese(paciente_id=paciente.id)

        db.session.add(anamnese)

    anamnese.objetivo_principal = (
        request.form.get(
            "objetivo_principal",
            "",
        ).strip()
        or None
    )

    anamnese.patologias = (
        request.form.get(
            "patologias",
            "",
        ).strip()
        or None
    )

    anamnese.medicamentos = (
        request.form.get(
            "medicamentos",
            "",
        ).strip()
        or None
    )

    anamnese.alergias_intolerancias = (
        request.form.get(
            "alergias_intolerancias",
            "",
        ).strip()
        or None
    )

    anamnese.aversoes_alimentares = (
        request.form.get(
            "aversoes_alimentares",
            "",
        ).strip()
        or None
    )

    anamnese.qualidade_sono = (
        request.form.get(
            "qualidade_sono",
            "",
        ).strip()
        or None
    )

    consumo_agua = request.form.get(
        "consumo_agua_diario",
        "",
    ).strip()

    try:
        if consumo_agua:
            anamnese.consumo_agua_diario = float(consumo_agua.replace(",", "."))
        else:
            anamnese.consumo_agua_diario = None

        db.session.commit()

    except (TypeError, ValueError):
        db.session.rollback()

        return (
            "<h1>Dados inválidos</h1><p>Verifique o consumo de água informado.</p>",
            400,
        )

    return redirect(
        url_for(
            "pacientes.gerenciar_paciente",
            paciente_id=paciente.id,
        )
    )


# ==========================================================
# NOVA AVALIAÇÃO FÍSICA
# ==========================================================
@pacientes_bp.route(
    "/nova/avaliacao/<int:paciente_id>",
    methods=["GET", "POST"],
)
@login_required
def nova_avaliacao(paciente_id):
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return "<h1>Acesso Negado</h1>", 403

    paciente = Paciente.query.get_or_404(paciente_id)

    if request.method == "POST":
        data_consulta_str = request.form.get(
            "data_consulta",
            "",
        ).strip()

        peso_str = request.form.get(
            "peso_atual",
            "",
        ).strip()

        altura_str = request.form.get(
            "altura_atual",
            "",
        ).strip()

        percentual_gordura_str = request.form.get(
            "percentual_gordura",
            "",
        ).strip()

        percentual_massa_magra_str = request.form.get(
            "percentual_massa_magra",
            "",
        ).strip()

        cintura_str = request.form.get(
            "circunferencia_cintura",
            "",
        ).strip()

        observacoes = request.form.get(
            "observacoes_clinicas",
            "",
        ).strip()

        try:
            data_consulta = datetime.strptime(
                data_consulta_str,
                "%Y-%m-%d",
            )

        except (TypeError, ValueError):
            flash(
                "Informe uma data válida para a avaliação.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        try:
            peso_atual = float(peso_str)
            altura_atual = float(altura_str)

        except (TypeError, ValueError):
            flash(
                "Informe peso e altura válidos.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        if peso_atual <= 0 or peso_atual > 500:
            flash(
                "Informe um peso válido.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        if altura_atual <= 0 or altura_atual > 300:
            flash(
                "Informe uma altura válida.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        try:
            percentual_gordura = (
                float(percentual_gordura_str) if percentual_gordura_str else None
            )

            percentual_massa_magra = (
                float(percentual_massa_magra_str)
                if percentual_massa_magra_str
                else None
            )

            circunferencia_cintura = float(cintura_str) if cintura_str else None

        except (TypeError, ValueError):
            flash(
                "Verifique os valores da composição corporal.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        if percentual_gordura is not None and (
            percentual_gordura < 0 or percentual_gordura > 100
        ):
            flash(
                "O percentual de gordura deve estar entre 0 e 100.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        if percentual_massa_magra is not None and (
            percentual_massa_magra < 0 or percentual_massa_magra > 100
        ):
            flash(
                "O percentual de massa magra deve estar entre 0 e 100.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        if circunferencia_cintura is not None and (
            circunferencia_cintura <= 0 or circunferencia_cintura > 300
        ):
            flash(
                "Informe uma circunferência de cintura válida.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.nova_avaliacao",
                    paciente_id=paciente.id,
                )
            )

        nova_consulta = ConsultaAntropometrica(
            paciente_id=paciente.id,
            data_consulta=data_consulta,
            peso_atual=peso_atual,
            altura_atual=altura_atual,
            percentual_gordura=percentual_gordura,
            percentual_massa_magra=percentual_massa_magra,
            circunferencia_cintura=circunferencia_cintura,
            observacoes_clinicas=observacoes or None,
        )

        db.session.add(nova_consulta)
        db.session.commit()

        flash(
            f"Avaliação física de {paciente.nome} registrada com sucesso.",
            "success",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente.id,
                aba="avaliacao-fisica",
            )
        )

    return render_template(
        "pacientes/nova_avaliacao.html",
        paciente=paciente,
        data_hoje=date.today().isoformat(),
    )


# ==========================================================
# EDITAR AVALIAÇÃO FÍSICA
# ==========================================================
@pacientes_bp.route(
    "/editar/avaliacao/<int:avaliacao_id>",
    methods=["GET", "POST"],
)
@login_required
def editar_avaliacao(avaliacao_id):
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return "<h1>Acesso Negado</h1>", 403

    avaliacao = ConsultaAntropometrica.query.get_or_404(avaliacao_id)

    paciente = Paciente.query.get_or_404(avaliacao.paciente_id)

    if request.method == "POST":
        data_consulta_str = request.form.get(
            "data_consulta",
            "",
        ).strip()

        peso_str = request.form.get(
            "peso_atual",
            "",
        ).strip()

        altura_str = request.form.get(
            "altura_atual",
            "",
        ).strip()

        percentual_gordura_str = request.form.get(
            "percentual_gordura",
            "",
        ).strip()

        percentual_massa_magra_str = request.form.get(
            "percentual_massa_magra",
            "",
        ).strip()

        cintura_str = request.form.get(
            "circunferencia_cintura",
            "",
        ).strip()

        observacoes = request.form.get(
            "observacoes_clinicas",
            "",
        ).strip()

        try:
            data_consulta = datetime.strptime(
                data_consulta_str,
                "%Y-%m-%d",
            )

        except (TypeError, ValueError):
            flash(
                "Informe uma data válida para a avaliação.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        try:
            peso_atual = float(peso_str)
            altura_atual = float(altura_str)

        except (TypeError, ValueError):
            flash(
                "Informe peso e altura válidos.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        if peso_atual <= 0 or peso_atual > 500:
            flash(
                "Informe um peso válido.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        if altura_atual <= 0 or altura_atual > 300:
            flash(
                "Informe uma altura válida.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        try:
            percentual_gordura = (
                float(percentual_gordura_str) if percentual_gordura_str else None
            )

            percentual_massa_magra = (
                float(percentual_massa_magra_str)
                if percentual_massa_magra_str
                else None
            )

            circunferencia_cintura = float(cintura_str) if cintura_str else None

        except (TypeError, ValueError):
            flash(
                "Verifique os valores da composição corporal.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        if percentual_gordura is not None and (
            percentual_gordura < 0 or percentual_gordura > 100
        ):
            flash(
                "O percentual de gordura deve estar entre 0 e 100.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        if percentual_massa_magra is not None and (
            percentual_massa_magra < 0 or percentual_massa_magra > 100
        ):
            flash(
                "O percentual de massa magra deve estar entre 0 e 100.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        if circunferencia_cintura is not None and (
            circunferencia_cintura <= 0 or circunferencia_cintura > 300
        ):
            flash(
                "Informe uma circunferência de cintura válida.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        avaliacao.data_consulta = data_consulta
        avaliacao.peso_atual = peso_atual
        avaliacao.altura_atual = altura_atual
        avaliacao.percentual_gordura = percentual_gordura
        avaliacao.percentual_massa_magra = percentual_massa_magra
        avaliacao.circunferencia_cintura = circunferencia_cintura
        avaliacao.observacoes_clinicas = observacoes or None

        try:
            db.session.commit()

        except Exception:
            db.session.rollback()

            flash(
                "Não foi possível atualizar a avaliação física.",
                "error",
            )

            return redirect(
                url_for(
                    "pacientes.editar_avaliacao",
                    avaliacao_id=avaliacao.id,
                )
            )

        flash(
            "Avaliação física atualizada com sucesso.",
            "success",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente.id,
                aba="avaliacao-fisica",
            )
        )

    return render_template(
        "pacientes/editar_avaliacao.html",
        paciente=paciente,
        avaliacao=avaliacao,
    )


# ==========================================================
# EXCLUIR AVALIAÇÃO FÍSICA
# ==========================================================
@pacientes_bp.route(
    "/excluir/avaliacao/<int:avaliacao_id>",
    methods=["POST"],
)
@login_required
def excluir_avaliacao(avaliacao_id):
    if not current_user.eh_admin() and not current_user.pode_cadastrar_paciente:
        return "<h1>Acesso Negado</h1>", 403

    avaliacao = ConsultaAntropometrica.query.get_or_404(avaliacao_id)

    paciente_id = avaliacao.paciente_id

    try:
        db.session.delete(avaliacao)
        db.session.commit()

    except Exception:
        db.session.rollback()

        flash(
            "Não foi possível excluir a avaliação física.",
            "error",
        )

        return redirect(
            url_for(
                "pacientes.gerenciar_paciente",
                paciente_id=paciente_id,
                aba="avaliacao-fisica",
            )
        )

    flash(
        "Avaliação física excluída com sucesso.",
        "success",
    )

    return redirect(
        url_for(
            "pacientes.gerenciar_paciente",
            paciente_id=paciente_id,
            aba="avaliacao-fisica",
        )
    )
