# 1. Duplicatas por chave — principal suspeito
dup = df_merged.duplicated(subset=[COL_CENTRO, COL_MATERIAL, COL_MES]).sum()
print(f"df_merged: {len(df_merged):,} linhas | duplicatas por chave: {dup:,}")
print(f"base: {len(base):,} linhas\n")

# 2. Colunas disponíveis (confirmar sufixos)
print([c for c in df_merged.columns if "usto" in c or "rodu" in c], "\n")

# 3. Escala das colunas críticas
display(base[[COL_PREV, COL_REAL, COL_PROD]].describe())

# 4. As 10 linhas que explodem o erro
top = base.assign(EV=base["Erro_Un_Abs_R$"] * base[COL_PROD]).nlargest(10, "EV")
display(top[[COL_CENTRO, COL_MATERIAL, COL_MES, COL_PREV, COL_REAL, COL_PROD, "EV"]])
