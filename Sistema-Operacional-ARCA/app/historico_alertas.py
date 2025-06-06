"""
Módulo de Histórico de Alertas

Este módulo gerencia o histórico de alertas do sistema ARCA, incluindo:
- Registro de novos alertas
- Verificação de alertas duplicados
- Visualização do histórico de alertas
"""

from app.api.geolocalizacao import obter_regiao

# Lista que armazena o histórico de alertas
historico_alertas = []

def registrar_alerta(alerta):
    """
    Registra um novo alerta no histórico, evitando duplicatas.
    
    Args:
        alerta (dict): Dicionário contendo os dados do alerta a ser registrado
            - id: Identificador único do alerta
            - tipo: Tipo do alerta
            - nivel: Nível de severidade
            - descricao: Descrição do alerta
            - data_emissao: Data e hora de emissão
            - bairro: Bairro afetado
            - cidade: Cidade afetada
    
    Returns:
        None: A função apenas adiciona o alerta à lista historico_alertas
    """
    if not alerta_ja_registrado(alerta):
        historico_alertas.append(alerta)

def alerta_ja_registrado(alerta):
    """
    Verifica se um alerta já está registrado no histórico.
    
    Args:
        alerta (dict): Dicionário contendo os dados do alerta a ser verificado
        
    Returns:
        bool: True se o alerta já estiver registrado, False caso contrário
    """
    for alerta_existente in historico_alertas:
        if alerta_existente['id'] == alerta['id']:
            return True
    return False

def menu_historico_alertas(usuario_logado):
    """
    Exibe o histórico de alertas registrados no sistema.
    
    Args:
        usuario_logado (dict): Dicionário contendo os dados do usuário atualmente logado
        
    Returns:
        None: A função apenas exibe as informações na tela
    """
    try:
        print('\n~~~~ Histórico de Alertas ~~~~')
        
        if not historico_alertas:
            print('Nenhum alerta registrado.')
            input("\nPressione Enter para continuar...")
            return
            
        # Obtém a localização do usuário
        _, _, cidade_usuario, _, _ = obter_regiao(usuario_logado['lat'], usuario_logado['lon'])
            
        # Filtra alertas por cidade se não for administrador
        alertas_filtrados = []
        if usuario_logado['perfil'] != 'Administrador':
            for alerta in historico_alertas:
                if alerta['cidade'].lower() == cidade_usuario.lower():
                    alertas_filtrados.append(alerta)
        else:
            alertas_filtrados = historico_alertas
            
        if not alertas_filtrados:
            print('Nenhum alerta registrado para sua região.')
            input("\nPressione Enter para continuar...")
            return
            
        # Ordena alertas por data (mais recentes primeiro)
        alertas_filtrados.sort(key=lambda x: x['data_emissao'], reverse=True)
        
        for alerta in alertas_filtrados:
            print(f'\nEmitido em: {alerta["data_emissao"]}')
            print(f'⚠️ {alerta["tipo"]} - {alerta["nivel"]}')
            print(f'Local: {alerta["bairro"]}, {alerta["cidade"]}')
            print(f'{alerta["descricao"]}')
            print('-' * 50)
            
        input("\nPressione Enter para continuar...")
        
    except Exception as e:
        print(f"Erro ao exibir histórico de alertas: {e}")
        input("\nPressione Enter para continuar...")
