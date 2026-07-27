caros = base[(base[COL_REAL] > 100) & (base[COL_REAL] <= 1000)]

print(f"{len(caros)} linhas | {caros[[COL_CENTRO, COL_MATERIAL]].drop_duplicates().shape[0]} materiais")
print(f"Representam {caros['Valor_Real_R$'].sum() / base['Valor_Real_R$'].sum():.1%} do valor total")
display(caros["Classe_ABC"].value_counts().to_frame("Linhas"))

display(
    caros.groupby([COL_CENTRO, COL_MATERIAL, "Classe_ABC"])
         .agg(Meses=(COL_MES, "nunique"), Acertos=("Acertou", "sum"),
              Preco_medio=(COL_REAL, "mean"), APE_medio=("APE", "mean"),
              Pior_APE=("APE", "max"), Erro_R$=("Erro_Valor_Abs_R$", "sum"))
         .sort_values("Erro_R$", ascending=False)
         .style.format({"Preco_medio": "R$ {:,.2f}", "APE_medio": "{:.1%}",
                        "Pior_APE": "{:.1%}", "Erro_R$": "R$ {:,.0f}"})
)
