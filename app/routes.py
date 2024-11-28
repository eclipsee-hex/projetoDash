import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import Blueprint, redirect, url_for



main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# Rota inicial redirecionando para /analise
@main.route("/")
def home():
    return redirect(url_for('main.analise'))

# Rota para gerar e exibir o gráfico de análise
@main.route("/analise")
def analise():
    arquivo_csv = os.path.join(UPLOAD_FOLDER, 'gastosNovembroPorCategoria.csv')
    
    

    try:
        # Lê o CSV
        def converter_valor(valor):
            try:
                return float(valor.replace('R$', '').replace(',', '.').strip())
                
            except:
                return 0.0
        
        
        df = pd.read_csv(arquivo_csv, encoding='utf-8')
        df_numeric = df.applymap(converter_valor)


        # Soma os valores por categoria
        totais_por_categoria = df_numeric.sum()
        print("valores somados")
        
        # Gera o gráfico
        plt.figure(figsize=(8, 6))
        totais_por_categoria.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title("Gastos Totais por Categoria - Novembro", fontsize=14)
        plt.xlabel("Categorias", fontsize=10)
        plt.ylabel("Gastos Totais (R$)", fontsize=11)
        plt.xticks(rotation=45, fontsize=8)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Salva o gráfico como imagem base64
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Retorna a imagem como resposta HTML
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f'<img src="data:image/png;base64,{img_base64}"/>'
    
    except Exception as e:
        return f"Erro ao gerar o gráfico: {str(e)}", 500
    
    
