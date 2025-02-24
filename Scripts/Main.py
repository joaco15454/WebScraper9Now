import subprocess  
import time  
import json  

class Main:  
    def __init__(self):  
        self.scraper_live_channels = "ScraperLive247.py"
        self.scraper_tv_guide = "ScraperChannelGuide.py"
        self.limpieza_csv = "limpiador.py"

    def run_script(self, script_name):  
        try:  
            start_time = time.time()
            subprocess.run(["python", script_name], check=True)  
            execution_time = time.time() - start_time
            return execution_time  
        except subprocess.CalledProcessError as e:  
            print(f"Error al ejecutar {script_name}: {e}")  
            return None  

    def execute_all(self):  
        total_execution_time = 0  

        for script in [self.scraper_live_channels, self.scraper_tv_guide, self.limpieza_csv]:  
            execution_time = self.run_script(script)  
            if execution_time is not None:  
                total_execution_time += execution_time  
        
        with open("execution_time.json", "w") as json_file:  
            json.dump({"total_execution_time_seconds": total_execution_time}, json_file)  

if __name__ == "__main__":  
    main = Main()  
    main.execute_all()  