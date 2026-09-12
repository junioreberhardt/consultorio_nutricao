from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from . import usuarios_bp
from models import db, Usuario


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

        if user and check_password_hash(user.senha, senha_form):

            if not user.ativo:

                flash(
                    'Seu acesso está desativado ou aguardando liberação.'
                )

                return redirect(
                    url_for('usuarios.login')
                )
                
            user.ultimo_acesso = datetime.utcnow()
            db.session.commit()

            login_user(user)

            return redirect(
                url_for('sistema.home')
            )

        flash('Usuário ou senha incorretos!')

    return render_template('auth/login.html')


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

    return render_template('auth/cadastro.html')


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