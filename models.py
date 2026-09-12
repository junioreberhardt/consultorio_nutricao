from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nome_usuario = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=False, nullable=False)
    cargo = db.Column(db.String(50), default="usuario", nullable=False)

    pode_cadastrar_paciente = db.Column(db.Boolean, default=True, nullable=False)
    pode_montar_cardapio = db.Column(db.Boolean, default=False, nullable=False)
    pode_ver_financeiro = db.Column(db.Boolean, default=False, nullable=False)

    tema_preferido = db.Column(db.String(10), default="claro", nullable=False)
    foto_perfil = db.Column(db.String(255), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    ultimo_acesso = db.Column(db.DateTime, nullable=True)

    # AQUI ESTÁ A NOVA REGRA PROFISSIONAL:
    def eh_admin(self):
        return self.nome_usuario == "admin"


class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def idade_atual(self):
        """Calcula a idade atual a partir da data de nascimento."""

        hoje = datetime.now()

        return (
            hoje.year
            - self.data_nascimento.year
            - (
                (hoje.month, hoje.day)
                < (self.data_nascimento.month, self.data_nascimento.day)
            )
        )

    evolucoes = db.relationship(
        "ConsultaAntropometrica",
        backref="paciente",
        lazy=True,
        cascade="all, delete-orphan",
    )

    anamneses = db.relationship(
        "Anamnese", backref="paciente", uselist=False, cascade="all, delete-orphan"
    )

    planos_alimentares = db.relationship(
        "PlanoAlimentar", backref="paciente", lazy=True, cascade="all, delete-orphan"
    )


class ConsultaAntropometrica(db.Model):
    __tablename__ = "consultas_antropometricas"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    data_consulta = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Métricas corporais capturadas na consulta
    peso_atual = db.Column(db.Float, nullable=False)
    altura_atual = db.Column(db.Float, nullable=False)
    percentual_gordura = db.Column(
        db.Float, nullable=True
    )  # Dobras cutâneas ou bioimpedância
    percentual_massa_magra = db.Column(db.Float, nullable=True)
    circunferencia_cintura = db.Column(db.Float, nullable=True)
    observacoes_clinicas = db.Column(db.Text, nullable=True)


# TABELA 2: FICHA DE ANAMNESE E RECORDATÓRIO CLÍNICO (1 PARA 1)
class Anamnese(db.Model):
    __tablename__ = "anamneses"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)

    # Histórico de Saúde
    objetivo_principal = db.Column(
        db.String(100), nullable=True
    )  # Ex: Emagrecimento, Hipertrofia
    patologias = db.Column(db.Text, nullable=True)  # Ex: Diabetes, Hipertensão
    medicamentos = db.Column(db.Text, nullable=True)
    alergias_intolerancias = db.Column(
        db.Text, nullable=True
    )  # Ex: Intolerância à lactose
    aversoes_alimentares = db.Column(
        db.Text, nullable=True
    )  # Alimentos que o paciente odeia

    # Rotina e Hábitos
    qualidade_sono = db.Column(db.String(50), nullable=True)
    consumo_agua_diario = db.Column(db.Float, nullable=True)  # Em litros


# TABELA 3: PASTA DE PLANOS ALIMENTARES (HISTÓRICO DE DIETAS)
class PlanoAlimentar(db.Model):
    __tablename__ = "planos_alimentares"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    nome_plano = db.Column(db.String(100), default="Plano Alimentar Padrão")
    meta_calorica = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default="Ativo")  # Ativo, Arquivado, Rascunho
