

## Gerar gráfico cruzando os dados da Média da Qualidade da Água segundo a ANA com os Estados Brasileiros
## Parâmetroas analisados para ter a média: Oxigênio Dissolvido, Fósforo Total, Demanda Bioquímica de Oxigênio, Turbidez e E. coli

#Importar bibliotecas
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# 1. Definir caminhos de leitura dos arquivos que estão na pasta raw
OUTDIR = Path(r"C:\Users\gasiq\Downloads\A11 - Pratique\Mod_18\data\raw")
caminho_agua = OUTDIR / "dados_qualidade_agua.csv"
caminho_ibge = OUTDIR / "ibge_estados.csv"

# 2. Carregar os CSVs para o Pandas
df_agua = pd.read_csv(caminho_agua)
df_ibge = pd.read_csv(caminho_ibge)

# Garantir que a coluna "ANO" seja tratada como número inteiro
df_agua["ANO"] = pd.to_numeric(df_agua["ANO"], errors="coerce")

# 3. Cruzar os dados usando as colunas correspondentes (SGUF -> UF-sigla)
df_cruzado = pd.merge(
    df_agua, df_ibge, left_on="SGUF", right_on="UF-sigla", how="inner"
)

# 4. Criar uma tabela com a média do IQA por Estado no ano de 2021
df_2021 = df_cruzado[df_cruzado["ANO"] == 2021]

# Agrupar pelo nome completo do estado do arquivo ('UF-nome') e calcular a média
media_por_estado = (
    df_2021.groupby("UF-nome")["MEDIQA"].mean().sort_values(ascending=False)
)

# Descobrir quais estados ficaram fora dos dados disponibilizados pela ANA
todos_estados_ibge = set(df_ibge["UF-nome"].dropna().unique())
estados_no_grafico = set(media_por_estado.index)
estados_ausentes = sorted(list(todos_estados_ibge - estados_no_grafico))

# Transformar a lista de estados ausentes em texto separado por vírgulas
texto_ausentes = ", ".join(estados_ausentes)

# 5. Configurar e gerar o gráfico de barras
plt.figure(figsize=(12, 7.5))  
media_por_estado.plot(kind="bar", color="skyblue", edgecolor="black")

# 6. Adicionar linhas horizontais de referência (Réguas de classificação do IQA)
plt.axhline(y=79, color="green", linestyle="--", label="Faixa Ótima (79-100)")
plt.axhline(y=51, color="orange", linestyle="--", label="Faixa Boa (51-79)")
plt.axhline(y=36, color="red", linestyle="--", label="Faixa Ruim/Péssima (<36)")

# 7. Customizações visuais do gráfico
plt.title(
    "Média do Índice de Qualidade da Água (IQA) por Estado - Ano 2021",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Estado (Dados: IBGE)", fontsize=12)
plt.ylabel("Média do IQA (Dados: ANA)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.ylim(0, 105)
plt.legend(loc="lower left")

# Informações no Rodapé
mensagem_rodape = (
    f"Metodologia: Dados calculados a partir das estatísticas anuais da base de dados da ANA (camada 16).\n"
    f"Fontes: ANA (Agência Nacional de Águas) e IBGE. | Autor: GABRIEL SIQUEIRA DOS SANTOS\n"
    f"Nota: Os seguintes estados não estão representados por não apresentarem dados de medição computados para o ano de 2021:\n"
    f"{texto_ausentes}."
)

plt.figtext(
    0.02, 0.01, 
    mensagem_rodape,
    fontsize=8, style="italic", color="dimgray", wrap=True
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.32)

# 8. Salvar o gráfico na pasta processed
PASTA_GRAFICOS = Path(
    r"C:\Users\gasiq\Downloads\A11 - Pratique\Mod_18\data\processed"
)
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)
caminho_salvamento_imagem = PASTA_GRAFICOS / "grafico_qualidade_agua_2021.png"

plt.savefig(caminho_salvamento_imagem, dpi=300)
plt.show()

print(f"Gráfico gerado e salvo com sucesso em: {caminho_salvamento_imagem}")


# FIM DO SCRIPT
