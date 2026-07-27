MESES_PT = {1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
            7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"}

def diagnostico_classe(df, classe, top_n=10):
    sub = df[df["Classe_ABC"] == classe].copy()

    # ---- Rótulo curto e cronológico para o mês ----
    mes_dt = pd.to_datetime(sub[COL_MES], errors="coerce")
    if mes_dt.notna().all():
        sub["_mes_lbl"] = mes_dt.dt.month.map(MESES_PT)
        sub = sub.assign(_ordem=mes_dt).sort_values("_ordem")
    else:
        sub["_mes_lbl"] = sub[COL_MES].astype(str)
        sub = sub.sort_values(COL_MES)

    # só o mês em que ERROU; acertos viram string vazia
    sub["_mes_erro"] = np.where(~sub["Acertou"], sub["_mes_lbl"], "")

    g = (sub.groupby([COL_CENTRO, COL_MATERIAL])
            .agg(Meses=(COL_MES, "nunique"),
                 Acertos=("Acertou", "sum"),
                 Valor_Real=("Valor_Real_R$", "sum"),
                 Valor_Prev=("Valor_Prev_R$", "sum"),
                 Erro_Impacto=("Erro_Valor_Abs_R$", "sum"),
                 Meses_Erro=("_mes_erro", lambda s: ", ".join(m for m in s if m)),
                 Pior_APE=("APE", "max"))
            .reset_index()
            .sort_values("Erro_Impacto", ascending=False))

    g["Acuracia"]      = 1 - g["Erro_Impacto"] / g["Valor_Real"]
    g["Vies"]          = (g["Valor_Prev"] - g["Valor_Real"]) / g["Valor_Real"]
    g["%_Erro_Classe"] = g["Erro_Impacto"] / g["Erro_Impacto"].sum()
    g["%_Erro_Acum"]   = g["%_Erro_Classe"].cumsum()
    g["Acertou_em"]    = g["Acertos"].astype(int).astype(str) + "/" + g["Meses"].astype(str)

    n_metade = int((g["%_Erro_Acum"] <= 0.50).sum()) + 1
    print(f"Classe {classe}: {len(g)} materiais | "
          f"erro total R$ {g['Erro_Impacto'].sum():,.2f}")
    print(f"{n_metade} material(is) concentram 50% do erro da classe "
          f"({n_metade/len(g):.0%} dos materiais)")

    cols = ["Centro", "Material", "Valor_Real", "Erro_Impacto", "%_Erro_Acum",
            "Acuracia", "Vies", "Acertou_em", "Meses_Erro", "Pior_APE"]
    return (g.head(top_n)
             .rename(columns={COL_CENTRO: "Centro", COL_MATERIAL: "Material"})[cols]
             .style.hide(axis="index")
             .format({"Valor_Real": "R$ {:,.0f}", "Erro_Impacto": "R$ {:,.0f}",
                      "%_Erro_Acum": "{:.1%}", "Acuracia": "{:.1%}",
                      "Vies": "{:+.1%}", "Pior_APE": "{:.1%}"}))


display(diagnostico_classe(base, "B"))
