base = base.sort_values([COL_CENTRO, COL_MATERIAL, "_dt"]).reset_index(drop=True)
g = base.groupby([COL_CENTRO, COL_MATERIAL])

base["Custo_M1"] = g[COL_REAL].shift(1)
_ant = g["_dt"].shift(1)
base["_gap"] = ((base["_dt"].dt.year * 12 + base["_dt"].dt.month) -
                (_ant.dt.year * 12 + _ant.dt.month))

print(f"Preenchidos: {base['Custo_M1'].notna().sum():,} de {len(base):,}")
display(base["_gap"].value_counts(dropna=False).to_frame("Linhas").rename_axis("Gap"))
