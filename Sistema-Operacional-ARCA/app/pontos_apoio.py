from app.api.geolocalizacao import obter_regiao
from math import radians, sin, cos, sqrt, atan2
from app.core.utils import validar_input_float
import re

# Constantes
RAIO_TERRA = 6371  # Raio da Terra em km
RAIO_PROXIMO = 5   # Raio para pontos próximos em km
RAIO_DISTANTE = 50 # Raio para pontos distantes em km

'''Simulação de dados vindos do Java'''
pontos_apoio = [
    {'id': 1, 'nome': 'Centro Comunitário Paulista', 'bairro': 'Bela Vista', 'rua': 'Av. Paulista, 1000', 'cidade': 'São Paulo', 'estado': 'SP', 'pais': 'Brasil', 'capacidade': 800, 'telefone': '+55 11 3333-4444', 'status': 'Aprovado', 'lat': -23.5689, 'lon': -46.6423, 'observacoes': 'Observações: O ponto de apoio aceita animais, possui acesso para deficientes físicos e cadeiras de rodas.'},
    {'id': 2, 'nome': 'Igreja de São Paulo', 'bairro': 'Pinheiros', 'rua': 'Rua Mourato Coelho', 'cidade': 'São Paulo', 'estado': 'SP', 'pais': 'Brasil', 'capacidade': 300, 'telefone': '11999998888', 'status': 'Aprovado', 'lat': -23.5605, 'lon': -46.6533, 'observacoes': 'Observações: O ponto de apoio não aceita animais.'},
    {'id': 3, 'nome': 'Escola Primária Maputo', 'bairro': 'Sommerschield', 'rua': 'Av. Eduardo Mondlane', 'cidade': 'Maputo', 'estado': 'Maputo', 'pais': 'Moçambique', 'capacidade': 450, 'telefone': '+258 21 123 456', 'status': 'Aprovado', 'lat': -25.9753, 'lon': 32.5992, 'observacoes': 'Observações: O ponto de apoio não aceita animais.'},
    {'id': 4, 'nome': 'Centro Cultural Paris 14', 'bairro': 'Montparnasse', 'rua': 'Rue de la Gaité', 'cidade': 'Paris', 'estado': 'Île-de-France', 'pais': 'França', 'capacidade': 250, 'telefone': '+33 1 42 18 88 88', 'status': 'Aprovado', 'lat': 48.9566, 'lon': 2.4522, 'observacoes': 'Observações: O ponto de apoio está localizado na região de Montparnasse, próximo ao Museu de Arte Moderna e ao Museu de Arte Contemporânea.'},
    {'id': 5, 'nome': 'Estádio Nacional de Lima', 'bairro': 'Santa Beatriz', 'rua': 'Av. Paseo de la República', 'cidade': 'Lima', 'estado': 'Lima', 'pais': 'Peru', 'capacidade': 1000, 'telefone': '+51 1 555 0000', 'status': 'Aprovado', 'lat': -12.0564, 'lon': -77.0528, 'observacoes': 'Observações: Possuí acesso para deficientes físicos.'}
]

def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula a distância aproximada entre dois pontos usando a fórmula de Haversine
    Retorna a distância em quilômetros
    """
    try:
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distancia = RAIO_TERRA * c
        
        return round(distancia, 1)  # Arredonda para 1 casa decimal
    except Exception as e:
        print(f"Erro ao calcular distância: {e}")
        return float('inf')

def ver_detalhes(id, usuario_logado):
    """
    Mostra os detalhes de um ponto de apoio específico
    
    Args:
        id (int): ID do ponto de apoio
        usuario_logado (dict): Dicionário com dados do usuário logado
        
    Returns:
        dict: Dicionário com dados do ponto de apoio ou None se não encontrado
    """
    try:
        for ponto in pontos_apoio:
            if ponto['id'] == id:
                # Verifica se é administrador ou se o ponto está aprovado
                if usuario_logado['perfil'] != 'Administrador' and ponto['status'] != 'Aprovado':
                    print("⚠️ Acesso restrito. Apenas administradores podem ver pontos pendentes.")
                    return None
                    
                print("\n📍 Detalhes do Ponto de Apoio")
                print(f"Nome: {ponto['nome']}")
                print(f"Endereço: {ponto['rua']}, {ponto['bairro']}")
                print(f"Cidade: {ponto['cidade']} - {ponto['estado']}, {ponto['pais']}")
                print(f"Capacidade: {ponto['capacidade']} pessoas")
                print(f"Telefone: {ponto['telefone']}")
                print(f"Status: {ponto['status']}")
                print(f"Observações: {ponto.get('observacoes', '—')}")
                return ponto
        print("⚠️ Ponto de apoio não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao mostrar detalhes: {e}")
        return None

def validar_telefone(telefone):
    """
    Valida o formato do número de telefone.
    
    Args:
        telefone (str): Número de telefone a ser validado
        
    Returns:
        bool: True se o telefone for válido, False caso contrário
    """
    # Remove caracteres não numéricos
    telefone = re.sub(r'\D', '', telefone)
    
    # Verifica se tem entre 10 e 15 dígitos (incluindo DDD e código do país)
    if len(telefone) < 10 or len(telefone) > 15:
        return False
    
    return True

def validar_capacidade(capacidade):
    """
    Valida a capacidade do ponto de apoio.
    
    Args:
        capacidade (str): Capacidade a ser validada
        
    Returns:
        int: Capacidade validada ou None se inválida
    """
    try:
        cap = int(capacidade)
        if cap <= 0:
            print("⚠️ A capacidade deve ser maior que zero.")
            return None
        if cap > 10000:
            print("⚠️ A capacidade não pode ser maior que 10.000 pessoas.")
            return None
        return cap
    except ValueError:
        print("⚠️ Por favor, digite um número válido.")
    return None

def validar_coordenadas(lat, lon):
    """
    Valida as coordenadas geográficas.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        
    Returns:
        bool: True se as coordenadas forem válidas, False caso contrário
    """
    if not (-90 <= lat <= 90):
        print("⚠️ Latitude inválida. Deve estar entre -90 e 90.")
        return False
    if not (-180 <= lon <= 180):
        print("⚠️ Longitude inválida. Deve estar entre -180 e 180.")
        return False
    return True

def cadastrar_ponto_apoio():
    """
    Cadastra um novo ponto de apoio no sistema
    """
    try:
        print("\n~~~ Cadastro de Novo Ponto de Apoio ~~~")
        
        # Gera um novo ID
        novo_id = max(p['id'] for p in pontos_apoio) + 1
        
        # Validação do nome
        while True:
            nome = input("Nome do ponto de apoio: ").strip()
            if len(nome) >= 3:
                break
            print("⚠️ O nome deve ter pelo menos 3 caracteres.")
        
        # Validação do bairro
        while True:
            bairro = input("Bairro: ").strip()
            if len(bairro) >= 2:
                break
            print("⚠️ O bairro deve ter pelo menos 2 caracteres.")
        
        # Validação da rua
        while True:
            rua = input("Rua: ").strip()
            if len(rua) >= 3:
                break
            print("⚠️ A rua deve ter pelo menos 3 caracteres.")
        
        # Validação da cidade
        while True:
            cidade = input("Cidade: ").strip()
            if len(cidade) >= 2:
                break
            print("⚠️ A cidade deve ter pelo menos 2 caracteres.")
        
        # Validação do estado
        while True:
            estado = input("Estado: ").strip()
            if len(estado) >= 2:
                break
            print("⚠️ O estado deve ter pelo menos 2 caracteres.")
        
        # Validação do país
        while True:
            pais = input("País: ").strip()
            if len(pais) >= 2:
                break
            print("⚠️ O país deve ter pelo menos 2 caracteres.")
        
        # Validação da capacidade
        while True:
            capacidade = validar_capacidade(input("Capacidade (número de pessoas): "))
            if capacidade is not None:
                break
        
        # Validação do telefone
        while True:
            telefone = input("Telefone: ").strip()
            if validar_telefone(telefone):
                break
            print("⚠️ Telefone inválido. Use o formato: +XX (DDD) XXXX-XXXX")
        
        # Validação das coordenadas
        while True:
            lat = validar_input_float("Latitude: ")
            lon = validar_input_float("Longitude: ")
            if validar_coordenadas(lat, lon):
                break
        
        # Observações (opcional)
        observacoes = input("Observações: ").strip()
        
        novo_ponto = {
            'id': novo_id,
            'nome': nome,
            'bairro': bairro,
            'rua': rua,
            'cidade': cidade,
            'estado': estado,
            'pais': pais,
            'capacidade': capacidade,
            'telefone': telefone,
            'status': 'Pendente',
            'lat': lat,
            'lon': lon,
            'observacoes': f"Observações: {observacoes}" if observacoes else "Observações: —"
        }
        
        pontos_apoio.append(novo_ponto)
        print("\n✅ Ponto de apoio cadastrado com sucesso!")
        print("Status: Pendente de aprovação")
        return novo_ponto
        
    except Exception as e:
        print(f"Erro ao cadastrar ponto de apoio: {e}")
        return None

def menu_pontos_apoio(usuario_logado):
    """
    Menu principal para busca e visualização de pontos de apoio
    """
    try:
        while True:
            print("\n~~~ Menu de Pontos de Apoio ~~~")
            print("1. Buscar pontos próximos")
            print("2. Cadastrar novo ponto")
            if usuario_logado['perfil'] == 'Administrador':
                print("3. Ver todos os pontos de apoio")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "0":
                break
            elif opcao == "1":
                lat = usuario_logado['lat']
                lon = usuario_logado['lon']
                rua, bairro, cidade, estado, pais = obter_regiao(lat, lon)

                print(f"\n🔎 Buscando pontos de apoio aprovados próximos a você...")
                print(f"Localização atual: {bairro}, {cidade} - {estado}, {pais}\n")

                encontrados = []
                pontos_proximos = []
                pontos_distantes = []

                for p in pontos_apoio:
                    # Se não for admin, só mostra pontos aprovados
                    if usuario_logado['perfil'] != 'Administrador' and p['status'] != 'Aprovado':
                        continue
                        
                    distancia = calcular_distancia(lat, lon, p['lat'], p['lon'])
                    ponto_info = {
                        'id': p['id'],
                        'nome': p['nome'],
                        'rua': p['rua'],
                        'distancia': distancia,
                        'capacidade': p['capacidade']
                    }
                    
                    if distancia <= RAIO_PROXIMO:
                        pontos_proximos.append(ponto_info)
                    elif distancia <= RAIO_DISTANTE:
                        pontos_distantes.append(ponto_info)
                    encontrados.append(p['id'])

                if pontos_proximos:
                    print("📍 Pontos próximos (até 5km):")
                    for p in sorted(pontos_proximos, key=lambda x: x['distancia']):
                        print(f"[{p['id']}] {p['nome']} — {p['rua']} | Distância: {p['distancia']}km | Capacidade: {p['capacidade']}")

                if pontos_distantes:
                    print("\n📍 Pontos mais distantes (até 50km):")
                    for p in sorted(pontos_distantes, key=lambda x: x['distancia']):
                        print(f"[{p['id']}] {p['nome']} — {p['rua']} | Distância: {p['distancia']}km | Capacidade: {p['capacidade']}")

                if not encontrados:
                    print("Nenhum ponto de apoio encontrado próximo a você.")
                    continue

                try:
                    escolha = int(input("\nDigite o ID do ponto para ver detalhes ou 0 para voltar: "))
                    if escolha == 0:
                        continue
                    if escolha in encontrados:
                        ver_detalhes(escolha, usuario_logado)
                        input("\nPressione Enter para continuar...")
                    else:
                        print("⚠️ ID inválido.")
                        input("\nPressione Enter para continuar...")
                except ValueError:
                    print("⚠️ Por favor, digite um número válido.")
                    input("\nPressione Enter para continuar...")
            
            elif opcao == "2":
                cadastrar_ponto_apoio()
                input("\nPressione Enter para continuar...")
                
            elif opcao == "3" and usuario_logado['perfil'] == 'Administrador':
                print("\n~~~ Todos os Pontos de Apoio ~~~")
                for p in pontos_apoio:
                    print(f"[{p['id']}] {p['nome']} — {p['rua']} | Status: {p['status']}")
                
                try:
                    escolha = int(input("\nDigite o ID do ponto para ver detalhes ou 0 para voltar: "))
                    if escolha == 0:
                        continue
                    ver_detalhes(escolha, usuario_logado)
                    input("\nPressione Enter para continuar...")
                except ValueError:
                    print("⚠️ Por favor, digite um número válido.")
                    input("\nPressione Enter para continuar...")
            else:
                print("⚠️ Opção inválida!")
                input("\nPressione Enter para continuar...")
                
    except Exception as e:
        print(f"Erro no menu de pontos de apoio: {e}")
        input("\nPressione Enter para continuar...")