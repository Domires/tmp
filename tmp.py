def diagnostico_classe(df, classe, top_n=10):
    sub = df[df["Classe_ABC"] == classe]

    g = (sub.groupby([COL_CENTRO, COL_MATERIAL])
            .agg(Meses=(COL_MES, "nunique"),
                 Acertos=("Acertou", "sum"),
                 Valor_Real=("Valor_Real_R$", "sum"),
                 Valor_Prev=("Valor_Prev_R$", "sum"),
                 Erro_Impacto=("Erro_Valor_Abs_R$", "sum"))
            .reset_index()
            .sort_values("Erro_Impacto", ascending=False))

    # métricas consistentes com o painel: ponderadas por valor
    g["Acuracia"]      = 1 - g["Erro_Impacto"] / g["Valor_Real"]
    g["Vies"]          = (g["Valor_Prev"] - g["Valor_Real"]) / g["Valor_Real"]
    g["%_Erro_Classe"] = g["Erro_Impacto"] / g["Erro_Impacto"].sum()
    g["%_Erro_Acum"]   = g["%_Erro_Classe"].cumsum()
    g["Acertou_em"]    = g["Acertos"].astype(int).astype(str) + "/" + g["Meses"].astype(str)

    # concentração: quantos materiais explicam metade do erro da classe
    n_metade = int((g["%_Erro_Acum"] <= 0.50).sum()) + 1
    print(f"Classe {classe}: {len(g)} materiais | "
          f"erro total R$ {g['Erro_Impacto'].sum():,.2f}")
    print(f"{n_metade} material(is) concentram 50% do erro da classe "
          f"({n_metade/len(g):.0%} dos materiais)")

    cols = ["Centro", "Material", "Valor_Real", "Erro_Impacto",
            "%_Erro_Classe", "%_Erro_Acum", "Acuracia", "Vies", "Acertou_em"]
    return (g.head(top_n)
             .rename(columns={COL_CENTRO: "Centro", COL_MATERIAL: "Material"})[cols]
             .style.hide(axis="index")
             .format({"Valor_Real": "R$ {:,.0f}", "Erro_Impacto": "R$ {:,.0f}",
                      "%_Erro_Classe": "{:.1%}", "%_Erro_Acum": "{:.1%}",
                      "Acuracia": "{:.1%}", "Vies": "{:+.1%}"}))


display(diagnostico_classe(base, "B"))
