import streamlit as st
import pandas as pd
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# ----------------------------------------
# CONEXIÓN GOOGLE SHEETS
# ----------------------------------------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key("18D_ctBRRxOSGcHIqdQJ0UmcC1w0valrq9teE6u0q-tQ").sheet1

# ----------------------------------------
# LISTAS
# ----------------------------------------

INSUMOS = [
    "Barras de proteina",
    "Agua",
    "Aguacate",
    "Almendras",
    "Amaranto",
    "Apio",
    "Avena",
    "Azucar",
    "Betabel",
    "Blueberries",
    "Brownies",
    "Café",
    "Caramelo",
    "Chapatas",
    "Chia",
    "Chiles",
    "Chipotle",
    "Crema de cacahuate",
    "Crema pistache",
    "Croissants",
    "Curcuma",
    "Espinaca",
    "Fresa",
    "Frutos Rojos",
    "Frutos secos",
    "Galletas colorado",
    "Galletas Costco",
    "Gomitas",
    "Granola",
    "Hielo",
    "Hierbas finas",
    "Jamon",
    "Jengibre",
    "Jitomate",
    "Leche Carnation",
    "Leche",
    "Leche de almendras",
    "Leche proteina",
    "Lechuga",
    "Limon",
    "Linaza",
    "Mango",
    "Mantequilla",
    "Manzana",
    "Matcha",
    "Mayonesa",
    "Miel",
    "Muffins",
    "Naranja",
    "Nesquick",
    "Nopal",
    "Nuez",
    "Nutella",
    "Pan Sandwich",
    "Pancho Pan",
    "Papaya",
    "Pechuga de pavo",
    "Pepino",
    "Pina",
    "Platano",
    "Queso de cabra",
    "Queso mozzarella",
    "Queso panela",
    "Queso suizo",
    "Salsita",
    "Sirope (maple)",
    "Stevia",
    "Toronja",
    "Vainilla",
    "Wafles",
    "Yogurth",
    "Zanahoria"
]

OPERATIVOS = [
    "Aluminio",
    "Bolsas Basura",
    "Bolsas chiles",
    "Bolsas Kraft",
    "Bolsas grandes",
    "Charolas RB160",
    "Charolas portavasos",
    "Gasolina",
    "Luz",
    "Internet",
    "Servicio de agua",
    "Renta",
    "Nómina",
    "Detergente",
    "Papel cuadriculado",
    "Popotes",
    "Publicidad",
    "Servilletas",
    "Spotify",
    "Vehiculo",
    "Recoleccion Basura",
    "Telefono",
    "Vasos chicos",
    "Vasos grandes",
    "Vasos latte",
    "Vasos cafe",
    "Vasitos salsita",
    "Otro"
]

# ----------------------------------------
# INTERFAZ
# ----------------------------------------

st.title("Control de Gastos Jugo Bonito")

st.subheader("Registrar nuevo gasto")

# FECHA
fecha = st.date_input(
    "Fecha",
    datetime.today()
)

# TIPO DE GASTO
tipo_gasto = st.selectbox(
    "Tipo de gasto",
    ["Insumo", "Operativo"]
)

# CONCEPTO
if tipo_gasto == "Insumo":

    concepto = st.selectbox(
        "Producto",
        INSUMOS
    )

else:

    concepto = st.selectbox(
        "Concepto",
        OPERATIVOS
    )

# MONTO
monto = st.number_input(
    "Monto",
    min_value=0.0,
    step=1.0
)

# MÉTODO DE PAGO
metodo_pago = st.selectbox(
    "Método de pago",
    [
        "Efectivo",
        "Tarjeta",
        "Transferencia"
    ]
)

# COMENTARIOS
comentarios = st.text_area(
    "Comentarios"
)

# ----------------------------------------
# GUARDAR GASTO
# ----------------------------------------

if st.button("Guardar gasto"):

    try:

        fila = [
            str(fecha),
            tipo_gasto,
            concepto,
            monto,
            metodo_pago,
            comentarios
        ]

        sheet.append_row(
            fila,
            value_input_option="USER_ENTERED",
            insert_data_option="INSERT_ROWS"
        )

        st.success("Gasto guardado correctamente")

        st.rerun()

    except Exception as e:

        st.error("Ocurrió un error al guardar:")
        st.exception(e)

# ----------------------------------------
# MOSTRAR ÚLTIMO GASTO
# ----------------------------------------

st.subheader("Último gasto registrado")

ultimo_gasto = st.session_state.get("ultimo_gasto")

if ultimo_gasto:

    st.write(f"**Fecha:** {ultimo_gasto[0]}")
    st.write(f"**Tipo:** {ultimo_gasto[1]}")
    st.write(f"**Concepto:** {ultimo_gasto[2]}")
    st.write(f"**Monto:** ${float(ultimo_gasto[3]):,.2f}")
    st.write(f"**Método de pago:** {ultimo_gasto[4]}")

    if len(ultimo_gasto) > 5 and ultimo_gasto[5]:
        st.write(f"**Comentarios:** {ultimo_gasto[5]}")

else:

    st.info("Registra un gasto para verlo aquí.")