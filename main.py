##### Importamos #####

# Importar la API sincrona de Playwright 
from playwright.sync_api import sync_playwright



# CONSTANTES que vamos a usar para nuestro web scrapping
URL_SCRAP = "https://www.unido.org/publications" # Esta Url cambbiara dependiendo de la pagina a scrappear


########## Pasos que va a realizar nuesto scrape #####
# 1. Inicia Playwright
# 2. Abre un navegador Chromium automático
# 3. Abre una pestaña
# 4. Va a una web
# 5. Espera 5 segundos
# 6. Cierra el navegador



# Definimos la funcion especial de Playwright (sync_playwright) que hace:
#    ✅ inicia el motor de automatización
#    ✅ conecta Python con el navegador
#    ✅ prepara Chromium / Firefox / WebKit

# Declaramos el Context Manager (with)
with sync_playwright() as p:

    #  Llamando a (p)  que es el controlador principal de Playwright el cual contiene los navegadores y lo lanzamos
    browser = p.chromium.launch(headless=False) # True  = navegador invisible/ False = visible

    # Creamos una nueva pestaña
    page  = browser.new_page()

    # Vamos a la web que queremos hacer el scrapping
    page.goto(URL_SCRAP)

    # Le decimos que espere a que terrmine de cargar todo
    page.wait_for_load_state("networkidle")

    # Recogemos todos los items qque vamos a scrapear
    items = page.locator("div.views-row")

    # Elentos que deseamos recoger de la pagina 
    # 1.TITULO
    # 2.FECHA
    # 3.PDF
    
    # Cerramos el navegador
    browser.close()
