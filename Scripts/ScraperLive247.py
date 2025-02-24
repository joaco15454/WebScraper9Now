import csv
import os
from time import sleep, time
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains

BASE_URL = "https://www.9now.com.au"  
LIVE_CHANNEL_PATH = "/?selectedTab=Live+24%2F7"  
OUTPUT_FILE = os.path.join(".", "Files", "live_channels.csv") 

def configure_driver():  
    options = Options()  
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")  
    options.add_argument("--disable-search-engine-choice-screen")   

    driver = webdriver.Chrome(options=options)  
    driver.get(BASE_URL + LIVE_CHANNEL_PATH)  
    return driver  

def find_element_with_wait(driver, by, value, timeout=10):  
    wait = WebDriverWait(driver, timeout)  
    return wait.until(EC.presence_of_element_located((by, value)))  

def get_panel_title(driver):  
    try:  
        panel = find_element_with_wait(driver, By.ID, "live-24/7-panel", timeout=5)  
        title = panel.find_element(By.CSS_SELECTOR, "h2").text  
        print("Título del panel:", title)  
    except Exception as e:  
        print("No se encontró el título:", e)  

def hover_over_element(driver, element):  
    actions = ActionChains(driver)  
    actions.move_to_element(element).perform()  
    try:  
        WebDriverWait(driver, 5).until(  
            lambda d: d.find_element(By.CLASS_NAME, "sdui_card__inner_content")  
        )  
    except Exception as e:  
        print("No se encontro la ventana emergente:", e)  

def extract_channel_info(channel):  
    print("Data-testid: " + channel.get_attribute("data-testid"))  
    try:  
        first_div = channel.find_element(By.XPATH, "//div[contains(@class, 'sdui_card__secondary_view secondary-card-view')]")  
        link = first_div.find_element(By.TAG_NAME, "a")  
        links = link.get_attribute("href")  

        sections = link.find_elements(By.TAG_NAME, "section")   
        hour_span = sections[0].find_elements(By.TAG_NAME, "span")  
        horario = hour_span[-1].get_attribute("textContent")  

        program_name = sections[1].find_element(By.XPATH, ".//span[2]//span") \
            if "Card-channel" in channel.get_attribute("data-testid") \
            else sections[1].find_element(By.XPATH, ".//span[1]//span")  
        title = program_name.get_attribute("textContent")  

        description = sections[2].find_element(By.XPATH, ".//div//p").get_attribute("textContent")  

        return {  
            "link": links,  
            "rango_horario": horario,  
            "titulo": title,  
            "descripcion": description  
        }  
    except Exception as e:  
        print(f"Error extrayendo informacion de canal: {e}")  
        return None  

def get_live_channels(driver):  
    driver.maximize_window()  
    try:  
        panel = WebDriverWait(driver, 5).until(  
            EC.presence_of_element_located((By.ID, "live-24/7-panel"))  
        )  

        channels = WebDriverWait(panel, 10).until(  
            lambda p: p.find_elements(By.XPATH, './/div[contains(@data-testid, "Card-")]')  
        )  
        channel_data = []  
        for channel in channels:  
            hover_over_element(driver, channel)  
            data = extract_channel_info(channel)  
            if data:  
                channel_data.append(data)  

        return channel_data  

    except Exception as e:  
        print("No se encontraron canales:", e)  
        return []  

def save_data_to_csv(data, execution_time):  
    if not data:  
        print("No hay datos para guardar")  
        return  

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:  
        writer = csv.DictWriter(file, fieldnames=["link", "rango_horario", "titulo", "descripcion"])  
        writer.writeheader()  
        writer.writerows(data)  
        writer.writerow({"link": "Tiempo de ejecución de scrapeo:", "rango_horario": execution_time, "titulo": "", "descripcion": ""})  

def main():      
    start_time = time()
    driver = configure_driver()  
    sleep(3)  

    get_panel_title(driver)  
    live_channels = get_live_channels(driver)  
    execution_time = time() - start_time
    save_data_to_csv(live_channels, execution_time)  

    driver.quit()  

if __name__ == "__main__":  
    main()