from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import usuarios_bp
from models import db, Usuario


def usuario_eh_admin():
    return current_user.eh_admin()


@usuarios_bp.route(
    '/alternar/permissao/<int:id>/<permissao>',
    methods=['POST']
)
@login_required
def alternar_permissao_usuario(id, permissao):
    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = db.session.get(Usuario, id)

    if not user:
        flash('Usuário não encontrado.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    if user.eh_admin():
        flash(
            'As permissões da conta administrativa principal são permanentes.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    permissoes_permitidas = {
        'pode_cadastrar_paciente',
        'pode_montar_cardapio',
        'pode_ver_financeiro'
    }

    if permissao not in permissoes_permitidas:
        flash('Permissão inválida.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    nomes_permissoes = {
        'pode_cadastrar_paciente': 'Pacientes',
        'pode_montar_cardapio': 'Cardápios',
        'pode_ver_financeiro': 'Financeiro'
    }

    nome_permissao = nomes_permissoes[permissao]

    novo_valor = not getattr(user, permissao)

    setattr(
        user,
        permissao,
        novo_valor
    )

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        flash(
            f'Não foi possível alterar a permissão de {nome_permissao}.',
            'erro'
        )

        return redirect(
            url_for('usuarios.gerenciar_usuarios')
        )

    if novo_valor:
        flash(
            f'Permissão de {nome_permissao} concedida para {user.nome}.',
            'sucesso'
        )
    else:
        flash(
            f'Permissão de {nome_permissao} removida de {user.nome}.',
            'sucesso'
        )

    return redirect(
        url_for('usuarios.gerenciar_usuarios')
    )


@usuarios_bp.route('/configurar/acesso/<int:id>')
@login_required
def configurar_acesso_usuario(id):
    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = db.session.get(Usuario, id)

    if not user:
        flash('Usuário não encontrado.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    return render_template(
        'usuarios/acesso_usuario.html',
        usuario=user
    )