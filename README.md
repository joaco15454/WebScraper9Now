# Documentación del Proyecto de Scraping y Limpieza de Datos  

Este proyecto consta de tres scripts principales que realizan scraping de canales en vivo y guías de televisión, así como la limpieza de los datos obtenidos. A continuación se detalla cada uno de los scripts.  

## 1. `Main.py`  

Este script es el punto de entrada del programa. Se encarga de ejecutar los otros scripts en un orden específico y registrar el tiempo total de ejecución.  

### Clases y Métodos  

- **Clase `Main`**  
  - **Método `__init__`**: Inicializa los nombres de los scripts que se van a ejecutar.  
  - **Método `run_script(script_name)`**: Ejecuta un script dado y devuelve el tiempo de ejecución. Maneja errores en caso de que el script falle.  
  - **Método `execute_all()`**: Ejecuta todos los scripts en orden y guarda el tiempo total de ejecución en un archivo JSON.  

## 2. `ScraperLive247.py`  

Este script se encarga de hacer scraping de los canales en vivo desde el sitio web de 9Now.  

### Funciones Principales  

- **`configure_driver()`**: Configura el controlador de Selenium con opciones específicas para el navegador.  
- **`find_element_with_wait(driver, by, value, timeout)`**: Busca un elemento en la página con un tiempo de espera.  
- **`get_panel_title(driver)`**: Obtiene y muestra el título del panel de canales en vivo.  
- **`hover_over_element(driver, element)`**: Realiza un hover sobre un elemento para mostrar información adicional.  
- **`extract_channel_info(channel)`**: Extrae información relevante de un canal, como el enlace, horario, título y descripción.  
- **`get_live_channels(driver)`**: Obtiene todos los canales en vivo y almacena la información extraída.  
- **`save_data_to_csv(data, execution_time)`**: Guarda la información de los canales en un archivo CSV.  


---  

## 3. `ScrapperChannelGuide.py`  


Este script utiliza **Selenium** para extraer información de la guía de televisión de 9Now. Navega por los días disponibles, accede a los programas de cada canal y extrae detalles como el título, capítulo, descripción, horario y más.  

## Flujo del Script  
1. **Configura el WebDriver** con opciones para evitar bloqueos.  
2. **Obtiene los botones de días** disponibles en la guía.  
3. **Navega a cada día** y extrae la programación.  
4. **Encuentra los programas en la guía** y los ordena por horario.  
5. **Extrae la información de cada programa** abriendo su detalle.  
6. **Guarda los datos en un archivo CSV**, incluyendo el tiempo de ejecución.  

## Funciones Principales  

### `setup_driver()`  
Configura el **WebDriver de Chrome** con opciones para evitar bloqueos y problemas de certificados.  

### `get_day_buttons(driver)`  
Obtiene los botones de navegación de los días en la guía de TV.  

### `navigate_to_day(driver, day_button)`  
Hace clic en un día de la guía y espera a que cargue la programación.  

### `get_program_divs(driver)`  
Encuentra los **contenedores de programas** en la grilla de la guía.  

### `go_to_morning_schedule(driver)`  
Hace clic en la pestaña de **programas de la mañana**.  

### `navigate_to_earliest_programs(driver)`  
Navega hacia los programas más tempranos del día.  

### `extract_program_info(driver, program_div, data_date, channel, cont_next_day)`  
Extrae la información detallada de un programa, incluyendo:  
- **Fecha**  
- **Canal**  
- **Título del programa**  
- **Nombre del capítulo**  
- **Descripción**  
- **Información adicional**  
- **Horario**  

Si el programa no está completamente visible, intenta navegar hasta encontrarlo.  

### `scrape_day(driver, day_button, all_data)`  
Procesa un día completo de la guía de TV, recorriendo todos los programas y extrayendo su información.  

### `save_to_csv(data, output_file, execution_time)`  
Guarda los datos extraídos en un archivo **CSV**, agregando el tiempo de ejecución al final.  

### `scrape_tv_guide()`  
Función principal del script:  
1. Inicia el WebDriver y abre la guía de TV.  
2. Recorre cada día disponible en la guía.  
3. Extrae los programas y los guarda en el CSV.  
4. Finaliza la ejecución y muestra el tiempo total.  
