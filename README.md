## ⚠️ Nota: Cambio de tema entre Evidencia 1 y Evidencia 2

Este repositorio contiene el trabajo de ambas evidencias del curso **Programación para Análisis de Datos (2026-1)**.

### Evidencia 1 — Metodología CRISP-DM (Tema original)
- **Tema:** Análisis de patrones de homicidio en Colombia fuera del conflicto armado.
- **Fuente de datos:** Dataset de homicidios del Ministerio de Defensa ([datos.gov.co](https://www.datos.gov.co/Seguridad-y-Defensa/HOMICIDIO/m8fd-ahd9/about_data/)).
- **Archivos:** Ver carpeta `/Evidencia_1/`

### Evidencia 2 — Etapa 3 CRISP-DM: Web Scraping (Nuevo tema)
- **Tema:** Extracción y almacenamiento de datos de vuelos de llegada y salida desde el portal de la Aeronáutica Civil.
- **Fuente de datos:** [aerocivil.gov.co](https://www.aerocivil.gov.co)
- **Herramientas:** Selenium + BeautifulSoup + SQL Server (ETL)
- **Archivos:** Ver carpeta `/Evidencia_2/`

El cambio de temática fue una decisión del equipo para trabajar con datos dinámicos en tiempo real y aplicar técnicas de web scraping con paginación JavaScript, alineándose mejor con los objetivos de la Evidencia 2.



# Evidencia de Aprendizaje 1: Metodología CRISP-DM

**Integrantes**: 

* Juan Fernando Cataño Higuita
* Óscar Javier García García
* Rober Andrés Castillo Gaviria
* Juan David Ramírez García

**Docente**: Ana María López Moreno

**Universidad**: INSTITUCIÓN UNIVERSITARIA DIGITAL DE ANTIOQUIA

## 1. Definición de la necesidad

Históricamente, el homicidio en Colombia se ha analizado desde la perspectiva del conflicto armado y el narcotráfico. Sin embargo, esta violencia no es uniforme; también se manifiesta mediante diversas dinámicas en contextos rurales y urbanos, como hurtos, riñas, sicariatos, etc.
El objetivo de este trabajo es analizar cómo este otro tipo de homicidios ha afectado a Colombia a lo largo del tiempo y en sus regiones, utilizando el dataset para comprender la problemática en su modalidad y sus causas.

**Pregunta de negocio o de la problemática**: ¿qué patrones de homicidio existen fuera del conflicto?


## 2. Diseño de la necesidad

Objetivos de negocio:

* Identificar los diferentes tipos de violencia por las diversas regiones de Colombia para apoyar la toma de decisiones en seguridad ciudadana.
* Clasificar los homicidios por modalidad y zona para distinguir la violencia común de la violencia por conflicto armado.


Fuentes de datos relevantes:

* Conjunto de datos:[dataset homicidios](https://www.datos.gov.co/Seguridad-y-Defensa/HOMICIDIO/m8fd-ahd9/about_data/ )
* Fuente: Datos abiertos del Ministerio de Defensa. Última actualización 24 de abril del 2026 [Aquí](https://www.mindefensa.gov.co/)

![Alt text](doc/ELTimagen.drawio.png)

![Alt text](doc/flujoproblematicaimagen.drawio.png)

# 3. Modelos de diseño

Se va a utilizar un modelo estrella para responder a los objetivos de negocio, mediante las siguientes tablas: Hechos_Homicidios, Dim_Modalidad, Dim_Municipio, Dim_Departamento y Dim_arma

Relaciones del modelo

* Entre la tabla Hechos_Homicidios y Dim_Modalidad se estableció una relación de Muchos a Uno (N:1) a través de los campos id_modalidad como Clave Foránea en Hechos_Homicidios  y Clave Primaria en la tabla Dim_Modalidad.

* Entre la tabla Hechos_Homicidios y Dim_Municipio se estableció una relación de Muchos a Uno (N:1) a través de los campos cod_muni como clave foránea y clave primaria en la tabla Dim_Municipio.

* Entre la tabla Dim_Municipio y Dim_Departamento existe una relación de Muchos a Uno (N:1) a través de los campos cod_depto. 

* Entre la tabla Hechos_Homicidios y Dim_Arma se establece una relación de Muchos a Uno (N:1) a través de los campos id_arma.

![Alt text](doc/entidad_relacion.png)

## Conexión y carga de pruebas de la base de datos

Vamos a cargar nuestro dataset desde el archivo homicidio.csv a una base de datos llamada HomicidiosDB en SQL Server, donde cargaremos los datos crudos en unas tablas Staging para una futura transformación y limpieza. 

Usamos este [ELT](Notebook/etl.py) para dicha tarea.

- `Evidencia_1/`
  - `data/`
    - `homicidio.csv` — Dataset original del Ministerio de Defensa
  - `notebook/`
    - `etl.py` — Script de carga y transformación
  - `doc/`
    - `imagenes.png` — Diagramas, modelo estrella y flujos
  - `SQL/`
    - `staging_tables.sql` — Creación de tablas en SQL Server
  - `Evidencia_1_CRISP-DM.pdf` — Documentación metodológica completa


# Evidencia de Aprendizaje 2: Etapa 3 de la Metodología CRISP-DM — Web Scraping


## 1. Definición de la necesidad
El seguimiento en tiempo real del estado de los vuelos en Colombia es una necesidad tanto para pasajeros como para entidades de transporte y autoridades aeronáuticas. Sin embargo, la información publicada por la Aeronáutica Civil en su portal web no está disponible en un formato estructurado descargable, lo que dificulta su análisis histórico y comparativo. El objetivo de este trabajo es extraer, transformar y almacenar de manera automatizada los datos de vuelos de llegada y salida publicados en el portal de la Aeronáutica Civil (aerocivil.gov.co), aplicando la etapa de preparación de datos de la metodología CRISP-DM mediante técnicas de web scraping.


Pregunta de negocio o de la problemática: ¿Cuál es el estado operativo de los vuelos de llegada y salida en Colombia, y qué patrones pueden identificarse a partir de la información publicada por la Aeronáutica Civil?


## 2. Diseño de la necesidad
Objetivos de negocio:

Automatizar la extracción de datos de vuelos de llegada y salida desde el portal de la Aeronáutica Civil para construir una base de datos estructurada que permita análisis posteriores.
Identificar patrones en la operación aérea colombiana, como las aerolíneas con mayor volumen de vuelos, los orígenes y destinos más frecuentes, y la distribución de vuelos nacionales e internacionales.

Fuentes de datos relevantes:

* Vuelos de llegada: https://www.aerocivil.gov.co
* Vuelos de salida: https://www.aerocivil.gov.co
* Fuente: Portal oficial de la Aeronáutica Civil de Colombia.


## 3. Modelos de diseño
Se diseñó un modelo relacional en SQL Server Express compuesto por tablas de staging independientes y una tabla de hechos unificada, siguiendo la misma lógica de separación entre datos crudos y datos transformados utilizada en la Evidencia 1.
Tablas del modelo:

Staging_Llegada: almacena los registros crudos extraídos del scraper de vuelos de llegada.
Staging_Salida: almacena los registros crudos extraídos del scraper de vuelos de salida.
Fact_Vuelos: tabla de hechos unificada que consolida tanto los vuelos de llegada como los de salida, con los datos ya transformados y limpios.

### Campos del modelo:

Cada tabla contiene los campos: aerolinea, numero_vuelo, ciudad_conexion, hora_estimada, fecha_vuelo, tipo_de_vuelo, estado y tipo_movimiento.
Relaciones del modelo:

Las tablas Staging_Llegada y Staging_Salida son independientes entre sí y actúan como fuente para la tabla Fact_Vuelos.
La tabla Fact_Vuelos consolida verticalmente ambas tablas de staging mediante una operación pd.concat(), diferenciando cada registro por el campo tipo_movimiento con los valores Llegada o Salida.

### Conexión y carga de prueba de la base de datos:

Los datos fueron cargados desde los archivos CSV generados por los scrapers hacia la base de datos EstadosVuelosDB en SQL Server Express, usando SQLAlchemy como conector y pandas para las transformaciones. El proceso ETL limpia los espacios en los nombres de columnas, normaliza el campo aerolínea extrayendo el nombre desde la URL de la imagen, elimina duplicados por número de vuelo y carga los datos en las tablas correspondientes.

El script ETL completo está disponible en el repositorio: etl.py
Estructura del repositorio:

documentación metodológica completa


- `Evidencia_2/`
  - `scrapers/`
    - `scraper_llegadas.py` — Scraper de vuelos de llegada
    - `scraper_salidas.py` — Scraper de vuelos de salida
  - `etl/`
    - `etl.py` — Script ETL de carga a SQL Server
  - `output/`
    - `vuelos_llegadas_selenium.csv`
    - `vuelos_salidas_selenium.csv`
  - `doc/`
    - `imagenes.png` — Diagramas y capturas del proceso
  - `SQL/`
    - `staging_tables.sql` — Creación de tablas en SQL Server
  - `Evidencia_2_web_scraping.pdf` — Documentación metodológica completa











