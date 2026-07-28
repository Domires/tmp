por_mat = (comp.groupby([COL_CENTRO, COL_MATERIAL, "Classe_ABC"])
              .apply(lambda x: pd.Series({
                  "Ganho_R$": x["Erro_Valor_Abs_M1"].sum() - x["Erro_Valor_Abs_R$"].sum()
              }), include_groups=False)
              .reset_index().sort_values("Ganho_R$", ascending=False))
por_mat["%_acum"] = por_mat["Ganho_R$"].cumsum() / por_mat["Ganho_R$"].sum()
display(por_mat.head(10))
