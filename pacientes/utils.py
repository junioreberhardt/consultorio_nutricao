import unicodedata

from flask_login import current_user


def usuario_pode_cadastrar_paciente():
    return current_user.eh_admin() or current_user.pode_cadastrar_paciente


def remover_acentos(texto):
    return "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caractere) != "Mn"
    )
