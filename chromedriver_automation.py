# automacao-vendas-recorrentes/chromedriver_automation.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

def baixar_planilha():
    load_dotenv()
    email = os.getenv("EMAIL")
    senha = os.getenv("SENHA")
    driver_path = r"C:\Users\User\Downloads\chromedriver-win64\chromedriver.exe"
    
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    
    driver.get("https://apprecorrente.com/login/login")
    time.sleep(1)
    
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)
    
    senha_field = driver.find_element(By.NAME, "senha")
    senha_field.send_keys(senha)
    
    time.sleep(1)
    login_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/form/button")
    login_button.click()
    time.sleep(3)
    
    # Acessa o menu de vendas
    vendas_element = driver.find_element(By.XPATH, "//*[@id='side-menu']/li[6]/ul/li/a/span")
    driver.execute_script("arguments[0].click();", vendas_element)
    time.sleep(2)
    
    data_de_field = driver.find_element(By.XPATH, '//*[@id="datade"]/input')
    driver.execute_script("arguments[0].value = '';", data_de_field)
    time.sleep(1)
    driver.execute_script("arguments[0].value = '01/01/2022';", data_de_field)
    time.sleep(1)
    data_de_field.send_keys(Keys.ENTER)
    time.sleep(1)
    
    refresh_button = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div/div/div/div[2]/ng-form/div/a')
    refresh_button.click()
    time.sleep(120)
    
    excel_button = driver.find_element(By.XPATH, '//*[@id="GridVenda_wrapper"]/div[1]/button[2]')
    driver.execute_script("arguments[0].click();", excel_button)
    time.sleep(120)
    
    driver.quit()

    return "Download concluído com sucesso"
    # Chromedriver_automation module

