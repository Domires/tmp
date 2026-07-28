import unicodedata

MESES_NUM = {"janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4,
             "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
             "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}
ANO = 2026

def _chave(s):
    s = unicodedata.normalize("NFKD", str(s).strip().lower())
    return s.encode("ascii", "ignore").decode("ascii")

base["_mes_num"] = base[COL_MES].map(lambda x: MESES_NUM.get(_chave(x)))
base["_dt"] = pd.to_datetime(
    dict(year=ANO, month=base["_mes_num"], day=1), errors="coerce")

print(f"Não convertidos: {base['_dt'].isna().sum()}")
display(base.loc[base["_dt"].isna(), COL_MES].value_counts())
