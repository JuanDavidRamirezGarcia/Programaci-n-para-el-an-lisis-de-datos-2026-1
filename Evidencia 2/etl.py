import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de conexión
file_path_1= r'output\vuelos_llegadas_selenium.csv'
file_path_2= r'output\vuelos_salidas_selenium.csv'
server = r'LAPTOP-5G1JGRV9\SQLEXPRESS'
database = 'EstadosVuelosDB'

engine = create_engine(f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server')

def load_and_upload():
    
    print("Cargando datos desde CSV...")
    # Cargamos y limpiamos espacios en los nombres de las columnas
    df1= pd.read_csv(file_path_1)
    df2= pd.read_csv(file_path_2)
    df1.columns = df1.columns.str.strip() 
    df2.columns = df2.columns.str.strip() 

    create_tables_query = """
    DROP TABLE IF EXISTS Staging_LLegada;
    DROP TABLE IF EXISTS Staging_Salida;
    DROP TABLE IF EXISTS Fact_Vuelos;
    

    CREATE TABLE Staging_LLegada (
        id_llegada INT PRIMARY KEY IDENTITY(1,1),
        aerolinea VARCHAR(255),
        numero_vuelo INT,
        ciudad_conexion VARCHAR(255),
        hora_estimada VARCHAR(50),
        fecha_vuelo VARCHAR(50),
        tipo_de_vuelo VARCHAR(50),
        estado VARCHAR(255),
        tipo_movimiento VARCHAR(50),
        pagina_fuente VARCHAR(255)
    );

    CREATE TABLE Staging_Salida (
        id_salida INT PRIMARY KEY IDENTITY(1,1),
        aerolinea VARCHAR(255),
        numero_vuelo INT,
        ciudad_conexion VARCHAR(255),
        hora_estimada VARCHAR(50),
        fecha_vuelo VARCHAR(50),
        tipo_de_vuelo VARCHAR(50),
        estado VARCHAR(255),
        tipo_movimiento VARCHAR(50),
        pagina_fuente VARCHAR(255)
    );
    """
        

    with engine.connect() as connection:
        print("Limpiando y creando tablas...")
        connection.execute(text(create_tables_query))
        connection.commit()

    # --- CREACIÓN DE DIMENSIONES ---

    # Llegada: BORRAMOS DUPLICADOS PARA ASEGURAR QUE NUMERO_VUELO SEA ÚNICO
    llegada_df = df1[[ 'Aerolínea','Numero_Vuelo', 'Ciudad_Conexion', 'Hora_Estimada', 'Fecha_Vuelo', 'Tipo_de_Vuelo', 'Estado', 'Tipo_movimiento']].drop_duplicates(subset=['Numero_Vuelo'])
    llegada_df.columns = ['aerolinea', 'numero_vuelo', 'ciudad_conexion', 'hora_estimada', 'fecha_vuelo', 'tipo_de_vuelo', 'estado', 'tipo_movimiento']

    # Salida: BORRAMOS DUPLICADOS PARA ASEGURAR QUE NUMERO_VUELO SEA ÚNICO
    salida_df = df2[['Aerolínea','Numero_Vuelo', 'Ciudad_Conexion', 'Hora_Estimada', 'Fecha_Vuelo', 'Tipo_de_Vuelo', 'Estado', 'Tipo_movimiento']].drop_duplicates(subset=['Numero_Vuelo'])
    salida_df.columns = ['aerolinea', 'numero_vuelo', 'ciudad_conexion', 'hora_estimada', 'fecha_vuelo', 'tipo_de_vuelo', 'estado', 'tipo_movimiento']

   
    # Limpiar el campo aerolinea para extraer solo el nombre
    def limpiar_aerolinea(df):
        df["aerolinea"] = (df["aerolinea"]
           .str.split('/').str[-1]       # toma el nombre del archivo
           .str.split('_').str[-1]       # quita el prefijo numérico
           .str.replace(r'\.(jpg|jpeg|png)$', '', regex=True)  # quita extensión
           .str.title()                  # capitaliza → "Avianca", "Latam"
        ) 
        return df

    llegada_df = limpiar_aerolinea(llegada_df)
    salida_df = limpiar_aerolinea(salida_df)

    #---Carga de datos a staging---

    print("Cargando dimensiones de staging a SQL...")

    llegada_df.to_sql('Staging_LLegada', engine, if_exists='append', index=False)
    salida_df.to_sql('Staging_Salida', engine, if_exists='append', index=False)

    # Combinar ambas tablas (Verticalmente)
    df_hechos_vuelos = pd.concat([llegada_df, salida_df], ignore_index=True)

    # Cargar a SQL
    df_hechos_vuelos.to_sql('Fact_Vuelos', engine, if_exists='append', index=False)
    print("Carga completa. Datos insertados en Fact_Vuelos.")
    
if __name__ == "__main__":
    load_and_upload()