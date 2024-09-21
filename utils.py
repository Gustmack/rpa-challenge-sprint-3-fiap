import unicodedata
from difflib import SequenceMatcher

# Função para remover acentos de uma string
def remover_acentos(texto):
    """
    Remove acentos de uma string utilizando o método de normalização 'NFD'.

    Args:
        texto (str): Texto de entrada que pode conter acentos.

    Retorna:
        str: Texto sem acentos.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Função para calcular a similaridade entre duas strings
def similaridade(a, b):
    """
    Calcula a similaridade entre duas strings utilizando a classe SequenceMatcher.

    Args:
        a (str): Primeira string para comparação.
        b (str): Segunda string para comparação.

    Retorna:
        float: Valor da similaridade entre as duas strings (entre 0 e 1).
    """
    return SequenceMatcher(None, a, b).ratio()

def consultar_empresa():
    """
    Solicita ao usuário o nome de uma empresa via input.

    Retorna:
        str: Nome da empresa fornecido pelo usuário.
    """
    nome_empresa = input("Digite o nome da empresa: ")
    return nome_empresa
