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

## Estructura repositorio

```text
/
├── data/
│   └── homicidio.csv  # Dataset original 
├── notebook/
│   └── ELT.py # Script de carga y transformación
├──doc/
│   └── imagenes.png # Imágenes relacionadas al proyecto como diagramas y flujos
├── SQL/
│   └── staging_tables.sql     # Carga SQL Server 
├── README.md                  # Documentación del proyecto
└── _Evidencia_CRISP-DM.pdf    # Documentación metodológica completa



