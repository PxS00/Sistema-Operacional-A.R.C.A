"""
Módulo de Geolocalização

Este módulo contém funções para obter informações de localização a partir de
coordenadas geográficas (latitude e longitude) utilizando a API OpenCage Geocoder.
"""

import requests
from app.core.config import API_KEY

def obter_regiao(lat, lon):
    """
    Obtém informações detalhadas de localização a partir de coordenadas geográficas.
    
    Args:
        lat (float): Latitude da localização
        lon (float): Longitude da localização
        
    Returns:
        tuple: Tupla contendo (rua, bairro, cidade, estado, pais)
            - Se houver erro na requisição, retorna (None, None, None, None, None)
            - Se algum componente não for encontrado, retorna um valor padrão
              (ex: "Rua não identificada")
    
    Raises:
        requests.RequestException: Se houver erro na requisição HTTP
    """
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}",
        "language": "pt",
        "pretty": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta exceção para códigos de erro HTTP

        dados = response.json()
        if dados["results"]:
            componentes = dados["results"][0]["components"]

            # Obtém os componentes da localização com valores padrão caso não encontrados
            rua     = componentes.get("road") or "Rua não identificada"
            bairro  = componentes.get("neighbourhood") or componentes.get("suburb") or "Bairro não identificado"
            cidade  = componentes.get("city") or componentes.get("town") or componentes.get("village") or "Cidade não identificada"
            estado  = componentes.get("state") or "Estado não identificado"
            pais    = componentes.get("country") or "País não identificado"

            print(f"📍 Localização: Rua: {rua}, Bairro: {bairro}, Cidade: {cidade}, Estado: {estado}, {pais}")
            return rua, bairro, cidade, estado, pais

    except requests.RequestException as e:
        print(f"⚠️ Erro ao obter a localização: {str(e)}")
        return None, None, None, None, None
