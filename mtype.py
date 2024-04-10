import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebPageInteraction:
    def __init__(self):
        binaryPath = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = binaryPath
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get('https://monkeytype.com/')
        self.resolution = 100

    def reset_resolution(self):
        self.resolution = 100
        
    def setup(self):
        print("Setting up the web driver")

    def teardown(self):
        print("Tearing down the web driver")
        self.driver.quit()

    
    def display_toast_message_ambience(self, message):
            script = f"""
            var toast = document.createElement('div');
            toast.style.position = 'fixed';
            toast.style.top = '20px';
            toast.style.left = '20px';
            toast.style.padding = '10px';
            toast.style.backgroundColor = '#333';
            toast.style.color = '#fff';
            toast.style.zIndex = '1000';
            toast.style.borderRadius = '5px';
            toast.textContent = '{message}';
            document.body.appendChild(toast);
            setTimeout(function() {{ document.body.removeChild(toast); }}, 3000);
            """
            self.driver.execute_script(script)

    def display_toast_message(self, message):
            script = f"""
            var toast = document.createElement('div');
            toast.style.position = 'fixed';
            toast.style.bottom = '20px';
            toast.style.right = '20px';
            toast.style.padding = '10px';
            toast.style.backgroundColor = '#333';
            toast.style.color = '#fff';
            toast.style.zIndex = '1000';
            toast.style.borderRadius = '5px';
            toast.textContent = '{message}';
            document.body.appendChild(toast);
            setTimeout(function() {{ document.body.removeChild(toast); }}, 3000);
            """
            self.driver.execute_script(script)

    def toggle_dark_theme_and_zoom(self):
        self.driver.get('https://docs.yworks.com/yfileshtml/#/home')

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'label.toggle')))

        label = self.driver.find_element(By.CSS_SELECTOR, 'label.toggle')
        label.click()
        
        time.sleep(3)
        
        self.driver.execute_script("document.body.style.zoom='110%'")
        time.sleep(2)

        self.driver.execute_script("document.body.style.zoom='120%'")
        time.sleep(2)
        
        self.driver.execute_script("document.body.style.zoom='130%'")
        time.sleep(3)
        print("Dark theme toggled and page zoomed to 130%")


    def adjust_resolution(self, api_response):
        if api_response['adjustment'] > 0:
            self.display_toast_message(f'PIR: {api_response["PIR"]} - Adjusting screen resolution')
            self.reset_resolution()
            self.resolution += api_response['adjustment']* 5
            # self.adjust_font('"Source Sans Pro","Helvetica Neue Light",HelveticaNeue-Light,"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif')
            print(self.resolution)
            script = f"document.body.style.zoom='{self.resolution}%'"
            self.driver.execute_script(script)
        # else:
        #     self.reset_resolution()
        #     self.resolution += api_response['adjustment']* 5
        #     # self.adjust_font('"Roboto", sans-serif')
        #     print(self.resolution)
        #     script = f"document.body.style.zoom='{self.resolution}%'"
        #     self.driver.execute_script(script)

    def adjust_theme(self, api_response):
        if 0 < api_response['brightness'] <= 15:
            self.display_toast_message_ambience(f'Ambient brightness: {api_response["brightness"]}')

            script = f"document.getElementById('contentWrapper').style.backgroundColor = '#010203';"
            self.driver.execute_script(script)
        elif 15 <= api_response['brightness'] < 20:
            self.display_toast_message_ambience(f'Ambient brightness:" {api_response["brightness"]} "- Adjusting theme')
            script = f"document.getElementById('contentWrapper').style.backgroundColor = '#2f3339';"
            self.driver.execute_script(script)
        elif 20 <= api_response['brightness'] <= 25:
            self.display_toast_message_ambience(f'Ambient brightness:" {api_response["brightness"]} "- Adjusting theme')
            script = f"document.getElementById('contentWrapper').style.backgroundColor = '#cfcfcf';"
            self.driver.execute_script(script)
        elif 25 <= api_response['brightness'] <= 30:
            self.display_toast_message_ambience(f'Ambient brightness:" {api_response["brightness"]} "- Adjusting theme')
            script = f"document.getElementById('contentWrapper').style.backgroundColor = '#2f3339';"
            self.driver.execute_script(script)
        else:
            self.display_toast_message_ambience(f'Ambient brightness:" {api_response["brightness"]} "- Adjusting theme')
            script = f"document.getElementById('contentWrapper').style.backgroundColor = '#fff9f2';"
            self.driver.execute_script(script)

    def call_endpoint_in_loop(self):
        response_dict = {}
        while True:
            try:
                response = requests.get('http://127.0.0.1:5000/adapt-ui2')
                if response.status_code == 200:
                    # Parse the JSON string into a Python dictionary
                    response_dict = response.json()
                    print(response_dict)
                    self.adjust_theme(response_dict)
                    self.adjust_resolution(response_dict)
                else:
                    print(f"Failed to call endpoint: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error calling endpoint: {e}")
            
            time.sleep(1) # Wait for 5 seconds before the next call

if __name__ == "__main__":
    interaction = WebPageInteraction()
    interaction.setup()
    # interaction.change_bgc()

    try:
        interaction.call_endpoint_in_loop()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
        interaction.teardown()