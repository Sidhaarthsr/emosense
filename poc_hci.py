import time
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

    def setup(self):
        print("Setting up the web driver")

    def teardown(self):
        print("Tearing down the web driver")
        self.driver.quit()

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


    def toggle_light_theme_and_reset_zoom(self):
        self.driver.get('https://docs.yworks.com/yfileshtml/#/home')

        checkbox_xpath = '//input[@ng-model="$root.docOptions.darkTheme"]'
        checkbox = self.driver.find_element(By.XPATH, checkbox_xpath)
        self.driver.execute_script("arguments[0].click();", checkbox)


        self.driver.execute_script("document.body.style.zoom='120%'")
        time.sleep(2)

        self.driver.execute_script("document.body.style.zoom='110%'")
        time.sleep(2)
        
        self.driver.execute_script("document.body.style.zoom='100%'")
        time.sleep(3)

        print("Page reset to original state")


    def change_bgc_by_css_selector(self, css_selector, color):
        script = f"""
        var elements = document.querySelectorAll('{css_selector}');
        for (var i = 0; i < elements.length; i++) {{
            elements[i].style.backgroundColor = '{color}';
        }}
        """
        self.driver.execute_script(script)

    def change_background_color(self, class_name, color):
        self.driver.get('https://docs.yworks.com/yfileshtml/#/home')

        wait = WebDriverWait(self.driver, 10)

        ele = self.driver.find_element(By.CSS_SELECTOR, class_name)
        ele.__setattr__(class_name, color)

    def change_bgc(self):
        # Navigate to the webpage
        self.driver.get('https://quickref.me/homebrew')

        # Refresh the page to ensure it's in a known state
        self.driver.refresh()
        time.sleep(1) # Wait for the page to load


        # Loop to transition between light blue and cyan colors
        while True:
            # # Change the background color to light blue
            # self.driver.execute_script("document.body.style.backgroundColor = '#323437';")
            # self.change_background_color('h3-wrap-list', '#323437')
            # self.change_background_color('.mdLayout .h3-wrap>.section', '#e2b714')
            # self.change_bgc_by_css_selector('.mdLayout .h3-wrap>.section>p', '#2c2e31')
            # # self.change_bgc_by_css_selector('.h3-wrap-list>.h3-wrap>h3', '#e2b714')
            # # self.change_bgc_by_css_selector('.mdLayout h3 a.h-anchor', '#e2b714')
            # self.change_bgc_by_css_selector('.mdLayout .h3-wrap>.section>pre', '#7e7e7e')
            # self.change_bgc_by_css_selector('.mdLayout .h3-wrap>.section>table', '#646669')

            

            time.sleep(3) # Wait for 1 second

            # # Change the background color to cyan
            # self.driver.execute_script("document.body.style.backgroundColor = 'cyan';")
            # self.change_background_color('h3-wrap-list', 'cyan')
            # self.change_background_color('section', 'cyan')
            # time.sleep(1) # Wait for 1 second


    def add_class_to_html_tag(self, class_name):
        script = f"""
        document.documentElement.classList.add('{class_name}');
        """
        self.driver.execute_script(script)

    
    def remove_class_from_html_tag(self, class_name):
        script = f"""
        document.documentElement.classList.remove('{class_name}');
        """
        self.driver.execute_script(script)


if __name__ == "__main__":
    interaction = WebPageInteraction()
    interaction.setup()
    # interaction.change_bgc()

    try:
        while True:
            # interaction.display_toast_message("Dark Mode + 130% Zoom")
            # interaction.toggle_dark_theme_and_zoom()
            interaction.change_background_color('body.theme-default', 'red')
            # interaction.display_toast_message("Light Mode + Default Zoom")
            # interaction.toggle_light_theme_and_reset_zoom()
            time.sleep(3) 
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
        interaction.teardown()



