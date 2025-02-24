import time
import os
import csv  
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains

def setup_driver():  
    options = Options()  
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")  
    options.add_argument("--disable-search-engine-choice-screen")  
    options.add_argument("--ignore-certificate-errors")  
    options.add_argument("--allow-running-insecure-content")
    driver = webdriver.Chrome(options=options)  
    return driver  

def get_day_buttons(driver):  
    day_nav_list = driver.find_element(By.XPATH, "//ul[contains(@class, 'day-nav__list')]")  
    return day_nav_list.find_elements(By.TAG_NAME, "li")  

def navigate_to_day(driver, day_button):
    time.sleep(0.5)
    a_tag = WebDriverWait(day_button, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "a"))
    )
    data_date = a_tag.get_attribute("data-date")  
    driver.execute_script("arguments[0].click();", a_tag)
    time.sleep(3)
    return data_date

def get_program_divs(driver):
    guide_grid = driver.find_element(By.CLASS_NAME, "guide__grid")  
    section = guide_grid.find_element(By.TAG_NAME, "section") 
    return section.find_elements(By.XPATH, ".//div[@data-channel-id]")

def go_to_morning_schedule(driver):
    morning_link = driver.find_element(By.CSS_SELECTOR, 'a[data-name="morning"]')
    driver.execute_script("arguments[0].click();", morning_link)
    time.sleep(0.5) 

def navigate_to_earliest_programs(driver):
    for _ in range(4):
        try:
            prev_link = driver.find_element(By.CSS_SELECTOR, 'a[data-tracking-link-name="nav_timeprev"]')
            driver.execute_script("arguments[0].click();", prev_link)
            time.sleep(0.5)
        except Exception as e:
            print(f"No se pudo hacer clic en prev_link: {e}")
            break 
    time.sleep(0.5)
def extract_program_info(driver, program_div, data_date, channel, cont_next_day):  
    try:
        rect = program_div.rect
        viewport_width = driver.execute_script('return window.innerWidth')
        is_in_viewport = rect['x'] + rect['width'] <= (viewport_width - 130)               
        if not is_in_viewport and cont_next_day < 9:
            print("Name: href")
            next_link = driver.find_element(By.CSS_SELECTOR, 'a[data-tracking-link-name="nav_timenext"]')
            driver.execute_script("arguments[0].click();", next_link)
            cont_next_day = cont_next_day + 1
            time.sleep(0.25)
        driver.execute_script("arguments[0].click();", program_div)
        show_content = WebDriverWait(driver, 1).until(  
            EC.presence_of_element_located((By.CLASS_NAME, "show-down__content"))  
        )
        WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'show-down') and contains(@class, 'loading')]")))
        close_button = show_content.find_element(By.TAG_NAME, "a")
        program_title = show_content.find_element(By.TAG_NAME, "h2").get_attribute("textContent")
        chapter_name = show_content.find_element(By.TAG_NAME, "h3").get_attribute("textContent")  
        description = show_content.find_element(By.XPATH, ".//p[contains(@class, 'show-down__description')]").get_attribute("textContent")  
        extra_info = show_content.find_element(By.XPATH, ".//p[contains(@class, 'show-down__tags' )]").get_attribute("textContent")  
        program_time = show_content.find_element(By.XPATH, ".//div//p[1]").get_attribute("textContent")
        driver.execute_script("arguments[0].click();", close_button)
        return [data_date, channel, program_title, chapter_name, description, extra_info, program_time, cont_next_day] 
    except Exception as e:  
        return None

def scrape_day(driver, day_button, all_data):  
    try:
        driver.execute_script("window.scrollTo(0, 0);")  
        data_date = navigate_to_day(driver, day_button)
        program_divs = get_program_divs(driver)
        for program_div in program_divs:
            channel = str(program_div.get_attribute("data-channel-name"))
            if channel == "9Now":
                continue
            go_to_morning_schedule(driver)
            navigate_to_earliest_programs(driver)
            cont_next_day = 0
            programs_channels = program_div.find_elements(By.XPATH, ".//div[contains(@class, 'guide__row__block')]")
            for  program_channel in programs_channels:
                if 'guide__row__block--yesterday' in program_channel.get_attribute('class'):
                    continue  
                div_program_channel = program_channel.find_element(By.XPATH, ".//div")
                program_link = WebDriverWait(div_program_channel, 1).until(  
                    EC.presence_of_element_located((By.TAG_NAME, "a")))
                print("Estoy por entrrar en program info")
                program_info = extract_program_info(driver, program_link, data_date, channel, cont_next_day)  
                if program_info:  
                    all_data.append(program_info[:-1])
                    cont_next_day = program_info[-1]

    except Exception as e:  
        print(f"Error scraping day {data_date}: {e}")  

def save_to_csv(data, output_file, execution_time):
    OUTPUT_FILE = os.path.join(".", "Files", output_file)  
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:  
        writer = csv.writer(f)  
        writer.writerow(["Fecha", "Canal", "Titulo", "Nombre Capitulo", "Descripcion", "Info adicional", "Horario"])  
        writer.writerows(data)  
        writer.writerow(["Tiempo de ejecución:", f"{execution_time:.2f} segundos"])  

def scrape_tv_guide():  
    base_url = "https://tvguide.9now.com.au/guide/"  
    output_file = "tv_guide_data_ultimate.csv"  
    all_data = []  
    driver = setup_driver()  
    driver.get(base_url)  
    driver.maximize_window()
    time.sleep(3)  
    start_time = time.time()  
    day_buttons = get_day_buttons(driver)  

    for day_button in day_buttons:  
        scrape_day(driver, day_button, all_data)  
    
    driver.quit()  
    
    execution_time = time.time() - start_time  
    save_to_csv(all_data, output_file, execution_time)  
    
    print(f"Scraping completado en {execution_time:.2f} segundos.")  

if __name__ == "__main__":  
    scrape_tv_guide()
