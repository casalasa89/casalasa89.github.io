# NTL Dataset Factory — Imputación KNN

Código demostrativo de imputación de variables numéricas con `KNNImputer` de scikit-learn.

## Instalación

```bash
pip install -r dataset_factory/requirements.txt
```

## Ejecución

```bash
python dataset_factory/imputation/knn_imputer.py \
  --input datos_usuarios.csv \
  --output datos_usuarios_knn.csv \
  --columns CONSUMO_ACTUAL CARTERA_TOTAL DIAS_MORA \
  --neighbors 5
```

Adapte los nombres de columnas al archivo real. Se conservan flags `<COLUMNA>_FALTANTE`. No se imputan columnas completamente vacías. El algoritmo no distingue automáticamente un cero legítimo de un faltante: esa decisión requiere reglas de calidad previas.

**Advertencia metodológica:** este script ajusta escalador e imputador sobre el archivo completo y sirve para exploración. Para experimentos supervisados, separar temporalmente train/validation/test **antes** de ajustar cualquier transformación; no usar este script sobre todo el dataset previo a esa separación. KNN puede ser costoso para decenas de miles de usuarios.

**Privacidad:** no subir datasets reales, identificadores de clientes ni información comercial confidencial al repositorio público.
