import pandas as pd
import numpy as np
import yfinance as yf

# Descargar precios desde yahoo finance
tickers = ["IVV", "ILF", "SOXX"] # SP500, LATAMA y SEMICONDUCTORES
vector_w = [0.5, 0.3, 0.2] # Lista de pesos para cada activo
vector_w = np.array(vector_w).reshape(-1,1) 
df_prices = yf.download(tickers, start="2024-01-01", end="2026-09-30")["Close"]
df_prices = df_prices[tickers]

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
volatilidad_anual = desv * (252**(1/2))
print(f"La volatilidad anual del portafolio es: {volatilidad_anual*100:.4}%")

# Calcular la media del portafolio
vector_ret = df_ret.mean()
vector_ret = vector_ret.values
vector_ret = vector_ret.reshape(-1,1) 

mu = np.dot(w_t, vector_ret)[0][0]
mu_anual = mu * 252

# Calcular Value at Risk (VaR) al 95% de confianza
var_95 = mu_anual - 1.64 * volatilidad_anual
print(f"La VaR anual del portafolio es: {var_95*100:.4}%")

# FIRMA: 11Q3IA3ErBpduGEp4LrVAeU9Gz3_gAYYAw0sAK4kNb3R4_wAs2jyGHH1booCBCDrVd58_XiFIVuRc_RpEyiNKzNKfMmmZHHv9BeAnhw-Ng==
