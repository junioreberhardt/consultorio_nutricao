from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from . import usuarios_bp
from models import db, Usuario

import os


# ==========================================================
# CONFIGURAÇÃO DE UPLOAD
# ==========================================================

EXTENSOES_PERMITIDAS = {
    'jpg',
    'jpeg',
    'png',
    'webp'
}


# ==========================================================
# PERFIL DO USUÁRIO
# ==========================================================

@usuarios_bp.route('/perfil')
@login_required
def perfil():

    return render_template('usuarios/perfil.html')


# ==========================================================
# EDITAR PERFIL
# ==========================================================

@usuarios_bp.route('/perfil/editar', methods=['POST'])
@login_required
def editar_perfil():

    novo_nome = request.form.get(
        'nome',
        ''
    ).strip()

    novo_email = request.form.get(
        'email',
        ''
    ).strip()

    # ------------------------------------------------------
    # Validação básica
    # ------------------------------------------------------

    if not novo_nome:

        flash(
            'O nome não pode ficar vazio.',
            'erro'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    if not novo_email:

        flash(
            'O e-mail não pode ficar vazio.',
            'erro'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Verifica se o e-mail já pertence a outro usuário
    # ------------------------------------------------------

    email_existente = Usuario.query.filter(
        Usuario.email == novo_email,
        Usuario.id != current_user.id
    ).first()

    if email_existente:

        flash(
            'Este e-mail já está sendo utilizado por outro usuário.',
            'erro'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Atualiza os dados
    # ------------------------------------------------------

    current_user.nome = novo_nome
    current_user.email = novo_email

    db.session.commit()

    flash(
        'Perfil atualizado com sucesso.',
        'sucesso'
    )

    return redirect(
        url_for('usuarios.perfil')
    )


# ==========================================================
# ALTERAR SENHA
# ==========================================================

@usuarios_bp.route('/perfil/senha', methods=['POST'])
@login_required
def alterar_senha():

    senha_atual = request.form.get(
        'senha_atual',
        ''
    )

    nova_senha = request.form.get(
        'nova_senha',
        ''
    )

    confirmar_senha = request.form.get(
        'confirmar_senha',
        ''
    )

    # ------------------------------------------------------
    # Verifica a senha atual
    #
    # Compatível com:
    # - senhas antigas em texto puro
    # - senhas novas protegidas por hash
    # ------------------------------------------------------

    senha_atual_valida = False

    if current_user.senha.startswith(
        ('scrypt:', 'pbkdf2:')
    ):

        senha_atual_valida = check_password_hash(
            current_user.senha,
            senha_atual
        )

    else:

        senha_atual_valida = (
            current_user.senha == senha_atual
        )

    if not senha_atual_valida:

        flash(
            'A senha atual está incorreta.',
            'erro'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Verifica a nova senha
    # ------------------------------------------------------

    if not nova_senha:

        flash(
            'Digite uma nova senha.',
            'erro'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Confirma a nova senha
    # ------------------------------------------------------

    if nova_senha != confirmar_senha:

        flash(
            'A confirmação da nova senha não confere.',
            'erro'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Evita reutilizar a senha atual
    # ------------------------------------------------------

    if nova_senha == senha_atual:

        flash(
            'A nova senha deve ser diferente da senha atual.',
            'erro'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Salva a nova senha protegida
    # ------------------------------------------------------

    current_user.senha = generate_password_hash(
        nova_senha
    )

    db.session.commit()

    flash(
        'Senha alterada com sucesso!',
        'sucesso'
    )

    return redirect(
        url_for('usuarios.perfil')
    )


# ==========================================================
# ALTERAR FOTO DE PERFIL
# ==========================================================

@usuarios_bp.route('/perfil/foto', methods=['POST'])
@login_required
def atualizar_foto_perfil():

    arquivo = request.files.get('foto')

    if not arquivo or not arquivo.filename:

        flash(
            'Nenhuma imagem foi selecionada.',
            'erro'
        )

        return redirect(
            request.referrer or url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Limite de 5 MB
    # ------------------------------------------------------

    tamanho_maximo = 5 * 1024 * 1024

    arquivo.seek(0, os.SEEK_END)
    tamanho_arquivo = arquivo.tell()
    arquivo.seek(0)

    if tamanho_arquivo > tamanho_maximo:

        flash(
            'A imagem deve ter no máximo 5 MB.',
            'erro'
        )

        return redirect(
            request.referrer or url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Verifica extensão
    # ------------------------------------------------------

    if '.' not in arquivo.filename:

        flash(
            'Arquivo de imagem inválido.',
            'erro'
        )

        return redirect(
            request.referrer or url_for('usuarios.perfil')
        )

    extensao = arquivo.filename.rsplit(
        '.',
        1
    )[1].lower()

    if extensao not in EXTENSOES_PERMITIDAS:

        flash(
            'Formato não permitido. Use JPG, JPEG, PNG ou WEBP.',
            'erro'
        )

        return redirect(
            request.referrer or url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Pasta dos avatares
    # ------------------------------------------------------

    pasta_upload = os.path.join(
        usuarios_bp.root_path,
        '..',
        'static',
        'uploads',
        'perfil'
    )

    pasta_upload = os.path.abspath(
        pasta_upload
    )

    os.makedirs(
        pasta_upload,
        exist_ok=True
    )

    # ------------------------------------------------------
    # Nome padronizado por usuário
    # ------------------------------------------------------

    nome_arquivo = secure_filename(
        f'usuario_{current_user.id}.{extensao}'
    )

    caminho_novo = os.path.join(
        pasta_upload,
        nome_arquivo
    )

    # ------------------------------------------------------
    # Guarda os arquivos antigos do usuário
    # ------------------------------------------------------

    arquivos_antigos = []

    for extensao_antiga in EXTENSOES_PERMITIDAS:

        caminho_antigo = os.path.join(
            pasta_upload,
            f'usuario_{current_user.id}.{extensao_antiga}'
        )

        if os.path.exists(caminho_antigo):

            arquivos_antigos.append(
                caminho_antigo
            )

    # ------------------------------------------------------
    # Salva a nova imagem
    # ------------------------------------------------------

    try:

        arquivo.save(
            caminho_novo
        )

        # Atualiza o banco
        current_user.foto_perfil = (
            f'uploads/perfil/{nome_arquivo}'
        )

        db.session.commit()

    except Exception:

        # Se algo falhar, remove a nova imagem
        # para não deixar arquivo órfão

        if os.path.exists(caminho_novo):

            os.remove(
                caminho_novo
            )

        db.session.rollback()

        flash(
            'Não foi possível atualizar a foto de perfil.',
            'erro'
        )

        return redirect(
            request.referrer or url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Remove versões antigas
    # ------------------------------------------------------

    for caminho_antigo in arquivos_antigos:

        if caminho_antigo != caminho_novo:

            try:

                os.remove(
                    caminho_antigo
                )

            except OSError:

                pass

    flash(
        'Foto de perfil atualizada com sucesso.',
        'sucesso'
    )

    return redirect(
        request.referrer or url_for('usuarios.perfil')
    )
