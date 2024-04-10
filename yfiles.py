import time
import requests
import json
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
        self.driver.get('https://docs.yworks.com/yfileshtml/#/home')
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
            toast.style.backgroundColor = '#fffdde';
            toast.style.color = 'black';
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
            toast.style.backgroundColor = '#fffdde';
            toast.style.color = 'black';
            toast.style.zIndex = '1000';
            toast.style.borderRadius = '5px';
            toast.textContent = '{message}';
            document.body.appendChild(toast);
            setTimeout(function() {{ document.body.removeChild(toast); }}, 3000);
            """
            self.driver.execute_script(script)


    def adjust_resolution(self, api_response):
        if api_response['adjustment'] > 0:
            self.display_toast_message(f'PIR: {api_response["PIR"]} - Adjusting screen resolution')
            self.reset_resolution()
            self.resolution += api_response['adjustment']* 5
            self.adjust_font('"Source Sans Pro","Helvetica Neue Light",HelveticaNeue-Light,"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif')
            print(self.resolution)
            script = f"document.body.style.zoom='{self.resolution}%'"
            self.driver.execute_script(script)
        else:
            self.display_toast_message(f'PIR: {api_response["PIR"]} - Adjusting screen resolution')
            self.reset_resolution()
            self.resolution += api_response['adjustment']* 5
            self.adjust_font('"Roboto", sans-serif')
            print(self.resolution)
            script = f"document.body.style.zoom='{self.resolution}%'"
            self.driver.execute_script(script)

    def adjust_theme(self, api_response):
        # Find the <body> element
        body_element = self.driver.find_element(By.TAG_NAME, 'body')

        # Get the class attribute of the <body> element
        class_attribute = body_element.get_attribute('class')
    
        # Split the class attribute string into a list of class names
        class_names = class_attribute.split()
        self.display_toast_message_ambience(f'Ambient brightness: {api_response["brightness"]}')

        if 'theme-default' in class_names and api_response['brightness'] >= 20:
            pass
        elif 'theme-default' not in class_names and api_response['brightness'] >= 20:
            self.toggle_theme()
        elif 'theme-dark' in class_names and api_response['brightness'] <= 20:
            pass
        else:
            self.toggle_theme()

    def adjust_font(self, font_family):
        font_family = '"Roboto", sans-serif'
        script = f"""
        document.querySelector('html').style.fontFamily = '{font_family}';
        document.querySelectorAll('input').forEach(function(input) {{
            input.style.fontFamily = '{font_family}';
        }});
        """
        self.driver.execute_script(script)
    
    def toggle_theme(self):
        checkbox_xpath = '//input[@ng-model="$root.docOptions.darkTheme"]'
        checkbox = self.driver.find_element(By.XPATH, checkbox_xpath)
        self.driver.execute_script("arguments[0].click();", checkbox)


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
            
            time.sleep(2) # Wait for 5 seconds before the next call

if __name__ == "__main__":
    interaction = WebPageInteraction()
    interaction.setup()

    try:
        interaction.call_endpoint_in_loop()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
        interaction.teardown()



