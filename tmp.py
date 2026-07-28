comp = base[(base["Custo_M1"].notna()) & (base["_gap"] == 1)].copy()

comp["Erro_Un_Abs_M1"]    = (comp["Custo_M1"] - comp[COL_REAL]).abs()
comp["APE_M1"]            = comp["Erro_Un_Abs_M1"] / comp[COL_REAL]
comp["Erro_Valor_Abs_M1"] = comp["Erro_Un_Abs_M1"] * comp[COL_PROD]
comp["Valor_M1_R$"]       = comp["Custo_M1"] * comp[COL_PROD]
comp["Acertou_M1"]        = comp["APE_M1"] <= comp["Classe_ABC"].map(TOLERANCIAS)

acur_s = 1 - comp["Erro_Valor_Abs_R$"].sum() / comp["Valor_Real_R$"].sum()
acur_b = 1 - comp["Erro_Valor_Abs_M1"].sum() / comp["Valor_Real_R$"].sum()

print(f"Linhas comparáveis: {len(comp):,} de {len(base):,} ({len(comp)/len(base):.0%})")
print(f"Cobrem {comp['Valor_Real_R$'].sum() / base['Valor_Real_R$'].sum():.0%} do valor movimentado\n")

tabela = pd.DataFrame({
    "Indicador": ["Acurácia", "Hit Rate", "MAE (R$/un)", "Erro total"],
    "Baseline (mês anterior)": [f"{acur_b:.1%}", f"{comp['Acertou_M1'].mean():.1%}",
                                f"R$ {comp['Erro_Un_Abs_M1'].mean():,.2f}",
                                f"R$ {comp['Erro_Valor_Abs_M1'].sum():,.0f}"],
    "Script": [f"{acur_s:.1%}", f"{comp['Acertou'].mean():.1%}",
               f"R$ {comp['Erro_Un_Abs_R$'].mean():,.2f}",
               f"R$ {comp['Erro_Valor_Abs_R$'].sum():,.0f}"],
    "Diferença": [f"{(acur_s - acur_b)*100:+.2f} p.p.",
                  f"{(comp['Acertou'].mean() - comp['Acertou_M1'].mean())*100:+.1f} p.p.",
                  f"R$ {comp['Erro_Un_Abs_R$'].mean() - comp['Erro_Un_Abs_M1'].mean():+,.2f}",
                  f"R$ {comp['Erro_Valor_Abs_R$'].sum() - comp['Erro_Valor_Abs_M1'].sum():+,.0f}"],
})
display(tabela.style.hide(axis="index"))

venceu = comp["Erro_Valor_Abs_R$"] < comp["Erro_Valor_Abs_M1"]
print(f"\nScript melhor em {venceu.sum()} linhas ({venceu.mean():.1%}) | "
      f"Baseline melhor em {(~venceu).sum()} ({1-venceu.mean():.1%})")
