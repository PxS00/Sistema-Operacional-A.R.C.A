"""
Módulo de Integração com API de Clima

Este módulo contém funções para obter informações meteorológicas utilizando
a API Open-Meteo, incluindo:
- Temperatura atual
- Probabilidade de chuva
- Precipitação acumulada
- Condições do tempo
- Velocidade do vento
- Rajadas de vento
"""

import requests

def obter_temperatura(lat, lon):
    """
    Obtém informações meteorológicas para uma localização específica.
    
    Args:
        lat (float): Latitude da localização
        lon (float): Longitude da localização
        
    Returns:
        tuple: Tupla contendo (temperatura, chuva_prob, chuva_acumulada, condicao, velocidade_vento, rajadas_vento)
            - temperatura (float): Temperatura atual em graus Celsius
            - chuva_prob (int): Probabilidade de chuva em porcentagem
            - chuva_acumulada (float): Precipitação acumulada em mm
            - condicao (str): Descrição das condições do tempo
            - velocidade_vento (float): Velocidade do vento em km/h
            - rajadas_vento (float): Velocidade das rajadas de vento em km/h
            
        Em caso de erro, retorna valores padrão:
            (28.0, 0, 0, "Desconhecido", 0.0, 0.0)
    
    Raises:
        requests.RequestException: Se houver erro na requisição HTTP
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=precipitation_probability,precipitation,windspeed_10m,windgusts_10m"
        f"&daily=precipitation_sum"
        f"&timezone=America%2FSao_Paulo"
        f"&windspeed_unit=kmh"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta exceção para códigos de erro HTTP
        
        dados = response.json()
        
        # Validação da estrutura da resposta
        if not isinstance(dados, dict):
            raise ValueError("Resposta da API em formato inválido")
            
        # Extração dos dados com validação
        current_weather = dados.get("current_weather", {})
        hourly = dados.get("hourly", {})
        daily = dados.get("daily", {})
        
        # Valores padrão caso algum campo não exista
        temperatura = current_weather.get("temperature", 28.0)
        weathercode = current_weather.get("weathercode", 0)
        chuva_prob = hourly.get("precipitation_probability", [0])[0] if hourly.get("precipitation_probability") else 0
        chuva_acumulada = daily.get("precipitation_sum", [0])[0] if daily.get("precipitation_sum") else 0
        velocidade_vento = hourly.get("windspeed_10m", [0])[0] if hourly.get("windspeed_10m") else 0.0
        rajadas_vento = hourly.get("windgusts_10m", [0])[0] if hourly.get("windgusts_10m") else 0.0
        
        condicao = interpretar_condicao_tempo(weathercode)

        return temperatura, chuva_prob, chuva_acumulada, condicao, velocidade_vento, rajadas_vento
        
    except requests.RequestException as e:
        print(f"⚠️ Erro na API Open-Meteo: {str(e)}")
        return 28.0, 0, 0, "Desconhecido", 0.0, 0.0
    except Exception as e:
        print(f"⚠️ Erro ao conectar com API de clima: {str(e)}")
        return 28.0, 0, 0, "Desconhecido", 0.0, 0.0

def interpretar_condicao_tempo(codigo):
    """
    Converte o código numérico da condição do tempo em uma descrição textual.
    
    Args:
        codigo (int): Código numérico da condição do tempo conforme API Open-Meteo
        
    Returns:
        str: Descrição textual da condição do tempo
            - Se o código não for reconhecido, retorna "Desconhecido"
    """
    mapa = {
        0: "Céu limpo",
        1: "Principalmente limpo",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Névoa",
        48: "Névoa com gelo",
        51: "Garoa leve",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva forte",
        80: "Chuva com pancadas",
        95: "Tempestade"
    }
    return mapa.get(codigo, "Desconhecido")