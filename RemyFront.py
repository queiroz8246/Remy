import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from IA.Remy import Remy
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}

        [data-testid="stHeader"]{{
            background-color: rgba(0,0,0,0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


add_bg_from_local("vinho4.jpeg")


st.markdown("<h1 style='color: white;'>Conheça Remy</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: white;'>A inteligencia Artificial somelier de vinhos</h2>", unsafe_allow_html = True)


with st.form(key='meu_form', clear_on_submit=True):

    col1, col2, col3 = st.columns(3)
    with col1:
        acidez =  st.number_input("Insira a acidez fixa:")
        acidezV = st.number_input("Insira a acidez volatil:")
        accitrico = st.number_input("Insira o acido citrico:")
        acucar = st.number_input("Insira o açucar residual:")
        cloretos = st.number_input("Insira os cloretos:")
        dioxidoL = st.number_input("Insira a quantidade de dioxido de enxofre livre:")

    with col2:    
        dioxidoT = st.number_input("Insira a quantidade de dioxido de enxofre total:")
        densidade = st.number_input("Insira a densidade:")
        ph = st.number_input("Insira o ph:")
        sulfatos = st.number_input("Insira o sulfato:")
        alcool = st.number_input("Insira o alcool:")

        enviar = False
        enviar = st.form_submit_button("Enviar Dados")

        vetor = [acidez, 
                 acidezV, 
                 accitrico,
                 acucar, 
                 cloretos, 
                 dioxidoL, 
                 dioxidoT, 
                 densidade, 
                 ph, 
                 sulfatos, 
                 alcool ]
        
    with col3:
        # if enviar:
        #     if acidez and dioxidoT:
        #         st.write("Dados recebidos: ")
        #         st.write(f"**Acidez Fixa: {acidez} **")
        #         st.write(f"**Acidez Volatil: {acidezV} **")
        #         st.write(f"**Acido Citrico: {accitrico} **")
        #         st.write(f"**Açucar: {acucar} **")
        #         st.write(f"**Cloretos: {cloretos} **")
        #         st.write(f"**Dioxido de Enxofre Livre: {dioxidoL} **")
        #         st.write(f"**Dioxido de Enxofre Total: {dioxidoT} **")
        #         st.write(f"**Densidade: {densidade} **")
        #         st.write(f"**PH: {ph} **")
        #         st.write(f"**sulfatos: {sulfatos} **")
        #         st.write(f"**Alcool: {alcool} **")

        # else:
        #     st.error("Porfavor insira algum valor!")
        if enviar:
            remy = Remy()
            retorno = remy.Analizar(vetor)
            st.markdown(f"""
            <div style='background-color: black; color: lightgreen; border: 3px white solid; border-radius: 20px; padding: 10px;'>
             {retorno[0]}<br>
            {retorno[1]}<br>
            {retorno[2]}<br>
            {retorno[3]}<br> 
            </div>
            """, unsafe_allow_html=True)
            remy.Say()

        # st.write(enviar)
