# exchange-stadistics

Utilidad ligera para reconstruir los indicadores mensuales que alimentan el
proyecto de estadistica aplicada. El repositorio incluye dos flujos que producen
las mismas salidas:

- `food_index.py` (Python): pensado para maquinas sin R instalado.
- `foodIndex.R` (R): script original con pipeline completo en tidyverse.

Ambos descubren la version mas reciente del FAO Food Price Index (FFPI) y, si
la descarga falla, recurren al indice de alimentos del FMI via FRED
(`PFOODINDEXM`).

## Requerimientos

### Flujo en Python

- Python 3.10 o superior (en Windows puedes usar el lanzador `py -3`).
- Dependencias de `requirements.txt` (pandas, requests, openpyxl, xlrd).
- Conexion a internet.
- Opcional: variable de entorno `FRED_API_KEY` para ampliar el limite de FRED.

### Flujo en R

- R 4.x con las librerias `httr2`, `rvest`, `xml2`, `readr`, `readxl`,
  `writexl`, `dplyr`, `tibble`, `tidyr`, `lubridate`, `stringr`, `janitor` y
  `jsonlite`.
- Conexion a internet y (opcional) la misma `FRED_API_KEY`.

Instala las dependencias una sola vez:

```powershell
# Python
py -3 -m venv .venv          # opcional pero recomendado
.venv\Scripts\Activate.ps1   # activa el entorno
py -3 -m pip install -r requirements.txt

# R (desde una consola de R)
install.packages(c(
  "httr2","rvest","xml2","readr","readxl","writexl",
  "dplyr","tibble","tidyr","lubridate","stringr","janitor","jsonlite"
))
```

## Uso

### Pipeline en Python

```powershell
py -3 food_index.py [opciones]
```

Opciones utiles:

- `--fred-only` fuerza el uso del fallback de FRED.
- `--start-year 2015` define el primer ano que se conserva (default 2010).
- `--out-dir data_ffpi` permite escribir en otra carpeta.
- `--fao-url https://...xlsx` evita la etapa de descubrimiento cuando ya
  conoces el enlace exacto publicado por FAO.

El script imprime en consola los enlaces encontrados y confirma cada archivo
generado bajo `data/` (o el directorio que indiques).

### Pipeline en R

```powershell
Rscript foodIndex.R
```

Los parametros principales (`start_year`, `use_fao`, rutas, etc.) estan en la
lista `cfg` al inicio del archivo. Ajustalos ahi si necesitas otro periodo,
un directorio diferente o si deseas desactivar temporalmente la ruta de FAO.
Basta con que `Rscript.exe` este en el PATH para ejecutar el pipeline completo.

## Salidas y trazabilidad

Independientemente del lenguaje que uses se crean los mismos artefactos
debajo de `data/` (el directorio se genera automaticamente):

- `ffpi_monthly.csv`: datos en formato ancho con las columnas
  `ffpi_food`, `ffpi_cereals`, `ffpi_veg_oils`, `ffpi_dairy`, `ffpi_meat`,
  `ffpi_sugar` mas campos informativos (`unit`, `base_period`, `source`,
  `source_url`, `retrieved_utc`).
- `ffpi_monthly.xlsx`: hoja `data` con el mismo contenido del CSV y hoja `meta`
  con detalles de la ejecucion (fuente primaria, cantidad de filas, comando).
- `ffpi_readme.txt`: resumen textual con fecha de generacion y notas sobre la
  fuente utilizada (incluye si se activo el fallback de FRED).

## Consejos y solucion de problemas

- Define `FRED_API_KEY` en tu entorno para acceder a cuotas mas amplias de la
  API de FRED y evitar limites en ejecuciones repetidas.
- Si FAO cambia nuevamente las rutas, puedes pasar `--fao-url` (Python) o
  sustituir temporalmente `cfg$fao_pages` en `foodIndex.R` para apuntar al
  recurso correcto.
- Ante errores de red intermitentes, vuelve a ejecutar el script: ambos flujos
  implementan reintentos exponenciales y el fallback automatico a FRED.

## Y si solo necesito un flujo?

Puedes elegir el lenguaje que prefieras. El codigo Python sirve como alternativa
cuando R no esta disponible, mientras que el script en R se integra mejor con
pipelines existentes en tidyverse. Ambos producen archivos compatibles para
consumir desde hojas de calculo o notebooks.
