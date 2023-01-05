from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import csv 

driver = webdriver.Chrome('../chromedriver.exe', options=webdriver.ChromeOptions())
driver.maximize_window()

def amazon():
    driver.get("https://www.amazon.com/")
    time.sleep(5)

def login(usr, pswd):
    amazon()

    if driver.find_element(By.XPATH, '//*[@id="nav-link-accountList-nav-line-1"]').get_attribute('innerHTML') == 'Hello, sign in':
        driver.find_element(By.XPATH, '//*[@id="nav-link-accountList"]').click()
        time.sleep(5)

        driver.find_element(By.XPATH, '//*[@id="ap_email"]').send_keys(usr)
        time.sleep(5)

        driver.find_element(By.XPATH, '//*[@id="continue"]').click()
        time.sleep(5)

        driver.find_element(By.XPATH, '//*[@id="ap_password"]').send_keys(pswd)
        time.sleep(3)

        driver.find_element(By.XPATH, '//*[@id="authportal-main-section"]/div[2]/div[1]/div/div/form/div/div[2]/div/div/label/div/label/input').click()
        time.sleep(3)

        driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()
        time.sleep(10)


def check_cart():
    login(usr, pswd)
    driver.find_element(By.XPATH, '//*[@id="nav-cart"]').click()


def add2cart(prod):
    login(usr, pswd)
    amazon()

    driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]').send_keys(str(prod))
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]').click()
    time.sleep(7)

    for i in range(1, 10):
        try:
            driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div['+ str(i) +']/div/div/div/div/div/div/div[1]/span/a/div').click()
            time.sleep(5)

            driver.find_element(By.XPATH, '//*[@id="submit.add-to-cart"]').click()
            time.sleep(5)

            driver.get("https://www.amazon.com/s?k="+str("+".join(prod.split())))
            time.sleep(5)
        
        except Exception as e:
            print("Exception: ", e)
            pass


def your_profile():
    driver.find_element(By.XPATH, '//*[@id="nav-link-accountList"]').click()
    time.sleep(5)


def your_orders():
    your_profile()
    driver.find_element(By.XPATH, '//*[@id="a-page"]/div[2]/div/div[2]/div[1]/a/div/div').click()
    time.sleep(5)


def your_list():
    your_profile()
    driver.find_element(By.XPATH, '//*[@id="a-page"]/div[2]/div/div[5]/div[1]/a/div/div').click()
    time.sleep(5)


def web_scrap(scrapp):
    amazon()
    login(usr, pswd)

    driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]').send_keys(str(scrapp))
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]').click()
    time.sleep(5)
    # web scraping of products
    scrap = []
    count = 2
    page = 1

    while page < 5:
        if count > 12:
            page += 1
            count = 2

        url = "https://www.amazon.com/s?k="+ str("+".join(scrapp.split())) +"&page="+str(page)
        driver.get(url)
        time.sleep(5)

        try:
            title = driver.find_element("xpath", '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div['+ str(count) +']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')
            title_text = title.get_attribute("innerHTML")
            title.click()
            time.sleep(5)
        except:
            title = driver.find_element("xpath", '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div['+ str(count+2) +']/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span')
            title_text = title.get_attribute("innerHTML")
            title.click()
            time.sleep(5)

        try:
            try:
                prize = driver.find_element("xpath", '//*[@id="corePrice_desktop"]/div/table/tbody/tr[2]/td[2]/span[1]/span')
                prize_text = prize.get_attribute("innerHTML").splitlines()[0]
                time.sleep(5)
            except:
                prize = driver.find_element("xpath", '//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span')
                prize_text = prize.get_attribute("innerHTML")
                time.sleep(5)
        except:
            prize_text = 'NA'

        scrap.append([title_text, prize_text])
        
        driver.get(url)
        driver.set_page_load_timeout(12)
        time.sleep(5)

        count += 1

    return scrap


if __name__ == "__main__":
    try:
        global usr, pswd, prod, scrapp
        usr = input("Enter your Amazon Email/Phone Number:\n")
        pswd = input("Enter your password:\n")

        prod = input("Enter the product you want to add in cart:\n")

        scrapp = input("Enter the product details you want to scrap for details with prize:\n")

        amazon()
        login(usr, pswd)
        your_profile()
        your_orders()
        your_list()
        check_cart()
        add2cart(prod)
        check_cart()

        with open('amazon.csv', 'w', newline='', encoding='utf-8') as csvfile:
            data = csv.writer(csvfile, delimiter=" ")
            for prod in web_scrap(scrapp):
                data.writerow(["Title:", prod[0]])
                data.writerow(["Prize:", prod[1]])
                data.writerow([])

    except Exception as e:
        print("Exception: ", e)