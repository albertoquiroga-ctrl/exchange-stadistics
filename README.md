# exchange-stadistics

Herramienta minima para reconstruir indicadores mensuales que alimentan el
proyecto de estadistica aplicada. El script original estaba escrito en R, pero
como esta maquina no tiene R ni Rscript en el PATH, ahora existe un flujo
equivalente en Python que no requiere instalar R.

## Requerimientos

- Python 3.10 o superior (en Windows puedes usar el lanzador `py -3`)
- Conexion a internet para descargar los datos
- Opcional: variable de entorno `FRED_API_KEY` para ampliar el limite de la API

Instala las dependencias una sola vez:

```powershell
py -3 -m pip install -r requirements.txt
```

Sugerencia: si prefieres aislar librerias, crea un entorno virtual con
`py -3 -m venv .venv` y activalo antes de instalar.

## Ejecutar el pipeline de Food Price Index

```powershell
py -3 food_index.py
```

El script intenta primero descubrir y descargar la version mas reciente del
FAO Food Price Index (FFPI). Si FAO esta inaccesible, cae automaticamente al
indice de alimentos del FMI via FRED (`PFOODINDEXM`). Puedes forzar el uso del
fallback con `--fred-only` o fijar el ano inicial con `--start-year 2015`.

### Salidas generadas

Se crean tres archivos bajo `data/` (el directorio se genera si no existe):

- `ffpi_monthly.csv` - datos en formato largo.
- `ffpi_monthly.xlsx` - hoja `data` + hoja `meta` con el contexto.
- `ffpi_readme.txt` - resumen textual de la ejecucion.

Cada fila incluye las columnas `ffpi_food`, `ffpi_cereals`, `ffpi_veg_oils`,
`ffpi_dairy`, `ffpi_meat` y `ffpi_sugar` (las sub-series no disponibles quedan
como `NA`). Tambien se anaden columnas informativas (`unit`, `base_period`,
`source`, `source_url`, `retrieved_utc`) para mantener trazabilidad.

### Y si quiero seguir usando R?

Si prefieres el script original (`foodIndex.R`), instala R desde
<https://cran.r-project.org/> y asegurate de que `Rscript.exe` este en tu PATH.
Una vez configurado, podras ejecutar `Rscript foodIndex.R`. El flujo en Python
es equivalente y resulta util cuando R no esta disponible.
