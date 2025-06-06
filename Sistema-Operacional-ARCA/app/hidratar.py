"""
Módulo de Calculadora de Hidratação

Este módulo contém funções para calcular a quantidade recomendada de água
que uma pessoa deve ingerir diariamente, baseado em:
- Peso corporal
- Temperatura atual da região
"""

from app.api.api_clima import obter_temperatura
from app.api.geolocalizacao import obter_regiao
from app.core.utils import validar_input_float

def calcular_hidratacao(temperatura, peso):
    """
    Calcula a quantidade recomendada de água a ser ingerida diariamente.
    
    A fórmula base é: (peso * 35) / 1000 litros
    Adicionalmente, considera a temperatura:
    - Temperatura >= 32°C: +1.0 litro
    - Temperatura >= 28°C: +0.5 litro
    
    Args:
        temperatura (float): Temperatura atual em graus Celsius
        peso (float): Peso corporal em quilogramas
        
    Returns:
        None: A função apenas exibe as informações na tela
    """
    # Cálculo base: 35ml por kg de peso
    litros = (peso * 35) / 1000
    
    # Ajuste baseado na temperatura
    if temperatura >= 32:
        litros += 1.0
    elif temperatura >= 28:
        litros += 0.5

    print(f"\n🌡️ Temperatura atual: {temperatura} °C")
    print(f"💧 Recomendação: beba aproximadamente {litros:.2f} litros de água hoje.")

def menu_calculadora_hidratacao(usuario_logado):
    """
    Exibe e gerencia o menu da calculadora de hidratação.
    
    Args:
        usuario_logado (dict): Dicionário contendo os dados do usuário atualmente logado,
                             incluindo latitude e longitude
        
    Returns:
        None: A função apenas exibe as informações na tela
    """
    print("\n~~~~ Calculadora de Hidratação ~~~~")
    peso = validar_input_float("Informe seu peso (kg): ")
    lat = usuario_logado['lat']
    lon = usuario_logado['lon']

    temperatura, *_ = obter_temperatura(lat, lon)
    calcular_hidratacao(temperatura, peso)