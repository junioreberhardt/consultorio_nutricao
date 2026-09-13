from datetime import date, datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import ConsultaAntropometrica, Paciente, db

from . import pacientes_bp


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
        "pacientes/prontuario/nova_avaliacao.html",
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
        "pacientes/prontuario/editar_avaliacao.html",
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
