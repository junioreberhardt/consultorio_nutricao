from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Anamnese, Paciente, db

from . import pacientes_bp


# ==========================================================
# GERENCIAR PACIENTE / PRONTUÁRIO
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
        "pacientes/prontuario/gerenciar_paciente.html",
        paciente=paciente,
        anamnese=anamnese,
        aba_inicial=aba,
    )


# ==========================================================
# ANAMNESE — SALVAR
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
