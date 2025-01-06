import streamlit as st
from datetime import datetime, timedelta
import time
import pygame
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração do Google Sheets
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'  # Nome do arquivo JSON baixado
SHEET_NAME = 'Poker Data'  # Nome da sua planilha no Google Sheets

def init_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        sheet = client.create(SHEET_NAME)
    return sheet

sheet = init_google_sheets()
chip_worksheet = sheet.worksheet("Fichas") if "Fichas" in [w.title for w in sheet.worksheets()] else sheet.add_worksheet("Fichas", 10, 2)

# Inicializar som
pygame.mixer.init()
ALARM_SOUND = "alarm.mp3"  # Adicione o caminho do som desejado.

# Configuração inicial
st.set_page_config(page_title="Organizador de Poker", layout="wide")

# Sessão inicial para armazenar dados
if "chip_values" not in st.session_state:
    st.session_state.chip_values = {"Branco": 1, "Vermelho": 5, "Azul": 10, "Verde": 25, "Preto": 100}

# Função para tocar som
def play_sound():
    pygame.mixer.music.load(ALARM_SOUND)
    pygame.mixer.music.play()

# Função para salvar valores das fichas no Google Sheets
def save_chip_values(chip_values):
    chip_worksheet.clear()
    for color, value in chip_values.items():
        chip_worksheet.append_row([color, value])

# Função para carregar valores das fichas do Google Sheets
def load_chip_values():
    chip_values = {}
    for row in chip_worksheet.get_all_values():
        if len(row) == 2:
            chip_values[row[0]] = int(row[1])
    return chip_values

# Carregar valores de fichas salvos
if chip_worksheet.get_all_values():
    st.session_state.chip_values = load_chip_values()

# Layout principal
st.title("Organizador de Poker")

# Seção: Configuração de valores das fichas
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
        save_chip_values(st.session_state.chip_values)
        st.success("Valores das fichas salvos com sucesso!")

# Mostrar legenda atual das fichas
st.subheader("Legenda de Fichas")
for color, value in st.session_state.chip_values.items():
    st.write(f"{color}: {value} pontos")
