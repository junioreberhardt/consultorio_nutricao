# usuarios/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario
import os


usuarios_bp = Blueprint('usuarios', __name__)


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
# LOGIN
# ==========================================================

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario_form = request.form.get('nome_usuario')
        senha_form = request.form.get('senha')

        user = Usuario.query.filter_by(
            nome_usuario=usuario_form
        ).first()

        if user:

            senha_valida = False

            # --------------------------------------------------
            # Senha já protegida por hash
            # --------------------------------------------------

            if user.senha.startswith(('scrypt:', 'pbkdf2:')):

                senha_valida = check_password_hash(
                    user.senha,
                    senha_form
                )

            # --------------------------------------------------
            # Senha antiga em texto puro
            #
            # Faz a migração automaticamente para hash
            # após um login válido.
            # --------------------------------------------------

            else:

                if user.senha == senha_form:

                    senha_valida = True

                    user.senha = generate_password_hash(
                        senha_form
                    )

                    db.session.commit()

            # --------------------------------------------------
            # Login autorizado
            # --------------------------------------------------

            if senha_valida:

                if not user.ativo:

                    flash(
                        'Seu acesso está desativado ou aguardando liberação.'
                    )

                    return redirect(
                        url_for('usuarios.login')
                    )

                login_user(user)

                return redirect(
                    url_for('home')
                )

        flash('Usuário ou senha incorretos!')

    return render_template('login.html')


# ==========================================================
# CADASTRO DE USUÁRIO
# ==========================================================

@usuarios_bp.route('/novo/usuario', methods=['GET', 'POST'])
def cadastrar_usuario():

    if request.method == 'POST':

        nome = request.form.get('nome')
        nome_usuario = request.form.get('nome_usuario')
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario_existente = Usuario.query.filter_by(
            nome_usuario=nome_usuario
        ).first()

        email_existente = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario_existente or email_existente:

            return (
                "<h1>Erro</h1>"
                "<p>Este nome de usuário ou e-mail já está em uso.</p>"
                "<a href='/novo/usuario'>Voltar</a>"
            )

        novo_usuario = Usuario(
            nome=nome,
            nome_usuario=nome_usuario,
            email=email,

            # Senha protegida desde o cadastro
            senha=generate_password_hash(senha),

            cargo='outro',
            ativo=False
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return (
            "<h1>Solicitação Enviada!</h1>"
            "<p>Aguarde a liberação.</p>"
            "<a href='/login'>Ir para o Login</a>"
        )

    return render_template('cadastro.html')


# ==========================================================
# PERFIL DO USUÁRIO
# ==========================================================

@usuarios_bp.route('/perfil')
@login_required
def perfil():

    return render_template('perfil.html')


# ==========================================================
# EDITAR PERFIL
# ==========================================================

@usuarios_bp.route('/perfil/editar', methods=['POST'])
@login_required
def editar_perfil():

    novo_nome = request.form.get('nome', '').strip()
    novo_email = request.form.get('email', '').strip()

    # ------------------------------------------------------
    # Validação básica
    # ------------------------------------------------------

    if not novo_nome:

        flash(
            'O nome não pode ficar vazio.'
        )

        return redirect(
            url_for('usuarios.perfil')
        )

    if not novo_email:

        flash(
            'O e-mail não pode ficar vazio.'
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
            'Este e-mail já está sendo utilizado por outro usuário.'
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

        return render_template(
            'perfil.html',
            mensagem_perfil='A senha atual está incorreta.',
            tipo_mensagem='erro'
        )

    # ------------------------------------------------------
    # Verifica a nova senha
    # ------------------------------------------------------

    if not nova_senha:

        return render_template(
            'perfil.html',
            mensagem_perfil='Digite uma nova senha.',
            tipo_mensagem='erro'
        )

    # ------------------------------------------------------
    # Confirma a nova senha
    # ------------------------------------------------------

    if nova_senha != confirmar_senha:

        return render_template(
            'perfil.html',
            mensagem_perfil='A confirmação da nova senha não confere.',
            tipo_mensagem='erro'
        )

    # ------------------------------------------------------
    # Evita reutilizar a senha atual
    # ------------------------------------------------------

    if nova_senha == senha_atual:

        return render_template(
            'perfil.html',
            mensagem_perfil='A nova senha deve ser diferente da senha atual.',
            tipo_mensagem='erro'
        )

    # ------------------------------------------------------
    # Salva a nova senha protegida
    # ------------------------------------------------------

    current_user.senha = generate_password_hash(
        nova_senha
    )

    db.session.commit()

    return render_template(
        'perfil.html',
        mensagem_perfil='Senha alterada com sucesso!',
        tipo_mensagem='sucesso'
    )


# ==========================================================
# ALTERAR FOTO DE PERFIL
# ==========================================================

@usuarios_bp.route('/perfil/foto', methods=['POST'])
@login_required
def atualizar_foto_perfil():

    arquivo = request.files.get('foto')

    # ------------------------------------------------------
    # Verifica se foi selecionado algum arquivo
    # ------------------------------------------------------

    if not arquivo or arquivo.filename == '':

        flash(
            'Nenhuma imagem foi selecionada.'
        )

        return redirect(
            request.referrer or url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Verifica a extensão
    # ------------------------------------------------------

    if '.' not in arquivo.filename:

        flash(
            'Arquivo inválido. Use JPG, JPEG, PNG ou WEBP.'
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
            'Formato de imagem não permitido. '
            'Use JPG, JPEG, PNG ou WEBP.'
        )

        return redirect(
            request.referrer or url_for('usuarios.perfil')
        )

    # ------------------------------------------------------
    # Local da pasta de uploads
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

    # ------------------------------------------------------
    # Cria a pasta caso ela não exista
    # ------------------------------------------------------

    os.makedirs(
        pasta_upload,
        exist_ok=True
    )

    # ------------------------------------------------------
    # Nome do arquivo
    # ------------------------------------------------------

    nome_arquivo = secure_filename(
        f'usuario_{current_user.id}.{extensao}'
    )

    caminho = os.path.join(
        pasta_upload,
        nome_arquivo
    )

    # ------------------------------------------------------
    # Salva a imagem
    # ------------------------------------------------------

    arquivo.save(caminho)

    # ------------------------------------------------------
    # Salva o caminho no banco
    # ------------------------------------------------------

    current_user.foto_perfil = (
        f'uploads/perfil/{nome_arquivo}'
    )

    db.session.commit()

    return redirect(
        request.referrer or url_for('usuarios.perfil')
    )


# ==========================================================
# GERENCIAR USUÁRIOS
# ==========================================================

@usuarios_bp.route('/gerenciar/usuarios')
@login_required
def gerenciar_usuarios():

    if not current_user.eh_admin():

        return (
            "<h1>Acesso Negado</h1>",
            403
        )

    todos = Usuario.query.all()

    return render_template(
        'usuarios.html',
        todos_usuarios=todos
    )


# ==========================================================
# SALVAR PERMISSÕES
# ==========================================================

@usuarios_bp.route('/salvar/permissoes/<int:id>', methods=['POST'])
@login_required
def salvar_permissoes(id):

    # Somente administrador pode alterar usuários
    if not current_user.eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = Usuario.query.get(id)

    if not user:
        return ("Usuário não encontrado", 404)

    # A conta administrativa principal não pode ser editada
    if user.eh_admin():
        return ("<h1>Ação Proibida</h1><p>A conta administrativa principal não pode ser alterada.</p>", 400)

    # ---------------------------------------------------------
    # NOME
    # ---------------------------------------------------------

    nome = request.form.get('nome_editado', '').strip()

    if not nome:
        flash('O nome do usuário é obrigatório.')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    user.nome = nome


    # ---------------------------------------------------------
    # E-MAIL
    # ---------------------------------------------------------

    email = request.form.get('email_editado', '').strip()

    if not email:
        flash('O e-mail do usuário é obrigatório.')
        return redirect(url_for('usuarios.gerenciar_usuarios'))

    user.email = email


    # ---------------------------------------------------------
    # CARGO
    # ---------------------------------------------------------

    cargo_selecionado = request.form.get('cargo')

    if cargo_selecionado == 'outro':

        cargo_personalizado = request.form.get(
            'cargo_personalizado',
            ''
        ).strip()

        if cargo_personalizado:
            user.cargo = cargo_personalizado
        else:
            user.cargo = 'outro'

    else:
        user.cargo = cargo_selecionado


    # ---------------------------------------------------------
    # SALVA
    # ---------------------------------------------------------

    db.session.commit()

    flash('Dados do usuário atualizados com sucesso.')

    return redirect(url_for('usuarios.gerenciar_usuarios'))



@usuarios_bp.route('/alternar/status/<int:id>', methods=['POST'])
@login_required
def alternar_status_usuario(id):

    if not current_user.eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = Usuario.query.get(id)

    if not user:
        return ("Usuário não encontrado", 404)

    if user.eh_admin():
        return (
            "<h1>Ação Proibida</h1>"
            "<p>A conta administrativa principal não pode ser desativada.</p>",
            400
        )

    user.ativo = not user.ativo

    db.session.commit()

    return redirect(url_for('usuarios.gerenciar_usuarios'))



@usuarios_bp.route('/alternar/permissao/<int:id>/<permissao>', methods=['POST'])
@login_required
def alternar_permissao_usuario(id, permissao):

    # Somente administrador pode alterar permissões
    if not current_user.eh_admin():
        return ("<h1>Acesso Negado</h1>", 403)

    user = Usuario.query.get(id)

    if not user:
        return ("Usuário não encontrado", 404)

    # A conta administrativa possui todas as permissões
    if user.eh_admin():
        return (
            "<h1>Ação Proibida</h1>"
            "<p>As permissões da conta administrativa principal são permanentes.</p>",
            400
        )

    # Lista branca: somente estas propriedades podem ser alteradas
    permissoes_permitidas = {
        'pode_cadastrar_paciente',
        'pode_montar_cardapio',
        'pode_ver_financeiro'
    }

    if permissao not in permissoes_permitidas:
        return ("<h1>Permissão inválida</h1>", 400)

    valor_atual = getattr(user, permissao)

    setattr(user, permissao, not valor_atual)

    db.session.commit()

    return redirect(url_for('usuarios.gerenciar_usuarios'))


permissoes_permitidas = {
    'pode_cadastrar_paciente',
    'pode_montar_cardapio',
    'pode_ver_financeiro'
}


# ==========================================================
# ATIVAR / DESATIVAR USUÁRIO
# ==========================================================


# ==========================================================
# EDITAR DADOS DO USUÁRIO
# ==========================================================

@usuarios_bp.route(
    '/editar/usuario/<int:id>',
    methods=['POST']
)
@login_required
def editar_usuario_dados(id):

    if not current_user.eh_admin():

        return (
            "<h1>Acesso Negado</h1>",
            403
        )

    user = Usuario.query.get(id)

    if not user:

        return (
            "Usuário não encontrado",
            404
        )

    # ------------------------------------------------------
    # Protege a conta principal
    # ------------------------------------------------------

    if user.eh_admin():

        return (
            "<h1>Ação Proibida</h1>"
            "<p>A conta mestre do sistema não pode "
            "ser editada por esta rota.</p>",
            400
        )

    user.nome = request.form.get(
        'nome'
    )

    user.email = request.form.get(
        'email'
    )

    db.session.commit()

    return redirect(
        url_for(
            'usuarios.gerenciar_usuarios'
        )
    )


# ==========================================================
# EXCLUIR USUÁRIO
# ==========================================================

@usuarios_bp.route(
    '/excluir/usuario/<int:id>',
    methods=['POST']
)
@login_required
def excluir_usuario(id):

    if not current_user.eh_admin():

        return (
            "<h1>Acesso Negado</h1>",
            403
        )

    user = Usuario.query.get(id)

    if not user:

        return (
            "Usuário não encontrado",
            404
        )

    # ------------------------------------------------------
    # Protege a conta principal
    # ------------------------------------------------------

    if user.eh_admin():

        return (
            "<h1>Ação Proibida</h1>"
            "<p>A conta master do sistema não pode "
            "ser apagada por esta rota.</p>",
            400
        )

    db.session.delete(user)

    db.session.commit()

    return redirect(
        url_for(
            'usuarios.gerenciar_usuarios'
        )
    )


# ==========================================================
# LOGOUT
# ==========================================================

@usuarios_bp.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(
        url_for('usuarios.login')
    )
