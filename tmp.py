comp = base[base[COL_M1].notna()].copy()

def metricas(df, erro_valor, erro_un, valor_prev, acertou):
    return {
        "Acuracia":   1 - df[erro_valor].sum() / df["Valor_Real_R$"].sum(),
        "MAE_un":     df[erro_un].mean(),
        "Vies":       (df[valor_prev].sum() - df["Valor_Real_R$"].sum()) / df["Valor_Real_R$"].sum(),
        "Hit_Rate":   df[acertou].mean(),
        "Erro_Total": df[erro_valor].sum(),
    }

s = metricas(comp, "Erro_Valor_Abs_R$", "Erro_Un_Abs_R$", "Valor_Prev_R$", "Acertou")
b = metricas(comp, "Erro_Valor_Abs_M1", "Erro_Un_Abs_M1", "Valor_M1_R$",  "Acertou_M1")

print(f"Base comparável: {len(comp):,} de {len(base):,} linhas ({len(comp)/len(base):.0%})")
print(f"Cobre {comp['Valor_Real_R$'].sum() / base['Valor_Real_R$'].sum():.0%} do valor movimentado\n")

tabela = pd.DataFrame({
    "Indicador": ["Acurácia", "MAE (R$/un)", "Viés", "Hit Rate", "Erro total (R$)"],
    "Baseline (mês anterior)": [f"{b['Acuracia']:.1%}", f"R$ {b['MAE_un']:,.2f}",
                                f"{b['Vies']:+.1%}", f"{b['Hit_Rate']:.1%}",
                                f"R$ {b['Erro_Total']:,.0f}"],
    "Script de forecast":      [f"{s['Acuracia']:.1%}", f"R$ {s['MAE_un']:,.2f}",
                                f"{s['Vies']:+.1%}", f"{s['Hit_Rate']:.1%}",
                                f"R$ {s['Erro_Total']:,.0f}"],
    "Diferença": [
        f"{(s['Acuracia'] - b['Acuracia'])*100:+.2f} p.p.",
        f"R$ {s['MAE_un'] - b['MAE_un']:+,.2f}",
        "—",
        f"{(s['Hit_Rate'] - b['Hit_Rate'])*100:+.1f} p.p.",
        f"R$ {s['Erro_Total'] - b['Erro_Total']:+,.0f}",
    ],
})
display(tabela.style.hide(axis="index"))

# ---- Placar linha a linha ----
venceu = comp["Erro_Valor_Abs_R$"] < comp["Erro_Valor_Abs_M1"]
perdeu = comp["Erro_Valor_Abs_R$"] > comp["Erro_Valor_Abs_M1"]
print(f"\nScript melhor: {venceu.sum():,} ({venceu.mean():.1%}) | "
      f"Baseline melhor: {perdeu.sum():,} ({perdeu.mean():.1%}) | "
      f"Empate: {(~venceu & ~perdeu).sum():,}")

# ---- Por classe ----
por_classe_comp = (
    comp.groupby("Classe_ABC")
        .apply(lambda x: pd.Series({
            "Acur_Baseline": 1 - x["Erro_Valor_Abs_M1"].sum() / x["Valor_Real_R$"].sum(),
            "Acur_Script":   1 - x["Erro_Valor_Abs_R$"].sum() / x["Valor_Real_R$"].sum(),
            "Script_venceu": (x["Erro_Valor_Abs_R$"] < x["Erro_Valor_Abs_M1"]).mean(),
        }), include_groups=False)
        .reset_index()
)
por_classe_comp["Ganho_pp"] = (por_classe_comp["Acur_Script"] - por_classe_comp["Acur_Baseline"]) * 100

display(por_classe_comp.style.hide(axis="index")
        .format({"Acur_Baseline": "{:.1%}", "Acur_Script": "{:.1%}",
                 "Script_venceu": "{:.1%}", "Ganho_pp": "{:+.2f}"}))
###

chk = base.copy()
chk["_dt"] = pd.to_datetime(chk[COL_MES], errors="coerce")
chk = chk.sort_values([COL_CENTRO, COL_MATERIAL, "_dt"])
chk["_dt_ant"] = chk.groupby([COL_CENTRO, COL_MATERIAL])["_dt"].shift(1)
chk["_gap"] = ((chk["_dt"].dt.year*12 + chk["_dt"].dt.month) -
               (chk["_dt_ant"].dt.year*12 + chk["_dt_ant"].dt.month))

print(f"Linhas com Custo_M1 preenchido: {base[COL_M1].notna().sum():,}")
display(chk.loc[base[COL_M1].notna(), "_gap"].value_counts(dropna=False)
           .to_frame("Linhas").rename_axis("Gap em meses"))
