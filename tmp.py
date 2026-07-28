comp["Script_venceu"] = comp["Erro_Valor_Abs_R$"] < comp["Erro_Valor_Abs_M1"]

display(
    comp.groupby("Classe_ABC")
        .apply(lambda x: pd.Series({
            "Linhas": len(x),
            "Script_venceu_%": x["Script_venceu"].mean(),
            "Acur_Baseline": 1 - x["Erro_Valor_Abs_M1"].sum() / x["Valor_Real_R$"].sum(),
            "Acur_Script":   1 - x["Erro_Valor_Abs_R$"].sum() / x["Valor_Real_R$"].sum(),
            "R$_evitado":    x["Erro_Valor_Abs_M1"].sum() - x["Erro_Valor_Abs_R$"].sum(),
        }), include_groups=False)
        .reset_index()
        .style.hide(axis="index")
        .format({"Linhas": "{:,.0f}", "Script_venceu_%": "{:.1%}",
                 "Acur_Baseline": "{:.1%}", "Acur_Script": "{:.1%}",
                 "R$_evitado": "R$ {:,.0f}"})
)
