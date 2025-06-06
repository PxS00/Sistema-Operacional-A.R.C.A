"""
Módulo de Gerenciamento de Usuários

Este módulo contém as funções e estruturas de dados necessárias para o gerenciamento
de usuários do sistema ARCA, incluindo:
- Lista de usuários
- Visualização de perfis
- Seleção de usuários
- Edição de dados do usuário
"""

# Simula usuários vindos do Java
usuarios = [
    {'id': 1, 'nome': 'Ana Sophia Araújo', 'cpf': '438.150.926-98', 'email': 'anarajo@hotmail.net', 'telefone': '71 6379-4026', 'idade': 58, 'perfil': 'Usuário', 'lat': -23.5575, 'lon': -46.6603},
    {'id': 2, 'nome': 'Samuel Plaça', 'cpf': '518.302.467-71', 'email': 'profsamuel.placa@fiap.com.br', 'telefone': '0900-593-1034', 'idade': 26, 'perfil': 'Administrador', 'lat': -23.5505, 'lon': -46.6333},
    {'id': 3, 'nome': 'Enzo Castro', 'cpf': '647.521.980-02', 'email': 'enzo.castro@gmail.com', 'telefone': '+55 51 2764 8350', 'idade': 33, 'perfil': 'Usuário', 'lat': -25.9653, 'lon': 32.5892},
    {'id': 4, 'nome': 'Aiko Ribeiro', 'cpf': '083.759.162-77', 'email': 'aiko.ribeiro@gmail.com', 'telefone': '(011) 91234-5678', 'idade': 29, 'perfil': 'Usuário', 'lat': 48.8566, 'lon': 2.3522},
    {'id': 5, 'nome': 'Pierre Santos', 'cpf': '651.394.821-66', 'email': 'pierre.santos@ymail.com', 'telefone': '(011) 91235-6789', 'idade': 34, 'perfil': 'Usuário', 'lat': -12.0464, 'lon': -77.0428}
]

def ver_detalhes(id):
    """
    Exibe os detalhes completos de um usuário específico.
    
    Args:
        id (int): ID do usuário a ser visualizado
        
    Returns:
        None: A função apenas exibe as informações na tela
    """
    for usuario in usuarios:
        if usuario['id'] == id:
            print("\nCadastro do Usuário")
            print(f"Nome: {usuario['nome']}")
            print(f"CPF: {usuario['cpf']}")
            print(f"Email: {usuario['email']}")
            print(f"Telefone: {usuario['telefone']}")
            print(f"Idade: {usuario['idade']}")
            print(f"Perfil: {usuario['perfil']}")
            return
    print("Usuário não encontrado.")

def selecionar_usuario():
    """
    Permite ao usuário selecionar um perfil da lista de usuários disponíveis.
    
    Returns:
        dict: Dicionário contendo os dados do usuário selecionado
        None: Se nenhum usuário for selecionado
    """
    print("\n~~~~ Selecionar Usuário ~~~~")
    for u in usuarios:
        print(f"[{u['id']}] {u['nome']} — {u['perfil']}")
    
    while True:
        try:
            id_escolhido = int(input("\nDigite o ID do usuário para selecionar: "))
            for u in usuarios:
                if u['id'] == id_escolhido:
                    return u
            print("⚠️ Usuário não encontrado.")
        except ValueError:
            print("⚠️ Entrada inválida.")

def menu_usuarios(usuario_logado):
    """
    Exibe e gerencia o menu de usuários do sistema.
    
    Args:
        usuario_logado (dict): Dicionário contendo os dados do usuário atualmente logado
        
    Returns:
        dict: Dicionário contendo os dados do usuário atualizado
    """
    while True:
        print("\n~~~~ Menu de Usuários ~~~~")
        print("1 - Ver meu perfil")
        print("2 - Editar meu perfil")
        print("3 - Ver usuários registrados")
        print("4 - Trocar de usuário")
        print("0 - Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            print("\n~~~~ Meu Perfil ~~~~")
            print(f"Nome: {usuario_logado['nome']}")
            print(f"CPF: {usuario_logado['cpf']}")
            print(f"Email: {usuario_logado['email']}")
            print(f"Telefone: {usuario_logado['telefone']}")
            print(f"Idade: {usuario_logado['idade']}")
            print(f"Perfil: {usuario_logado['perfil']}")
            
        elif opcao == "2":
            print("\n~~~~ Editar Perfil ~~~~")
            print("1 - Editar email")
            print("2 - Editar telefone")
            print("0 - Voltar")
            
            edit_opcao = input("\nEscolha o que deseja editar: ")
            
            if edit_opcao == "1":
                novo_email = input("Digite o novo email: ")
                usuario_logado['email'] = novo_email
                print("Email atualizado com sucesso!")
            elif edit_opcao == "2":
                novo_telefone = input("Digite o novo telefone: ")
                usuario_logado['telefone'] = novo_telefone
                print("Telefone atualizado com sucesso!")
                
        elif opcao == "3":
            print("\n~~~~ Usuários Conectados ~~~~")
            encontrados = []
            for u in usuarios:
                print(f"[{u['id']}] {u['nome']} — {u['idade']} anos| {u['perfil']}")
                encontrados.append(u['id'])
            try:
                escolha = int(input("\nDigite o ID do usuário para ver detalhes ou 0 para sair: "))
                if escolha in encontrados:
                    ver_detalhes(escolha)
                elif escolha != 0:
                    print("⚠️ ID inválido.")
            except ValueError:
                print("⚠️ Entrada inválida.")

        elif opcao == "4":
            print("\n~~~~ Trocar de Usuário ~~~~")
            novo_usuario = selecionar_usuario()
            if novo_usuario:
                return novo_usuario
                
        elif opcao == "0":
            return usuario_logado
        else:
            print("⚠️ Opção inválida.")
            
        input("\nPressione Enter para continuar...")


