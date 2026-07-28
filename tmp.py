det = base.copy()
det["Tolerancia_%"]  = det["Classe_ABC"].map(TOLERANCIAS)
det["Tolerancia_R$"] = det[COL_REAL] * det["Tolerancia_%"]
det["Folga_R$"]      = det["Tolerancia_R$"] - det["Erro_Un_Abs_R$"]
det["Resultado"]     = np.where(det["Acertou"], "Acerto", "Erro")

cols = [COL_CENTRO, COL_MATERIAL, "_mes_lbl", "Classe_ABC", COL_REAL, COL_PREV,
        "Erro_Un_Abs_R$", "APE", "Tolerancia_%", "Tolerancia_R$", "Folga_R$",
        COL_PROD, "Erro_Valor_Abs_R$", "Resultado"]

fmt = {COL_REAL: "R$ {:,.2f}", COL_PREV: "R$ {:,.2f}",
       "Erro_Un_Abs_R$": "R$ {:,.2f}", "APE": "{:.1%}",
       "Tolerancia_%": "{:.0%}", "Tolerancia_R$": "R$ {:,.2f}",
       "Folga_R$": "R$ {:,.2f}", COL_PROD: "{:,.0f}",
       "Erro_Valor_Abs_R$": "R$ {:,.0f}"}

def realce(row):
    cor = "background-color: #ffe5e5" if row["Resultado"] == "Erro" else ""
    return [cor] * len(row)

print(f"{(~base['Acertou']).sum()} erros | {base['Acertou'].sum()} acertos\n")
print("--- 20 piores casos (maior estouro da tolerância) ---")
display(det[~det["Acertou"]].nsmallest(20, "Folga_R$")[cols]
        .style.hide(axis="index").format(fmt).apply(realce, axis=1))

print("--- 10 que passaram raspando ---")
display(det[det["Acertou"]].nsmallest(10, "Folga_R$")[cols]
        .style.hide(axis="index").format(fmt))
