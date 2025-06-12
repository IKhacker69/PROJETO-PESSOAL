from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import uuid # Módulo para gerar IDs únicos

app = Flask(__name__)

# --- Dados simulados em memória ---
# Estes dados serão perdidos quando o servidor for reiniciado!

# Dicionário de serviços disponíveis
servicos = {
    "1": {
        "nome": "Corte de Cabelo",
        "descricao": "Corte moderno para homens e mulheres.",
        "duracao_minutos": 30
    },
    "2": {
        "nome": "Manicure e Pedicure",
        "descricao": "Unhas impecáveis para mãos e pés.",
        "duracao_minutos": 60
    },
    "3": {
        "nome": "Massagem Relaxante",
        "descricao": "Sessão de massagem de corpo inteiro.",
        "duracao_minutos": 90
    }
}

# Lista de agendamentos. Cada agendamento é um dicionário.
agendamentos = []

# Dicionário para simular a disponibilidade de um "provedor" de serviço
# Horários fixos para cada dia da semana (0=Segunda, 6=Domingo)
disponibilidade_provedor = {
    0: [("09:00", "17:00")],  # Segunda-feira
    1: [("09:00", "17:00")],  # Terça-feira
    2: [("09:00", "17:00")],  # Quarta-feira
    3: [("09:00", "17:00")],  # Quinta-feira
    4: [("09:00", "17:00")],  # Sexta-feira
    5: [("10:00", "14:00")],  # Sábado (horário reduzido)
    6: []                    # Domingo (fechado)
}

# Lista para armazenar usuários (simulando um banco de dados de usuários)
usuarios_cadastrados = []
# --- Fim dos Dados simulados em memória ---


# --- Funções Auxiliares ---
def get_slot_end_time(start_time_str, duration_minutes):
    """Calcula o horário de término de um slot."""
    start_dt = datetime.strptime(start_time_str, "%H:%M")
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    return end_dt.strftime("%H:%M")

def is_slot_available(target_date_str, target_start_time_str, duration_minutes):
    """
    Verifica se um slot específico está disponível,
    considerando agendamentos existentes e disponibilidade do provedor.
    """
    target_datetime_start = datetime.strptime(f"{target_date_str} {target_start_time_str}", "%Y-%m-%d %H:%M")
    target_datetime_end = target_datetime_start + timedelta(minutes=duration_minutes)

    # 1. Verificar disponibilidade do provedor (horários de trabalho)
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    dia_semana_num = target_date.weekday() # Retorna 0 para segunda, 6 para domingo

    horarios_trabalho_dia = disponibilidade_provedor.get(dia_semana_num, [])

    if not horarios_trabalho_dia:
        return False # Provedor não trabalha neste dia

    disponivel_no_horario_geral = False
    for inicio_trabalho_str, fim_trabalho_str in horarios_trabalho_dia:
        inicio_trabalho_dt = datetime.strptime(f"{target_date_str} {inicio_trabalho_str}", "%Y-%m-%d %H:%M")
        fim_trabalho_dt = datetime.strptime(f"{target_date_str} {fim_trabalho_str}", "%Y-%m-%d %H:%M")

        # Verifica se o slot desejado está dentro do horário de trabalho do provedor
        if (target_datetime_start >= inicio_trabalho_dt and
            target_datetime_end <= fim_trabalho_dt):
            disponivel_no_horario_geral = True
            break # Encontrou um bloco de horário de trabalho que acomoda o agendamento
    
    if not disponivel_no_horario_geral:
        return False # O slot não está dentro do horário de trabalho do provedor

    # 2. Verificar conflito com agendamentos existentes
    for agendamento_existente in agendamentos:
        # Ignora agendamentos cancelados para verificação de conflito
        if agendamento_existente.get('status') == 'cancelado':
            continue

        existente_date_str = agendamento_existente['data']
        existente_start_time_str = agendamento_existente['hora_inicio']
        existente_end_time_str = agendamento_existente['hora_fim']

        # Se for no mesmo dia
        if existente_date_str == target_date_str:
            existente_datetime_start = datetime.strptime(f"{existente_date_str} {existente_start_time_str}", "%Y-%m-%d %H:%M")
            existente_datetime_end = datetime.strptime(f"{existente_date_str} {existente_end_time_str}", "%Y-%m-%d %H:%M")

            # Verifica se há sobreposição de horários
            # (Se o novo agendamento começa antes do existente e termina depois do existente
            # OU se o novo agendamento começa durante o existente
            # OU se o novo agendamento termina durante o existente)
            if not (target_datetime_end <= existente_datetime_start or
                    target_datetime_start >= existente_datetime_end):
                return False # Há um conflito

    return True # Slot está disponível

# --- Rotas da API ---

@app.route('/')
def home():
    return 'Bem-vindo à API de Agendamentos em Flask (Dados na Memória)!'



## Rotas de Autenticação (Login/Registro)

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    """
    Registra um novo usuário.
    Requer no corpo da requisição JSON: 'username', 'password'
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"erro": "Username e password são obrigatórios."}), 400

    # Verifica se o username já existe
    for user in usuarios_cadastrados:
        if user['username'] == username:
            return jsonify({"erro": "Username já existe. Escolha outro."}), 409 # Conflict

    # Adiciona o novo usuário à lista
    novo_usuario = {
        "id": str(uuid.uuid4()), # Gera um ID único
        "username": username,
        "password": password # ATENÇÃO: Em um sistema real, a senha seria HASHED por segurança!
    }
    usuarios_cadastrados.append(novo_usuario)

    return jsonify({"mensagem": "Usuário registrado com sucesso!", "user_id": novo_usuario['id']}), 201

@app.route('/login', methods=['POST'])
def login_usuario():
    """
    Autentica um usuário.
    Requer no corpo da requisição JSON: 'username', 'password'
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"erro": "Username e password são obrigatórios."}), 400

    # Procura o usuário na lista
    for user in usuarios_cadastrados:
        if user['username'] == username and user['password'] == password:
            # Em um sistema real, você geraria um token JWT ou uma sessão aqui para manter o login
            return jsonify({"mensagem": "Login bem-sucedido!", "user_id": user['id'], "username": user['username']}), 200
    
    return jsonify({"erro": "Username ou senha incorretos."}), 401 # Unauthorized



## Rotas de Serviços

@app.route('/servicos', methods=['GET'])
def listar_servicos():
    """
    Retorna todos os serviços disponíveis.
    """
    lista_servicos = []
    for id_servico, detalhes in servicos.items():
        servico_com_id = detalhes.copy()
        servico_com_id['id'] = id_servico
        lista_servicos.append(servico_com_id)
    return jsonify(lista_servicos)


## Rotas de Agendamentos e Disponibilidade

@app.route('/disponibilidade/<string:servico_id>', methods=['GET'])
def obter_disponibilidade(servico_id):
    """
    Retorna os horários disponíveis para um serviço em uma data específica.
    Parâmetro de query na URL: ?data=YYYY-MM-DD
    Ex: /disponibilidade/1?data=2025-06-12
    """
    data_str = request.args.get('data') # Obtém a data da URL (query parameter)

    if not data_str:
        return jsonify({"erro": "Parâmetro 'data' é obrigatório (formato YYYY-MM-DD)."}), 400

    if servico_id not in servicos:
        return jsonify({"erro": "Serviço não encontrado."}), 404

    servico = servicos[servico_id]
    duracao_servico = servico['duracao_minutos']

    try:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    dia_semana_num = data_obj.weekday() # 0=Segunda, 6=Domingo

    horarios_trabalho_dia = disponibilidade_provedor.get(dia_semana_num, [])
    
    if not horarios_trabalho_dia:
        return jsonify({"disponivel": []}) # Nenhuma disponibilidade para este dia

    slots_disponiveis = []

    for inicio_trabalho_str, fim_trabalho_str in horarios_trabalho_dia:
        current_slot_start = datetime.strptime(f"{data_str} {inicio_trabalho_str}", "%Y-%m-%d %H:%M")
        fim_trabalho_dt = datetime.strptime(f"{data_str} {fim_trabalho_str}", "%Y-%m-%d %H:%M")

        # Gerar slots em intervalos de 15 minutos para maior flexibilidade
        # A função is_slot_available vai garantir que o slot completo do serviço caiba
        intervalo_geracao_slots = 15 # minutos
        while current_slot_start + timedelta(minutes=duracao_servico) <= fim_trabalho_dt:
            slot_start_time_str = current_slot_start.strftime("%H:%M")
            
            if is_slot_available(data_str, slot_start_time_str, duracao_servico):
                slots_disponiveis.append({
                    "hora_inicio": slot_start_time_str,
                    "hora_fim": (current_slot_start + timedelta(minutes=duracao_servico)).strftime("%H:%M")
                })
            
            current_slot_start += timedelta(minutes=intervalo_geracao_slots)


    return jsonify({"disponivel": slots_disponiveis})


@app.route('/agendar', methods=['POST'])
def agendar_servico():
    """
    Cria um novo agendamento.
    Requer no corpo da requisição JSON: 'servico_id', 'data' (YYYY-MM-DD), 'hora_inicio' (HH:MM), 'cliente_nome'
    """
    data = request.json
    servico_id = data.get('servico_id')
    data_agendamento_str = data.get('data')
    hora_inicio_agendamento_str = data.get('hora_inicio')
    cliente_nome = data.get('cliente_nome') # Em um sistema real, este viria do usuário logado (via token)

    if not all([servico_id, data_agendamento_str, hora_inicio_agendamento_str, cliente_nome]):
        return jsonify({"erro": "Dados incompletos. Requer: servico_id, data, hora_inicio, cliente_nome."}), 400

    if servico_id not in servicos:
        return jsonify({"erro": "Serviço não encontrado."}), 404

    servico = servicos[servico_id]
    duracao_servico = servico['duracao_minutos']
    hora_fim_agendamento_str = get_slot_end_time(hora_inicio_agendamento_str, duracao_servico)

    # VALIDAÇÃO CRÍTICA: Checar disponibilidade na hora de agendar para evitar conflitos simultâneos
    if not is_slot_available(data_agendamento_str, hora_inicio_agendamento_str, duracao_servico):
        return jsonify({"erro": "Horário não disponível. Por favor, escolha outro."}), 409 # Conflict

    # Se estiver disponível, adiciona o agendamento
    novo_agendamento = {
        "id": len(agendamentos) + 1, # ID simples, apenas para este exemplo (não robusto para produção)
        "servico_id": servico_id,
        "cliente_nome": cliente_nome,
        "data": data_agendamento_str,
        "hora_inicio": hora_inicio_agendamento_str,
        "hora_fim": hora_fim_agendamento_str,
        "status": "confirmado" # Status inicial
    }
    agendamentos.append(novo_agendamento)

    return jsonify({"mensagem": "Agendamento realizado com sucesso!", "agendamento": novo_agendamento}), 201

@app.route('/meus_agendamentos', methods=['GET'])
def meus_agendamentos():
    """
    Retorna todos os agendamentos (para simulação).
    Em um sistema real, você filtraria por cliente_id do usuário logado.
    """
    return jsonify(agendamentos)

@app.route('/cancelar_agendamento/<int:agendamento_id>', methods=['POST'])
def cancelar_agendamento(agendamento_id):
    """
    Cancela um agendamento existente.
    """
    for agendamento in agendamentos:
        if agendamento['id'] == agendamento_id:
            if agendamento['status'] == 'cancelado':
                return jsonify({"mensagem": "Agendamento já está cancelado."}), 400
            agendamento['status'] = 'cancelado'
            return jsonify({"mensagem": f"Agendamento {agendamento_id} cancelado com sucesso."}), 200
    return jsonify({"erro": "Agendamento não encontrado."}), 404

# --- Execução do Servidor ---
if __name__ == '__main__':
    # Você pode pré-popular agendamentos ou usuários para testes se quiser,
    # descomentando as linhas abaixo. Lembre-se que eles serão resetados
    # ao reiniciar o servidor.
    # usuarios_cadastrados.append({"id": "abc-123", "username": "teste", "password": "123"})
    # agendamentos.append({
    #     "id": 1,
    #     "servico_id": "1",
    #     "cliente_nome": "João Silva",
    #     "data": "2025-06-12",
    #     "hora_inicio": "10:00",
    #     "hora_fim": "10:30",
    #     "status": "confirmado"
    # })
    app.run(debug=True) # debug=True reinicia o servidor automaticamente ao salvar o código e mostra erros detalhados