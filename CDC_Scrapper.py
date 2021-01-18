from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os

def main () :
	
	Webpath = 'https://covid.cdc.gov/covid-data-tracker/#vaccinations'
	cwd = os.getcwd()

	if not os.path.exists(cwd + "/Data"):
		os.makedirs(cwd + "/Data")
	browser = getWebpageData(Webpath,cwd)
	#result, Doses = getTotalDoses(browser)

	result = getStatesData(browser)

	if result :
		print ('Your data has downlaoded and is available at:' + cwd +'/Data/')
		browser.quit()


def getWebpageData(Webpath,cwd):
	
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=1920x1080")
	chrome_options.add_argument("--disable-notifications")
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--verbose')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-software-rasterizer')
	preferences = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": cwd + '/Data/',
                "directory_upgrade": True
            }
	chrome_options.add_experimental_option('prefs',preferences)
	if ((os.name) == 'posix') :
		driver_path = cwd + '/chromedriver'

	else :
		driver_path = cwd + '/chromedriver.exe'
	browser = webdriver.Chrome(executable_path= driver_path, chrome_options=chrome_options)
	browser.get(Webpath)
	delay = 6 # seconds
	try:
		myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'vaccinations-banner-wrapper')))
		print ("Page is ready!")
	except TimeoutException:
		print ("Loading took too much time!")
	return browser


def getTotalDoses (browser) :
	Total_Doses_Distributed = browser.find_element_by_xpath('//*[@id="vaccinations-banner-wrapper"]/div/div/div[1]/div/div/div').text
	Total_Doses_Administered = browser.find_element_by_xpath('//*[@id="vaccinations-banner-wrapper"]/div/div/div[2]/div/div/div').text
	Number_of_People_Receiving_1_or_More_Doses = browser.find_element_by_xpath('//*[@id="vaccinations-banner-wrapper"]/div/div/div[3]/div/div/div').text
	Number_of_People_Receiving_2_or_More_Doses = browser.find_element_by_xpath('//*[@id="vaccinations-banner-wrapper"]/div/div/div[4]/div/div/div').text
	All_Doses = browser.find_elements_by_xpath('//*[local-name()="svg"]/*[local-name()="g"]/*[local-name()="text"]')
	Pfizer_Doses = All_Doses[2].text
	Moderna_Doses = All_Doses[3].text
	Unidentified_Doses = All_Doses[4].text
	
	return True, [Pfizer_Doses,Moderna_Doses,Unidentified_Doses]

def getStatesData (browser) :
	csvbutton = browser.find_element_by_id('btnVaccinationsExport')
	table_button = browser.find_element_by_id('vaccinations-table-header-icon').click()
	csvbutton.click()
	browser.implicitly_wait(10)

	
	return True
		

if __name__=="__main__": 
    main() 








    