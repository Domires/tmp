print(f"BI: {len(df_bi):,} | Forecast: {len(df_fc):,} | Merge: {len(df_merged):,}")
print(f"Centros no BI:       {sorted(df_bi[COL_CENTRO].unique())}")
print(f"Centros no Forecast: {sorted(df_fc[COL_CENTRO].unique())}")
