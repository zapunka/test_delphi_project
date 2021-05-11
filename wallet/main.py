from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from python3_anticaptcha import CustomResultHandler
import random
import platform
import json
import time
import wallet.config as conf


def main():
    # При каждой итерации меняем USERAGENT
    U_A_File = open('useragent.txt')
    U_A_File = U_A_File.readlines()
    for line in U_A_File:
        # anti-captcha plugin
        options = webdriver.ChromeOptions()
        options.add_extension('../wallet/anticaptcha-plugin_v0.54.zip')

        driver = webdriver.Chrome('../wallet/drivers/chromedriver')
        if platform.system() == 'Linux':
            driver = webdriver.Chrome("../wallet/drivers/chromedriver_linux", options=options)
        actions = ActionChains(driver)

        # Рандомно изменяем размер запускаемого окна
        # sx = random.randint(1000, 1500)
        # sn = random.randint(3000, 4500)
        # driver.set_window_size(sx, sn)
        #  END Рандомно изменяем размер запускаемого окна

        driver.get("https://play.alienworlds.io/")
        time.sleep(20)
        actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0, 0).move_by_offset(0, 160).click().perform()
        time.sleep(10)
        driver.switch_to.window(driver.window_handles[-2])
        time.sleep(5)

        # Получаем элементы ввода данных через XPATH
        login_input_path = '//*[@id="root"]/div/div/div[2]/div[5]/div/div/div/div[1]/div[1]/input'
        driver.find_element_by_xpath(login_input_path).send_keys(conf.TEST_LOGIN)
        pass_input_path = '//*[@id="root"]/div/div/div[2]/div[5]/div/div/div/div[1]/div[2]/input'
        driver.find_element_by_xpath(pass_input_path).send_keys(conf.TEST_PASSWORD)
        # Ожидание разгадывания капчи
        WebDriverWait(driver, 120).until(lambda x: x.find_element_by_css_selector('.antigate_solver.solved'))
        driver.find_element_by_css_selector('input[type=submit]').click()

        # driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div[5]/div/div/div/div[4]/div/div/div/div/div/div/iframe').click()
        # driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div[5]/div/div/div/div[5]/button[1]').click()
        # END Получаем элементы ввода данных через XPATH
        # АНТИКАПЧА
        # custom_result = CustomResultHandler.CustomResultHandler(anticaptcha_key=ANTICAPTCHA_KEY)
        # user_answer = custom_result.task_handler(task_id=TASK_ID)
        # print(user_answer)


        driver.close()


def acp_api_send_request(driver, message_type, data={}):
    message = {
        # this receiver has to be always set as antiCaptchaPlugin
        'receiver': 'antiCaptchaPlugin',
        # request type, for example setOptions
        'type': message_type,
        # merge with additional data
        **data
    }
    # run JS code in the web page context
    # preceicely we send a standard window.postMessage method
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))


main()

