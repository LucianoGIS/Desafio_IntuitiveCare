from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "./data/despesas_agregadas.csv"

def carregar_dados():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()

@app.get("/api/operadoras")
def listar_operadoras(page: int = 1, limit: int = 10, search: str = ""):
    df = carregar_dados()
    
    if df.empty:
        return {"data": [], "total": 0}

    if search:
        df = df[df['Razao_Social'].str.contains(search, case=False, na=False)]
    
    total = len(df)
    inicio = (page - 1) * limit
    fim = inicio + limit
    
    dados = df.iloc[inicio:fim].to_dict(orient="records")
    
    return {
        "data": dados,
        "page": page,
        "limit": limit,
        "total": total
    }

@app.get("/api/estatisticas")
def estatisticas():
    df = carregar_dados()
    if df.empty:
        return []
    
    stats = df.groupby('UF')['Total_Despesas'].sum().reset_index()
    return stats.to_dict(orient="records")