import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de conexión
file_path = 'homicidio.csv'
server = r'LAPTOP-5G1JGRV9\SQLEXPRESS'
database = 'HomicidiosDB'

engine = create_engine(f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server')

def load_and_upload():
    
    print("Cargando datos desde CSV...")
    # Cargamos y limpiamos espacios en los nombres de las columnas
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip() 

    create_tables_query = """
    DROP TABLE IF EXISTS Staging_Homicidios;
    DROP TABLE IF EXISTS Staging_Municipio;
    DROP TABLE IF EXISTS Staging_Departamento;
    DROP TABLE IF EXISTS Staging_Arma;
    DROP TABLE IF EXISTS Staging_Modalidad;

    CREATE TABLE Staging_Departamento (
        cod_depto VARCHAR(50) PRIMARY KEY,
        departamento VARCHAR(255)
    );

    CREATE TABLE Staging_Municipio (
        cod_muni VARCHAR(50) PRIMARY KEY,
        municipio VARCHAR(255),
        cod_depto VARCHAR(50),
        FOREIGN KEY (cod_depto) REFERENCES Staging_Departamento(cod_depto)
    );

    CREATE TABLE Staging_Arma (
        id_arma INT PRIMARY KEY IDENTITY(1,1),
        arma_medio VARCHAR(255)
    );

    CREATE TABLE Staging_Modalidad (
        id_modalidad INT PRIMARY KEY IDENTITY(1,1),
        modalidad_presunta VARCHAR(255)
    );

    CREATE TABLE Staging_Homicidios (
        id_homicidio INT PRIMARY KEY IDENTITY(1,1),
        fecha_hecho DATE,
        cod_muni VARCHAR(50),
        id_arma INT,
        id_modalidad INT,
        zona VARCHAR(50),
        sexo VARCHAR(50),
        cantidad INT,
        FOREIGN KEY (cod_muni) REFERENCES Staging_Municipio(cod_muni),
        FOREIGN KEY (id_arma) REFERENCES Staging_Arma(id_arma),
        FOREIGN KEY (id_modalidad) REFERENCES Staging_Modalidad(id_modalidad)
    );
    """

    with engine.connect() as connection:
        print("Limpiando y creando tablas...")
        connection.execute(text(create_tables_query))
        connection.commit()

    # --- CREACIÓN DE DIMENSIONES ---
    
    # Departamento: BORRAMOS DUPLICADOS PARA ASEGURAR QUE COD_DEPTO SEA ÚNICO
    depto_df = df[['COD_DEPTO', 'DEPARTAMENTO']].drop_duplicates(subset=['COD_DEPTO'])
    depto_df.columns = ['cod_depto', 'departamento']

    # MUNICIPIO: BORRAMOS DUPLICADOS PARA ASEGURAR QUE COD_MUNI SEA ÚNICO
    muni_df = df[['COD_MUNI', 'MUNICIPIO', 'COD_DEPTO']].drop_duplicates(subset=['COD_MUNI'])
    muni_df.columns = ['cod_muni', 'municipio', 'cod_depto']

    # Arma
    arma_df = df[['ARMA MEDIO']].drop_duplicates()
    arma_df.columns = ['arma_medio']

    # Modalidad: Limpiamos espacios para evitar problemas de mapeo
    mod_df = df[['MODALIDAD PRESUNTA']].drop_duplicates()
    mod_df.columns = ['modalidad_presunta']

    #---Carga de datos a staging---

    print("Cargando dimensiones de staging a SQL...")

    depto_df.to_sql('Staging_Departamento', engine, if_exists='append', index=False)
    muni_df.to_sql('Staging_Municipio', engine, if_exists='append', index=False)
    arma_df.to_sql('Staging_Arma', engine, if_exists='append', index=False)
    mod_df.to_sql('Staging_Modalidad', engine, if_exists='append', index=False)

    # --- CARGA DE HECHOS ---
    print("Mapeando IDs y cargando Hechos...")

    db_armas = pd.read_sql("SELECT id_arma, arma_medio FROM Staging_Arma", engine)
    db_mods = pd.read_sql("SELECT id_modalidad, modalidad_presunta FROM Staging_Modalidad", engine)

    hechos_df = df.copy()
    hechos_df = hechos_df.merge(db_armas, left_on='ARMA MEDIO', right_on='arma_medio')
    hechos_df = hechos_df.merge(db_mods, left_on='MODALIDAD PRESUNTA', right_on='modalidad_presunta')

    hechos_final = hechos_df[['FECHA HECHO', 'COD_MUNI', 'id_arma', 'id_modalidad', 'ZONA', 'SEXO', 'CANTIDAD']]
    hechos_final.columns = ['fecha_hecho', 'cod_muni', 'id_arma', 'id_modalidad', 'zona', 'sexo', 'cantidad']
    hechos_final['fecha_hecho'] = pd.to_datetime(hechos_final['fecha_hecho'], dayfirst=True)

    hechos_final.to_sql('Staging_Homicidios', engine, if_exists='append', index=False)
    print("¡Proceso completado sin errores!")

if __name__ == "__main__":
    load_and_upload()