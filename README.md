# exchange-stadistics

Repositorio integral de la materia de estadistica aplicada. Aqui conviven:

- el pipeline reproducible del proyecto final (versiones en Python y en R),
- las diapositivas de las clases,
- hojas de ejercicios y bancos de preguntas,
- tablas auxiliares, diccionarios y otros documentos de referencia.

Todo queda en un solo lugar para estudiar, practicar y reconstruir los
entregables.

## Mapa de carpetas

- `Final Project/`: codigo, datos intermedios y assets del proyecto de curso.
  - `food_index.py` y `foodIndex.R` implementan el pipeline FFPI (ver detalles
    mas abajo).
  - `data/` almacena la ultima corrida (`ffpi_monthly.csv`, `.xlsx`, `ffpi_readme.txt`).
  - `Example/` contiene ejemplos de dataset final, data dictionary, graficas y
    slides (`docs/`).
- `Lectures/`: presentaciones PPTX de cada clase (01 a 07). Se pueden abrir sin
  dependencias especiales.
- `Practice Questions/`: PDFs de ejercicios (partes 1-4) y el subdirectorio
  `Agresti/` con los capitulos correspondientes del libro para practicar.
- `Extras/`: recursos rapidos como tablas Z/T, un diccionario de variables y
  hojas de calculo de ejemplo mencionadas en clase.
- Documentos sueltos en la raiz (`syllabus_Stat_Fall2025 (2).docx`,
  `Statistics_2025 (1).pptx`, `Appendix.docx`) para referencia rapida del curso.
- `.venv/`: entorno virtual opcional usado para correr el flujo en Python.

## Proyecto Final: pipeline Food Price Index

El objetivo del proyecto es reconstruir mensualmente el FAO Food Price Index
(FFPI) y generar los archivos que se consumen en reportes y slides.

### Requerimientos

#### Flujo en Python (`Final Project/food_index.py`)

- Python 3.10+ (en Windows puedes usar `py -3`).
- Dependencias en `Final Project/requirements.txt`
  (`pandas`, `requests`, `openpyxl`, `xlrd`).
- Conexion a internet y, opcionalmente, la variable `FRED_API_KEY` para ampliar
  el limite de la API de FRED.

#### Flujo en R (`Final Project/foodIndex.R`)

- R 4.x con `httr2`, `rvest`, `xml2`, `readr`, `readxl`, `writexl`, `dplyr`,
  `tibble`, `tidyr`, `lubridate`, `stringr`, `janitor` y `jsonlite`.
- Conexion a internet y la misma `FRED_API_KEY` si se desea.

### Instalacion rapida

Todos los comandos asumen que trabajas dentro de `Final Project/`.

```powershell
cd "Final Project"

# Python
py -3 -m venv .venv          # opcional pero recomendado
.venv\Scripts\Activate.ps1
py -3 -m pip install -r requirements.txt

# R (desde una sesion de R)
install.packages(c(
  "httr2","rvest","xml2","readr","readxl","writexl",
  "dplyr","tibble","tidyr","lubridate","stringr","janitor","jsonlite"
))
```

### Ejecucion

#### Pipeline en Python

```powershell
cd "Final Project"
py -3 food_index.py [opciones]
```

Opciones utiles:

- `--fred-only` fuerza el uso del fallback de FRED.
- `--start-year 2015` define el primer ano que se conserva (default 2010).
- `--out-dir data_ffpi` permite escribir en otra carpeta.
- `--fao-url https://...xlsx` evita la etapa de descubrimiento cuando ya
  conoces el enlace exacto publicado por FAO.

El script imprime los enlaces encontrados y confirma cada archivo generado bajo
`data/` (o el directorio indicado).

#### Pipeline en R

```powershell
cd "Final Project"
Rscript foodIndex.R
```

Los parametros principales (`start_year`, `use_fao`, rutas, etc.) viven en la
lista `cfg` al inicio del archivo. Ajustalos ahi para cambiar el periodo,
directorios o para desactivar temporalmente la ruta de FAO. Basta con que
`Rscript.exe` este en el PATH.

### Salidas y trazabilidad

Independientemente del lenguaje se crean los mismos artefactos dentro de
`Final Project/data/` (la carpeta se genera automaticamente):

- `ffpi_monthly.csv`: formato ancho con `ffpi_food`, `ffpi_cereals`,
  `ffpi_veg_oils`, `ffpi_dairy`, `ffpi_meat`, `ffpi_sugar` y campos informativos
  (`unit`, `base_period`, `source`, `source_url`, `retrieved_utc`).
- `ffpi_monthly.xlsx`: hoja `data` con el mismo contenido y una hoja `meta`
  con fuente primaria, filas exportadas y comando utilizado.
- `ffpi_readme.txt`: resumen de la ejecucion y notas sobre si se uso el
  fallback de FRED.

`Final Project/Example/` conserva una corrida de ejemplo (dataset de muestra,
diccionario, graficas PNG y slides en `docs/`) para documentar el entregable.
Reemplazalo cuando tengas datos reales.

## Material de apoyo del curso

- **Lectures** (`Lectures/`): abrir los PPTX para revisar teorias, formulas y
  ejemplos vistos en clase.
- **Practice Questions** (`Practice Questions/`): PDFs por unidad y la carpeta
  `Agresti/` con capitulos escaneados para ejercicios adicionales.
- **Extras** (`Extras/`): tablas Z/T de bolsillo, un diccionario de variables
  para el proyecto y hojas de calculo con distribuciones y muestras.
- **Documentos de referencia** (raiz del repo): syllabus oficial, un
  apendice con notas y la presentacion general de la materia.

## Consejos y solucion de problemas

- Define `FRED_API_KEY` para evitar limites bajos en consultas repetidas.
- Si FAO cambia los enlaces, usa `--fao-url` (Python) o edita
  `cfg$fao_pages` en `foodIndex.R` para apuntar al nuevo recurso.
- Ante errores de red, vuelve a ejecutar: ambos flujos tienen reintentos
  exponenciales y fallback automatico a FRED.
- El entorno `.venv/` es solo local; recrealo si clonas el repo en otra maquina.

## Y si solo necesito un flujo?

Elige el lenguaje que prefieras: Python resulta util donde no hay R disponible,
mientras que el script en R se integra mejor con pipelines tidyverse. Ambos
producen exactamente los mismos archivos, que luego alimentan a las diapositivas
y al paquete de ejemplo en `Final Project/Example/`. El resto de carpetas te
da el contexto teorico y todo el material de estudio para la materia completa.
