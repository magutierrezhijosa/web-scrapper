##### Importamos #####

# Importar la API sincrona de Playwright 
from playwright.sync_api import sync_playwright
# Importamos la libreria de Expresiones Regulares
import re
# Importamos la libreria urljoin de Python para unir la URL_Base mas la URL relativa  que nos va a dar cuando recogamos el valor del "href"
from urllib.parse import urljoin

# CONSTANTES que vamos a usar para nuestro web scrapping
URL_BASE = "https://www.unido.org/publications" # Esta Url cambbiara dependiendo de la pagina a scrappear


########## Pasos que va a realizar nuesto scraper #####
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
    page.goto(URL_BASE)

    

    # Los datos que deseamos recoger de la pagina 
    # 1.TITULO
    # 2.FECHA
    # 3.PDF

    # Creamos la funcion para realizar el scrapp
    def scrapear_publicaciones(page):   

        # Defino una varaible diccionario para guardar los daatos y posteriormente enviarlos a un CSV
        results = []

        # Declaro una varaible para guardar el numero de pagina que llevamos recorridas
        page_number = 1

        while True:

            # Mostramos un titulo y el  numero de la pagina que estamos scrapeando
            print(f"\n============ SCRAPEANDO PAGINA {page_number} =================")

            # Le decimos que espere a que terrmine de cargar todo
            page.wait_for_load_state("networkidle")

            # Recogemos todos los items que vamos a scrapear
            # Mucho mejor usar locator() que query() REECOMENDACION Playwright
            items = page.locator("div.views-row")

            ############## Mostramos todas las publicaciones #############
            print("Publicaiones encontradas", items.count())

            total_items = items.count()

            # Creamos un bucle para iterar las diferentes publicaciones
            for i in range(total_items):

                # Llamamos a la funcion nth() para seleccionar un elemento concreto dentro de un conjunto que comparten un locator()
                item = items.nth(i)

                # Declaramos la variable que va a recoger el TITULO
                # Utilizamos get_by_role() por que es el selector mas estable y robusto no depende del HTML y resiste cambios CSS
                title = item.get_by_role("link").first.inner_text()

                ########### Mostramos los titulos #############
                print("Titulo de la publicacion : " , title)

                # Vamos a buscar dentro del elemento item el primer <p> que encuentre
                date_element = item.locator("p.text-body.mt-1") 
            
                # Recogemos la data del elemento seleccionado anteriormente
                date_text = date_element.first.text_content()

                # Ahora vamos a recoger solamente el valor del año utilizando Expresiones Regulares
                match = re.search(r"\b20\d{2}\b",date_text)

                # Transformamos el texto para guardarlo en la variable final en el caso de que lo haya encontrado 
                year = match.group() if match else None

            
                ########### Mostramos los FECHA #############    
                print("Esta es la fecha del documento : " , year)

                # Marcamos el elemento que vamos a sacar la informacion 
                meta_link = item.locator("a.unido-link.link")
            
                    
                # Recogemos el texto del link utilizando la referencia al "href" y lo guardamos
                href = meta_link.first.get_attribute("href")

                # Unimos la Url base mas el href reelativo 
                pdf_link = urljoin(URL_BASE,href) if href else None
                    
                ########### Mostramos el LINK #############    
                print("Esto es el link del PDF : " , pdf_link)

                # Guardamos los datos dentro del diccionario 
                results.append({
                    "title": title,
                    "year": year,
                    "link":pdf_link
                })
       
            # *********************************
            #           PAGINACION
            # *********************************

            # Declaro la variable para  seleccionar el elemento donde se encuentra el boton de next
            next_button = page.locator("li.page-item.pager__item--next a")

            # Mientras haya algun boton de siguiente seguimos paginando 
            if next_button.count() > 0 :

                # Mostramos un mensaje para informar que cambiamos de pagina
                print("➡️ Pasando a la siguiente página...")

                # Procedemos a hacer click en NEXT para pasar de pagina
                next_button.first.click()

                # Esperamos a la navegacion real 
                page.wait_for_load_state("networkidle")

                # Aumentamos en 1 el valor de la varaible que cuenta las pagina
                page_number += 1


            else:

                # Mostramos en pantalla que no hay mas pagina
                print("✅ No hay más páginas.")

                # Terminams la ejecucion 
                break

        return results  

    if __name__ == "__main__":
        results = scrapear_publicaciones(page)
        print(results)
    
    
    
    # CERRAMOS LA NAVEGACION 
    browser.close()
