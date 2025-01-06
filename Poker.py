import streamlit as st
from datetime import datetime, timedelta
import time
import pygame

# Inicializar som
pygame.mixer.init()
ALARM_SOUND = "alarm.mp3"  # Substitua pelo caminho do som desejado, se necessário

# Configuração inicial do app
st.set_page_config(page_title="Organizador de Poker", layout="wide")

# Inicializar sessão de dados
if "players" not in st.session_state:
    st.session_state.players = []
if "tables" not in st.session_state:
    st.session_state.tables = {"Mesa 1": []}
if "blind_timer" not in st.session_state:
    st.session_state.blind_timer = None
if "current_blind" not in st.session_state:
    st.session_state.current_blind = {"tempo": 0, "valor": ""}
if "eliminated_players" not in st.session_state:
    st.session_state.eliminated_players = []
if "chip_values" not in st.session_state:
    st.session_state.chip_values = {"Branco": 1, "Vermelho": 5, "Azul": 10, "Verde": 25, "Preto": 100}

# Função para tocar som
def play_sound():
    pygame.mixer.music.load(ALARM_SOUND)
    pygame.mixer.music.play()

# Layout principal
st.title("Organizador de Poker")

# Configuração dos valores das fichas
st.subheader("Configuração de Valores das Fichas")
with st.form("config_chip_values"):
    st.write("Defina os valores das fichas:")
    branco = st.number_input("Branco", min_value=1, value=st.session_state.chip_values.get("Branco", 1))
    vermelho = st.number_input("Vermelho", min_value=1, value=st.session_state.chip_values.get("Vermelho", 5))
    azul = st.number_input("Azul", min_value=1, value=st.session_state.chip_values.get("Azul", 10))
    verde = st.number_input("Verde", min_value=1, value=st.session_state.chip_values.get("Verde", 25))
    preto = st.number_input("Preto", min_value=1, value=st.session_state.chip_values.get("Preto", 100))

    submitted = st.form_submit_button("Salvar Valores")
    if submitted:
        st.session_state.chip_values = {
            "Branco": branco,
            "Vermelho": vermelho,
            "Azul": azul,
            "Verde": verde,
            "Preto": preto,
        }
        st.success("Valores das fichas salvos com sucesso!")

# Mostrar legenda atual das fichas
st.subheader("Legenda de Fichas")
for color, value in st.session_state.chip_values.items():
    st.write(f"{color}: {value} pontos")

# Seção: Jogadores
st.subheader("Jogadores")
new_player = st.text_input("Adicionar Jogador")
if st.button("Adicionar Jogador") and new_player:
    st.session_state.players.append(new_player)
    st.success(f"Jogador {new_player} adicionado!")

if st.session_state.players:
    st.write("Jogadores Registrados:")
    st.write(", ".join(st.session_state.players))

# Seção: Mesas
st.subheader("Mesas")
num_tables = st.number_input("Número de Mesas", min_value=1, value=len(st.session_state.tables))
if st.button("Atualizar Mesas"):
    st.session_state.tables = {f"Mesa {i+1}": [] for i in range(num_tables)}

for table, players in st.session_state.tables.items():
    st.write(f"**{table}**")
    assigned_players = st.multiselect(f"Jogadores em {table}", st.session_state.players, default=players)
    st.session_state.tables[table] = assigned_players

# Seção: Timer de Blinds
st.subheader("Timer de Blinds")
blind_time = st.number_input("Tempo do Blind (em minutos)", min_value=1, value=5)
blind_value = st.text_input("Valor do Blind Atual")

if st.button("Iniciar Blind"):
    st.session_state.current_blind = {"tempo": blind_time, "valor": blind_value}
    st.session_state.blind_timer = datetime.now() + timedelta(minutes=blind_time)

if st.session_state.blind_timer:
    time_left = (st.session_state.blind_timer - datetime.now()).total_seconds()
    if time_left > 0:
        st.write(f"Tempo restante: {int(time_left // 60)}m {int(time_left % 60)}s")
        time.sleep(1)
    else:
        st.warning("Blind finalizado!")
        play_sound()
        st.session_state.blind_timer = None

# Seção: Eliminações
st.subheader("Eliminações")
eliminated_player = st.selectbox("Selecionar Jogador Eliminado", st.session_state.players)
if st.button("Registrar Eliminação"):
    if eliminated_player not in st.session_state.eliminated_players:
        st.session_state.eliminated_players.append(eliminated_player)
        st.success(f"Jogador {eliminated_player} eliminado!")

if st.session_state.eliminated_players:
    st.write("Jogadores Eliminados:")
    st.write(", ".join(st.session_state.eliminated_players))
