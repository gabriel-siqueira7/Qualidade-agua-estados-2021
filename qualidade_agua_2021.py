
### IDEIA: BAIXAR OS DADOS DE QUALIDADE DA ÁGUA DO SITE DA ANA (2021)
### E CRUZA-LOS COM OS DADOS DOS ESTADOS DO SITE DO IBGE 


#Importar as bibliotecas
from pathlib import Path
import pandas as pd
import requests

# 1. Salvar dados brutos na pasta "raw"
OUTDIR = Path(r"C:\Users\gasiq\Downloads\A11 - Pratique\Mod_18\data\raw")
OUTDIR.mkdir(parents=True, exist_ok=True)

# Definição de caminho
caminho_final = OUTDIR / "dados_qualidade_agua.csv"

# 2. Link e parametrização para paginação (1646 dados)
url_base = "https://www.snirh.gov.br/arcgis/rest/services/SPR/Indicadores_Qualidade_v31072023/FeatureServer/16/query?where=1%3D1&outFields=MEDIQA,MINIQA,MAXIQA,DEVIQA,ANO,SGUF,NUIQA,ID&outSR=4326&f=json"

params = {
    "where": "1=1",
    "outFields": "MEDIQA,MINIQA,MAXIQA,DEVIQA,ANO,SGUF,NUIQA,ID",
    "outSR": "4326",
    "f": "json",
    "resultRecordCount": 1000,  # Blocos de 1000
    "resultOffset": 0           # Começa do zero
}

todos_atributos = []
continuar_baixando = True

print("Iniciando o download dos dados da ANA...")

# 3. Loop de requisições
while continuar_baixando:
    resposta = requests.get(url_base, params=params)
    dados_json = resposta.json()
    
    features = dados_json.get("features", [])
    
    if not features:
        break
        
    for feature in features:
        todos_atributos.append(feature["attributes"])
        
    print(f"Baixados {len(todos_atributos)} registros até agora...")
    
    if len(features) < 1000:
        continuar_baixando = False
    else:
        params["resultOffset"] += 1000

# 5. Criar o DataFrame
df_api = pd.DataFrame(todos_atributos)
print(f"Download concluído! Total de linhas salvas na memória: {len(df_api)}")

# 6. Salvar o CSV estrutur
df_api.to_csv(caminho_final, index=False, encoding="utf-8-sig")

print("Arquivo 'dados_qualidade_agua.csv' gerado com sucesso na pasta raw!")


#### FIM DO SCRIPT
