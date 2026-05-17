"""
Actividad de aprendizaje 2 - CRIPS-DM FASE 3 -WEB SCRAPING
Objetivo: Extraer estado de vuelos (Llegadas) de la Aerocivil
Resultado: CSV con Aerolínea, Vuelo, Origen, Hora y Estado
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# ── Configuración ──
# URL específica de salidas de la Aerocivil

URL_AEROCIVIL = "https://www.aerocivil.gov.co/loader.php?lServicio=Aerolineas&lTipo=User&lFuncion=VistaUsuario&salida=N&vuelo=&aerolinea=&origen="

def crear_driver():
    """Crea instancia de Chrome con opciones para scraping."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extraer_vuelos_con_paginacion(driver, max_paginas=10):
    """Navega por todas las páginas disponibles y extrae los vuelos."""
    todos_los_vuelos = []
    pagina_actual = 1

    print(f"Navegando a: {URL_AEROCIVIL}")
    driver.get(URL_AEROCIVIL)

    while pagina_actual <= max_paginas:
        print(f" Procesando página {pagina_actual}...")
        
        # 1. Esperar a que la tabla de la página actual esté lista
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
        except:
            print("No se pudo cargar la tabla.")
            break

        # 2. Extraer datos de la página actual con BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "lxml")     
        tabla = soup.find("table")
        if tabla:
            filas = tabla.find_all("tr")
            for fila in filas:
                 cols = fila.find_all("td")
                 if len(cols) >= 5:
                     vuelo = {
                         "Aerolínea": cols[0].find("img")["src"].strip() if cols[0].find("img") else "",
                        "Numero_Vuelo": cols[1].get_text(strip=True),
                        "Ciudad_Conexion": cols[2].get_text(strip=True),
                        "Hora_Estimada": cols[3].get_text(strip=True),
                        "Fecha_Vuelo": cols[5].get("data-fecha-archivo", "").strip(),
                        "Tipo_de_Vuelo": cols[5].get_text(strip=True),
                        "Estado": cols[6].get_text(strip=True),
                        "Tipo_movimiento": "Salida",
                        "Pagina_Fuente": pagina_actual
                     }
                     if vuelo["Aerolínea"].lower() != "aerolínea":
                         todos_los_vuelos.append(vuelo)

        # 3. Intentar ir a la siguiente página
        try:
            boton_siguiente = driver.find_element(By.CSS_SELECTOR, "button.page-link.next") 

            if "disabled" in boton_siguiente.get_attribute("class"):
                print("No hay más páginas disponibles.")
                break
            else:
                boton_siguiente.click()
                pagina_actual += 1
                time.sleep(2)  # Esperar a que la nueva página cargue
        except:
            print("No se pudo encontrar el botón de siguiente o no hay más páginas.")
            break
    return todos_los_vuelos

def main():
    print("=" * 60)
    print("  SCRAPER AEROCIVIL - ESTADO DE VUELOS DE SALIDA")
    print("=" * 60)

    driver = crear_driver()
    
    try:
        # Extraer datos
        datos_vuelos = extraer_vuelos_con_paginacion(driver, max_paginas=10)
        
        if not datos_vuelos:
            print("No se obtuvieron datos.")
            return

        # Paso 4: Guardar en CSV con Pandas
        df = pd.DataFrame(datos_vuelos)
        
        # Crear carpeta de salida
        if not os.path.exists("output"):
            os.makedirs("output")

        archivo_csv = "output/vuelos_salidas_selenium.csv"
        df.to_csv(archivo_csv, index=False, encoding="utf-8-sig")

        print(f"\n{'=' * 60}")
        print(f"  Datos guardados en: {archivo_csv}")
        print(f"  Total de vuelos capturados: {len(df)}")
        print(f"{'=' * 60}")
        
        # Vista previa en consola
        print("\nVista previa de los primeros vuelos:")
        print(df.head(10).to_string(index=False))

    finally:
        driver.quit()
        print("\nNavegador cerrado.")

if __name__ == "__main__":
    main()