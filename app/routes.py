import os
import pandas as pd
import json
from flask import Blueprint, jsonify, Response

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')  # Caminho para a pasta 'uploads'

#def normalize_dataframe(df):
#    return df.applymap(
#        lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x
#    )
#]

def substituir_ao(df):
    return df.map(
        lambda x: x.replace("ão", "ao") if isinstance(x, str) else x
    )


@main.route("/")
def carregar_csv():
    arquivos_csv = []
    
    for arquivo in os.listdir(UPLOAD_FOLDER):
        if arquivo.endswith(".csv"):
            arquivo_path = os.path.join(UPLOAD_FOLDER, arquivo)
            print(f"Lendo o arquivo: {arquivo_path}")
            
            # Lê o CSV com o encoding especificado
            try:
                df = pd.read_csv(arquivo_path, encoding='utf-8', on_bad_lines='skip')  # Ignora linhas mal formadas
                #df = normalize_dataframe(df)
                df = substituir_ao(df)
                arquivos_csv.append({
                    "nome_arquivo": arquivo,
                    "dados": df.head().to_dict(orient="records")  # Exibe as primeiras linhas como exemplo
                })
            except Exception as e:
                print(f"Erro ao ler o arquivo {arquivo}: {str(e)}")
    
    if not arquivos_csv:
        return jsonify({"message": "Nenhum arquivo CSV encontrado!"}), 404
    
    return Response(json.dumps(arquivos_csv, ensure_ascii=False), content_type='application/json; charset=utf-8')
    
    #return jsonify(arquivos_csv), 200
