"""Imputación KNN de variables numéricas para NTL Dataset Factory.

Uso:
  python dataset_factory/imputation/knn_imputer.py --input datos.csv --output datos_knn.csv --columns CONSUMO_ACTUAL CARTERA_TOTAL

No subir datos de clientes a repositorios públicos.
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

def imputar_knn(df: pd.DataFrame, columnas: list[str], vecinos: int = 5) -> pd.DataFrame:
    """Imputa columnas numéricas conservando los valores observados y flags de ausencia.

    Demostración de imputación para un único conjunto. Para evaluación ML temporal,
    ajustar scaler/imputer SOLO en train y transformar validation/test sin reajustar.
    """
    if vecinos < 1:
        raise ValueError("vecinos debe ser >= 1")
    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        raise ValueError(f"Columnas no encontradas: {faltantes}")
    if not columnas:
        raise ValueError("Indique al menos una columna.")
    resultado = df.copy()
    x = df[columnas].apply(pd.to_numeric, errors="coerce")
    for col in columnas:
        resultado[f"{col}_FALTANTE"] = x[col].isna().astype("int8")
    validas = [c for c in columnas if x[c].notna().any()]
    if not validas:
        raise ValueError("Todas las columnas seleccionadas están completamente vacías.")
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x[validas])
    knn = KNNImputer(n_neighbors=vecinos, weights="distance", metric="nan_euclidean")
    imputed = pd.DataFrame(
        scaler.inverse_transform(knn.fit_transform(x_scaled)),
        columns=validas, index=df.index
    )
    for col in validas:
        resultado[col] = x[col].where(x[col].notna(), imputed[col])
    return resultado

def main():
    parser = argparse.ArgumentParser(description="Imputación KNN de columnas numéricas")
    parser.add_argument("--input", required=True, help="CSV de entrada")
    parser.add_argument("--output", required=True, help="CSV de salida")
    parser.add_argument("--columns", nargs="+", required=True, help="Columnas a imputar")
    parser.add_argument("--neighbors", type=int, default=5)
    args = parser.parse_args()
    data = pd.read_csv(args.input)
    output = imputar_knn(data, args.columns, args.neighbors)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(target, index=False, encoding="utf-8-sig")
    print(f"Archivo generado: {target} ({len(output)} filas)")

if __name__ == "__main__":
    main()
