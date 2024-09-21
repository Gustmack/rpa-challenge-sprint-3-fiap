import unicodedata
from difflib import SequenceMatcher

# Função para remover acentos de uma string
def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Função para calcular a similaridade entre duas strings
def similaridade(a, b):
    return SequenceMatcher(None, a, b).ratio()


def consultar_empresa():
    nome_empresa = input("Digite o nome da empresa: ")
    return nome_empresa
