from datetime import date

from app import app
from models import db, Paciente


# =========================================================
# PACIENTES DE TESTE
# =========================================================

DATA_REFERENCIA = date(2026, 9, 7)


pacientes_teste = [
    ("Ana Beatriz Almeida", 29, "F", 61.5, 1.62, "(47) 99999-1001"),
    ("Bruno Henrique Alves", 34, "M", 78.2, 1.78, "(47) 99999-1002"),
    ("Camila Fernanda Andrade", 41, "F", 69.8, 1.65, "(47) 99999-1003"),
    ("Daniel Augusto Barbosa", 52, "M", 91.4, 1.82, "(47) 99999-1004"),
    ("Eduarda Cristina Batista", 23, "F", 55.7, 1.59, "(47) 99999-1005"),
    ("Felipe Martins Cardoso", 38, "M", 84.6, 1.80, "(47) 99999-1006"),
    ("Gabriela Souza Costa", 31, "F", 63.1, 1.67, "(47) 99999-1007"),
    ("Gustavo Henrique Dias", 45, "M", 88.7, 1.76, "(47) 99999-1008"),
    ("Helena Duarte Ferreira", 27, "F", 58.4, 1.61, "(47) 99999-1009"),
    ("Igor Rafael Gomes", 36, "M", 76.9, 1.74, "(47) 99999-1010"),

    ("Juliana Martins Lima", 44, "F", 72.5, 1.68, "(47) 99999-1011"),
    ("Lucas Gabriel Machado", 25, "M", 71.3, 1.81, "(47) 99999-1012"),
    ("Mariana Oliveira Mendes", 33, "F", 64.8, 1.63, "(47) 99999-1013"),
    ("Matheus Pereira Monteiro", 40, "M", 82.1, 1.79, "(47) 99999-1014"),
    ("Natalia Rodrigues Moraes", 30, "F", 59.6, 1.60, "(47) 99999-1015"),
    ("Otavio Ribeiro Nascimento", 57, "M", 95.3, 1.75, "(47) 99999-1016"),
    ("Patricia Santos Oliveira", 48, "F", 77.2, 1.66, "(47) 99999-1017"),
    ("Rafael Silva Pinto", 32, "M", 80.4, 1.83, "(47) 99999-1018"),
    ("Renata Teixeira Ramos", 39, "F", 68.9, 1.64, "(47) 99999-1019"),
    ("Rodrigo Fernandes Rocha", 46, "M", 87.5, 1.77, "(47) 99999-1020"),

    ("Sandra Cristina Santos", 55, "F", 74.1, 1.58, "(47) 99999-1021"),
    ("Thiago Barbosa Souza", 28, "M", 73.8, 1.82, "(47) 99999-1022"),
    ("Vanessa Caroline Teixeira", 35, "F", 62.7, 1.69, "(47) 99999-1023"),
    ("Victor Hugo Vieira", 42, "M", 90.1, 1.85, "(47) 99999-1024"),
    ("Amanda Cristina Xavier", 26, "F", 57.3, 1.60, "(47) 99999-1025"),
    ("Caio Henrique Alves", 37, "M", 79.5, 1.73, "(47) 99999-1026"),
    ("Beatriz Martins Barros", 43, "F", 70.6, 1.65, "(47) 99999-1027"),
    ("Carlos Eduardo Campos", 51, "M", 86.4, 1.78, "(47) 99999-1028"),
    ("Claudia Regina Carvalho", 49, "F", 73.2, 1.62, "(47) 99999-1029"),
    ("Diego Moreira Correia", 24, "M", 68.7, 1.76, "(47) 99999-1030"),

    ("Elisa Maria Dias", 58, "F", 81.3, 1.59, "(47) 99999-1031"),
    ("Fernando Luiz Farias", 47, "M", 92.6, 1.80, "(47) 99999-1032"),
    ("Isabela Martins Freitas", 22, "F", 54.9, 1.57, "(47) 99999-1033"),
    ("Joao Pedro Goncalves", 35, "M", 77.6, 1.82, "(47) 99999-1034"),
    ("Larissa Cristina Lopes", 28, "F", 60.8, 1.64, "(47) 99999-1035"),
    ("Leonardo Marques Medeiros", 41, "M", 83.9, 1.79, "(47) 99999-1036"),
    ("Monica Regina Nunes", 53, "F", 75.4, 1.61, "(47) 99999-1037"),
    ("Paulo Roberto Pacheco", 60, "M", 89.8, 1.74, "(47) 99999-1038"),
    ("Priscila Araujo Peixoto", 32, "F", 66.3, 1.67, "(47) 99999-1039"),
    ("Samuel Rodrigues Reis", 29, "M", 72.4, 1.80, "(47) 99999-1040"),

    ("Simone Cristina Ribeiro", 46, "F", 69.7, 1.63, "(47) 99999-1041"),
    ("Alexandre Martins Santana", 54, "M", 94.2, 1.77, "(47) 99999-1042"),
    ("Aline Beatriz Soares", 34, "F", 61.9, 1.66, "(47) 99999-1043"),
    ("Anderson Luiz Tavares", 39, "M", 85.7, 1.84, "(47) 99999-1044"),
    ("Bruna Caroline Torres", 27, "F", 56.8, 1.60, "(47) 99999-1045"),
    ("Cristiano Oliveira Vaz", 43, "M", 81.6, 1.76, "(47) 99999-1046"),
    ("Denise Maria Viana", 50, "F", 78.3, 1.64, "(47) 99999-1047"),
    ("Eduardo Henrique Vieira", 31, "M", 75.9, 1.81, "(47) 99999-1048"),
    ("Flavia Regina Martins", 37, "F", 65.4, 1.62, "(47) 99999-1049"),
    ("Marcelo Augusto Rocha", 56, "M", 93.5, 1.79, "(47) 99999-1050"),
]


# =========================================================
# GERAR DATA DE NASCIMENTO
# =========================================================

def gerar_data_nascimento(idade):
    return date(
        DATA_REFERENCIA.year - idade,
        DATA_REFERENCIA.month,
        DATA_REFERENCIA.day
    )


# =========================================================
# INSERCAO
# =========================================================

with app.app_context():

    existentes = {
        paciente.nome
        for paciente in Paciente.query.all()
    }

    novos = []

    for dados in pacientes_teste:

        nome = dados[0]
        idade = dados[1]

        if nome in existentes:
            continue

        paciente = Paciente(
            nome=nome,
            data_nascimento=gerar_data_nascimento(idade),
            genero=dados[2],
            peso=dados[3],
            altura=dados[4],
            telefone=dados[5]
        )

        db.session.add(paciente)
        novos.append(nome)

    if novos:

        db.session.commit()

        print()
        print("=" * 50)
        print("PACIENTES DE TESTE INSERIDOS")
        print("=" * 50)
        print(f"Quantidade inserida: {len(novos)}")
        print()

    else:

        print()
        print("=" * 50)
        print("NENHUM PACIENTE FOI INSERIDO")
        print("=" * 50)
        print("Os 50 pacientes de teste ja existem no banco.")
        print()