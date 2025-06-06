"""
Módulo de Utilitários

Este módulo contém funções utilitárias utilizadas em todo o sistema ARCA,
incluindo:
- Limpeza do console
- Formatação de data e hora
- Validação de entrada de dados
"""

import os
from datetime import datetime

# Limpeza de console 
def limpar_console():
    """
    Limpa a tela do console de forma compatível com diferentes sistemas operacionais.
    
    Returns:
        None: A função apenas limpa a tela do console
    """
    os.system("cls" if os.name == "nt" else "clear")

# Formatação da data e hora atual
def data_atual_formatada():
    """
    Retorna a data e hora atual formatada.
    
    Returns:
        str: Data e hora no formato "YYYY-MM-DD HH:MM"
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M")

# Validação de número float com tratamento de erro
def validar_input_float(mensagem):
    """
    Solicita e valida a entrada de um número decimal.
    
    Args:
        mensagem (str): Mensagem a ser exibida ao solicitar a entrada
        
    Returns:
        float: Número decimal válido inserido pelo usuário
        
    Note:
        A função continua solicitando entrada até que um número válido seja fornecido
    """
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("⚠️ Valor inválido. Digite um número válido.")