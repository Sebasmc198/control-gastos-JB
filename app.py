import streamlit as st
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
import os

# CONFIGURACIÓN
ARCHIVO_EXCEL = "gastos.xlsx"

# TÍTULO
st.title("Control de Gastos Jugo Bonito")

st.subheader("Registrar nuevo gasto")

# FECHA
fecha = st.date_input("Fecha", datetime.today())

# TIPO DE GASTO
tipo_gasto = st.selectbox(
    "Tipo de gasto",
    ["Insumo", "Operativo"]
)

# CONCEPTO
if tipo_gasto == "Insumo":
    concepto = st.selectbox(
        "Producto",
        [
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
  "Leche Carnetion", 
  "Leche",  
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
  "Toronja",  
  "Wafles",  
  "Yogurth",  
  "Zanahoria",  
        ]
    )
else:
    concepto = st.selectbox(
        "Concepto",
        [
            "Gasolina",
            "Luz",
            "Internet",
            "Servicio de agua"
            "Renta",
            "Nómina",
            "Detergente",
            "Publicidad",
            "Spotify",
            "Vehiculo",
            "Recoleccion Basura",
            "Telefono",
            "Otro"
        ]
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
comentarios = st.text_area("Comentarios")

# BOTÓN
if st.button("Guardar gasto"):

    nuevo_gasto = {
        "Fecha": [fecha],
        "Tipo": [tipo_gasto],
        "Concepto": [concepto],
        "Monto": [monto],
        "Metodo_Pago": [metodo_pago],
        "Comentarios": [comentarios]
    }

    df_nuevo = pd.DataFrame(nuevo_gasto)

    # SI EL ARCHIVO YA EXISTE
    if os.path.exists(ARCHIVO_EXCEL):
      
        df_existente = pd.read_excel(ARCHIVO_EXCEL)

        df_final = pd.concat(
            [df_existente, df_nuevo],
            ignore_index=True
        )

        df_final.to_excel(
            ARCHIVO_EXCEL,
            index=False
        )

    else:
        df_nuevo.to_excel(
            ARCHIVO_EXCEL,
            index=False
        )

    st.success("Gasto guardado correctamente")

# MOSTRAR HISTORIAL
st.subheader("Historial de gastos")

if os.path.exists(ARCHIVO_EXCEL):

    df = pd.read_excel(ARCHIVO_EXCEL)

    st.dataframe(df.tail(20))

    # TOTAL GASTADO
    total = df["Monto"].sum()

    st.metric("Total gastado", f"${total:,.2f}")

    # DESCARGA
    with open(ARCHIVO_EXCEL, "rb") as file:
        st.download_button(
            label="Descargar Excel",
            data=file,
            file_name="gastos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )