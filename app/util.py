from selenium import webdriver


def get_chrome_driver_with_options(*args):
    options = webdriver.ChromeOptions()
    for arg in args:
        options.add_argument(arg)

    return webdriver.Chrome("C:\\Users\\gemi\\Downloads\\chromedriver.exe", chrome_options=options)
