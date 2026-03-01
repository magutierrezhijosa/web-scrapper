##### Importamos #####

# Importar la API sincrona de Playwright 
from playwright.sync_api import sync_playwright



# CONSTANTES que vamos a usar para nuestro web scrapping
URL_SCRAP = "https://www.unido.org/publications" # Esta Url cambbiara dependiendo de la pagina a scrappear


# Definimos la funncion que va a realizar el scrapping



# Definimos la funcion especial de Playwright (sync_playwright) que hace:
#    ✅ inicia el motor de automatización
#    ✅ conecta Python con el navegador
#    ✅ prepara Chromium / Firefox / WebKit

# Declaramos el Context Manager (with)
with sync_playwright() as p:

    #  Llamando a (p)  que es el controlador principal de Playwright el cual contiene los navegadores y lo lanzamos
    browser = p.chronium.launch(headless=False) # True  = navegador invisible/ False = visible
