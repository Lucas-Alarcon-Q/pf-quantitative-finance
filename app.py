import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

#===============
#APP
#===============

#Título de la app
st.title("Calculadora Riesgo Mercado")

#Seleccionar tickers
st.multiselect(label = "tickers", options = ["IVV", "ILF", "SOXX"] , key = "tickers", default = "SOXX")
tickers = st.session_state["tickers"]

#Seleccionar pesos
st.multiselect(label = "pesos", options = [0.5, 0.3, 0.2], key = "pesos")
vector_w = st.session_state["pesos"]
vector_w = np.array(vector_w).reshape(-1,1) 

#Descargar precios desde yahoo finance
if len(tickers) > 0:
    df_prices = yf.download(tickers, start="2024-01-01", end="2026-09-30")["Close"]
    df_prices = df_prices[tickers]
   #st.dataframe(df_prices)

# Calcular los retornos diarios
df_ret = df_prices.pct_change().dropna()

#Calcular la matriz de varaianza-covarianza
df_cov = df_ret.cov()

# Calcular la varianza del portafolio
w = vector_w
w_t = w.T
sigma = df_cov.values
varianza = np.dot(sigma, w)
varianza = np.dot(w_t, varianza)[0][0]
desv = varianza**(1/2)
volatilidad_anual = desv * (252**(1/2)) #Anualizar la volatilidad
st.write(f"La volatilidad anual del portafolio es: {volatilidad_anual*100:.4}%")

