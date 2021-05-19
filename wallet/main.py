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
    options = webdriver.ChromeOptions()
    options.add_extension('../wallet/anticaptcha-plugin_v0.54.crx')
    options.add_argument("user-agent={}".format(get_random_user_agent()))

    driver = webdriver.Chrome(executable_path='../wallet/drivers/chromedriver', options=options)
    if platform.system() == 'Linux':
        driver = webdriver.Chrome(executable_path="../wallet/drivers/chromedriver_linux", options=options)
    actions = ActionChains(driver)

    # Рандомно изменяем размер запускаемого окна
    # sx = random.randint(1000, 1500)
    # sn = random.randint(3000, 4500)
    # driver.set_window_size(sx, sn)
    #  END Рандомно изменяем размер запускаемого окна

    driver.get("https://play.alienworlds.io/")
    time.sleep(40)
    # WebDriverWait(driver, 120).until(lambda x: x.find_element_by_css_selector('.webgl-content'))
    try:
        actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0, 0).move_by_offset(0, 160).click().perform()
        time.sleep(10)
        driver.switch_to.window(driver.window_handles[-2])
        time.sleep(5)
    except IndexError:
        print('Не смогли выбрать окно (возможно, не дождались его открытия)')
        driver.close()

    # Получаем элементы ввода данных через XPATH
    login_input_path = '//*[@id="root"]/div/div/div[2]/div[5]/div/div/div/div[1]/div[1]/input'
    driver.find_element_by_xpath(login_input_path).send_keys(conf.TEST_LOGIN)
    pass_input_path = '//*[@id="root"]/div/div/div[2]/div[5]/div/div/div/div[1]/div[2]/input'
    driver.find_element_by_xpath(pass_input_path).send_keys(conf.TEST_PASSWORD)
    # Ожидание разгадывания капчи
    WebDriverWait(driver, 120).until(lambda x: x.find_element_by_css_selector('.antigate_solver.solved'))
    driver.find_element_by_css_selector('input[type=submit]').click()

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
    return driver.execute_script("""return window.postMessage({});""".format(json.dumps(message)))


def captcha_solver():
    options = webdriver.ChromeOptions()
    options.add_extension('../wallet/anticaptcha-plugin_v0.54.crx')

    browser = webdriver.Chrome(executable_path='../wallet/drivers/chromedriver', options=options)
    acp_api_send_request(
        browser,
        'setOptions',
        {'options': {'antiCaptchaApiKey': conf.ANTICAPTCHA_KEY}}
    )
    # 3 seconds pause
    time.sleep(3)

    # Go to the test form with reCAPTCHA 2
    browser.get('https://antcpt.com/rus/information/demo-form/recaptcha-2.html')

    # Test input
    browser.find_element_by_name('demo_text').send_keys('Test input')

    # Most important part: we wait upto 120 seconds until the AntiCaptcha plugin indicator with antigate_solver class
    # gets the solved class, which means that the captcha was successfully solved
    WebDriverWait(browser, 120).until(lambda x: x.find_element_by_css_selector('.antigate_solver.solved'))

    # Sending form
    browser.find_element_by_css_selector('input[type=submit]').click()


def get_random_user_agent():
    rand = random.randint(0, len(conf.USER_AGENTS)-1)
    return conf.USER_AGENTS[rand]


main()
# captcha_solver()
