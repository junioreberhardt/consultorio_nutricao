from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import case

from . import usuarios_bp
from models import db, Usuario


def usuario_eh_admin():
    return current_user.eh_admin()


@usuarios_bp.route('/gerenciar/usuarios')
@login_required
def gerenciar_usuarios():
    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    todos = Usuario.query.order_by(
        case(
            (Usuario.nome_usuario == 'admin', 0),
            else_ = 1            
        ),
        Usuario.nome
    ).all()

    return render_template(
        'usuarios/usuarios.html',
        todos_usuarios=todos
    )


@usuarios_bp.route('/salvar/permissoes/<int:id>', methods=['POST'])
@login_required
def salvar_permissoes(id):
    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = db.session.get(Usuario, id)

    if not user:
        flash('Usuário não encontrado.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    if user.eh_admin():
        flash(
            'A conta administrativa principal não pode ser alterada.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    nome = request.form.get('nome_editado', '').strip()

    if not nome:
        flash('O nome do usuário é obrigatório.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    email = request.form.get('email_editado', '').strip().lower()

    if not email:
        flash('O e-mail do usuário é obrigatório.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    email_existente = Usuario.query.filter(
        Usuario.email == email,
        Usuario.id != user.id
    ).first()

    if email_existente:
        flash(
            'Este e-mail já está sendo utilizado por outro usuário.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    cargos_permitidos = {
        'atendente',
        'estagiario',
        'nutricionista',
        'secretaria',
        'outro'
    }

    cargo_selecionado = request.form.get('cargo', '').strip()

    if cargo_selecionado not in cargos_permitidos:
        flash('Cargo inválido.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    if cargo_selecionado == 'outro':
        cargo_personalizado = request.form.get(
            'cargo_personalizado',
            ''
        ).strip()

        if not cargo_personalizado:
            flash('Informe o cargo personalizado.', 'erro')
            return redirect(url_for('usuarios.gerenciar_usuarios'))

        user.cargo = cargo_personalizado
    else:
        user.cargo = cargo_selecionado

    user.nome = nome
    user.email = email

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(
            'Não foi possível atualizar os dados do usuário.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    flash(
        'Dados do usuário atualizados com sucesso.',
        'sucesso'
    )

    return redirect(url_for('usuarios.gerenciar_usuarios'))


@usuarios_bp.route('/alternar/status/<int:id>', methods=['POST'])
@login_required
def alternar_status_usuario(id):
    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = db.session.get(Usuario, id)

    if not user:
        flash('Usuário não encontrado.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    if user.eh_admin():
        flash(
            'A conta administrativa principal não pode ser desativada.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    user.ativo = not user.ativo

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(
            'Não foi possível alterar o status do usuário.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    if user.ativo:
        flash(
            f'{user.nome} foi ativado com sucesso.',
            'sucesso'
        )
    else:
        flash(
            f'{user.nome} foi desativado com sucesso.',
            'sucesso'
        )

    return redirect(url_for('usuarios.gerenciar_usuarios'))


@usuarios_bp.route('/editar/usuario/<int:id>', methods=['GET'])
@login_required
def editar_usuario(id):
    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = db.session.get(Usuario, id)

    if not user:
        flash('Usuário não encontrado.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    if user.eh_admin():
        flash(
            'A conta administrativa principal não pode ser editada por esta página.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    return render_template(
        'usuarios/editar_usuario.html',
        usuario=user
    )


@usuarios_bp.route('/editar/usuario/<int:id>', methods=['POST'])
@login_required
def editar_usuario_dados(id):

    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = db.session.get(Usuario, id)

    if not user:
        flash(
            'Usuário não encontrado.',
            'erro'
        )
        return redirect(
            url_for('usuarios.gerenciar_usuarios')
        )

    # A conta administrativa principal não pode ser
    # editada por esta página.
    if user.eh_admin():
        flash(
            'A conta administrativa principal não pode ser editada por esta página.',
            'erro'
        )
        return redirect(
            url_for('usuarios.gerenciar_usuarios')
        )

    # =========================================================
    # DADOS RECEBIDOS DO FORMULÁRIO
    # =========================================================

    nome = request.form.get(
        'nome',
        ''
    ).strip()

    email = request.form.get(
        'email',
        ''
    ).strip().lower()

    cargo_selecionado = request.form.get(
        'cargo',
        ''
    ).strip()

    cargo_personalizado = request.form.get(
        'cargo_personalizado',
        ''
    ).strip()

    ativo = request.form.get(
        'ativo'
    ) == '1'

    pode_cadastrar_paciente = request.form.get(
        'pode_cadastrar_paciente'
    ) == '1'

    pode_montar_cardapio = request.form.get(
        'pode_montar_cardapio'
    ) == '1'

    pode_ver_financeiro = request.form.get(
        'pode_ver_financeiro'
    ) == '1'

    # Dados usados para preservar os valores digitados
    # caso alguma validação falhe.
    dados_formulario = {
        'nome': nome,
        'email': email,
        'cargo': cargo_selecionado,
        'cargo_personalizado': cargo_personalizado,
        'ativo': ativo,
        'pode_cadastrar_paciente': pode_cadastrar_paciente,
        'pode_montar_cardapio': pode_montar_cardapio,
        'pode_ver_financeiro': pode_ver_financeiro
    }

    def mostrar_erro(mensagem, campo=None):

        return render_template(
            'usuarios/editar_usuario.html',
            usuario=user,
            erro_edicao=mensagem,
            erro_campo=campo,
            dados_formulario=dados_formulario
        )

    # =========================================================
    # VALIDAÇÃO DO NOME
    # =========================================================

    if not nome:

        return mostrar_erro(
            'O nome do usuário é obrigatório.',
            'nome'
        )

    # =========================================================
    # VALIDAÇÃO DO E-MAIL
    # =========================================================

    if not email:

        return mostrar_erro(
            'O e-mail do usuário é obrigatório.',
            'email'
        )

    email_existente = Usuario.query.filter(
        Usuario.email == email,
        Usuario.id != user.id
    ).first()

    if email_existente:

        return mostrar_erro(
            'Este e-mail já está sendo utilizado por outro usuário.',
            'email'
        )

    # =========================================================
    # VALIDAÇÃO DO CARGO
    # =========================================================

    cargos_padrao = {
        'atendente',
        'estagiario',
        'nutricionista',
        'secretaria',
        'outro'
    }

    if cargo_selecionado not in cargos_padrao:

        return mostrar_erro(
            'Cargo inválido.',
            'cargo'
        )

    # ---------------------------------------------------------
    # CARGO PERSONALIZADO
    # ---------------------------------------------------------
    #
    # Se "outro" foi selecionado:
    #
    # 1. Se foi digitado um novo cargo, usa o novo cargo.
    #
    # 2. Se não foi digitado nada, mas o usuário já possui
    #    um cargo personalizado salvo, mantém o cargo existente.
    #
    # 3. Se "outro" foi selecionado e não existe cargo
    #    personalizado anterior, exige preenchimento.
    # ---------------------------------------------------------

    cargos_padrao_salvos = {
        'atendente',
        'estagiario',
        'nutricionista',
        'secretaria'
    }

    if cargo_selecionado == 'outro':

        # Usuário digitou um novo cargo personalizado.
        if cargo_personalizado:

            novo_cargo = cargo_personalizado

        # Usuário já possui um cargo personalizado salvo.
        elif user.cargo not in cargos_padrao_salvos:

            novo_cargo = user.cargo

        # É um usuário novo escolhendo "Outro",
        # mas não informou qual cargo.
        else:

            return mostrar_erro(
                'Informe o cargo personalizado.',
                'cargo_personalizado'
            )

    else:

        novo_cargo = cargo_selecionado

    # =========================================================
    # GUARDAR VALORES ANTIGOS
    # =========================================================

    nome_antigo = user.nome
    email_antigo = user.email
    cargo_antigo = user.cargo
    ativo_antigo = user.ativo

    pacientes_antigo = (
        user.pode_cadastrar_paciente
    )

    cardapio_antigo = (
        user.pode_montar_cardapio
    )

    financeiro_antigo = (
        user.pode_ver_financeiro
    )

    # =========================================================
    # APLICAR ALTERAÇÕES
    # =========================================================

    user.nome = nome
    user.email = email
    user.cargo = novo_cargo
    user.ativo = ativo

    user.pode_cadastrar_paciente = (
        pode_cadastrar_paciente
    )

    user.pode_montar_cardapio = (
        pode_montar_cardapio
    )

    user.pode_ver_financeiro = (
        pode_ver_financeiro
    )

    # =========================================================
    # SALVAR NO BANCO
    # =========================================================

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        return mostrar_erro(
            'Não foi possível salvar as alterações. '
            'Verifique os dados e tente novamente.'
        )

    # =========================================================
    # MONTAR MENSAGEM DE ALTERAÇÕES
    # =========================================================

    alteracoes = []

    if nome != nome_antigo:

        alteracoes.append(
            f'Nome alterado para {nome}.'
        )

    if email != email_antigo:

        alteracoes.append(
            f'E-mail alterado para {email}.'
        )

    if novo_cargo != cargo_antigo:

        nomes_cargos = {
            'atendente': 'Atendente',
            'estagiario': 'Estagiário',
            'nutricionista': 'Nutricionista',
            'secretaria': 'Secretária'
        }

        cargo_exibicao = nomes_cargos.get(
            novo_cargo,
            novo_cargo
        )

        alteracoes.append(
            f'Cargo alterado para {cargo_exibicao}.'
        )

    if ativo != ativo_antigo:

        if ativo:

            alteracoes.append(
                'Acesso ao sistema liberado.'
            )

        else:

            alteracoes.append(
                'Acesso ao sistema bloqueado.'
            )

    if (
        pode_cadastrar_paciente
        != pacientes_antigo
    ):

        if pode_cadastrar_paciente:

            alteracoes.append(
                'Permissão para cadastrar e gerenciar pacientes liberada.'
            )

        else:

            alteracoes.append(
                'Permissão para cadastrar e gerenciar pacientes removida.'
            )

    if (
        pode_montar_cardapio
        != cardapio_antigo
    ):

        if pode_montar_cardapio:

            alteracoes.append(
                'Permissão para montar cardápios liberada.'
            )

        else:

            alteracoes.append(
                'Permissão para montar cardápios removida.'
            )

    if (
        pode_ver_financeiro
        != financeiro_antigo
    ):

        if pode_ver_financeiro:

            alteracoes.append(
                'Permissão para visualizar o financeiro liberada.'
            )

        else:

            alteracoes.append(
                'Permissão para visualizar o financeiro removida.'
            )

    # =========================================================
    # MENSAGEM FINAL
    # =========================================================

    if alteracoes:

        mensagem = (
            f'{user.nome} atualizado com sucesso.\n'
            + '\n'.join(
                f'• {alteracao}'
                for alteracao in alteracoes
            )
        )

        flash(
            mensagem,
            'sucesso'
        )

    else:

        flash(
            f'Nenhuma alteração foi realizada em {user.nome}.',
            'info'
        )

    return redirect(
        url_for('usuarios.gerenciar_usuarios')
    )


@usuarios_bp.route('/excluir/usuario/<int:id>', methods=['POST'])
@login_required
def excluir_usuario(id):
    if not usuario_eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = db.session.get(Usuario, id)

    if not user:
        flash('Usuário não encontrado.', 'erro')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    if user.eh_admin():
        flash(
            'A conta administrativa principal não pode ser excluída.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    nome_usuario = user.nome

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(
            'Não foi possível excluir o usuário.',
            'erro'
        )
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    flash(
        f'Usuário {nome_usuario} excluído com sucesso.',
        'sucesso'
    )

    return redirect(url_for('usuarios.gerenciar_usuarios'))
