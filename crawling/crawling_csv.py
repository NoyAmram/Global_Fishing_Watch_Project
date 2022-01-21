from selenium import webdriver
import time
import glob
import pandas as pd
import os

WEB_SCRAPPING_FOLDER = '/app/crawling/webscrapping'


def set_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {"download.default_directory": WEB_SCRAPPING_FOLDER}
    chrome_options.add_experimental_option("prefs", prefs)

    return chrome_options


def get_url(search_url):
    driver.get(search_url)
    time.sleep(2)


def login_to_site(user_name, user_password):
    search_box = driver.find_element_by_xpath('//*[@id="email"]')
    search_box.send_keys(user_name)
    search_box = driver.find_element_by_xpath('//*[@id="password"]')
    search_box.send_keys(user_password)
    search_box.submit()
    time.sleep(5)


def download_csv(xpath):
    csv_file_button = driver.find_element_by_xpath(xpath)
    csv_file_button.click()


def download_wait(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds


def one_csv(path, file_output_path='/app/fixtures/full_raw_data.csv'):
    all_files = glob.glob(path + "/*.csv")
    files_list = []
    for filename in all_files:
        df_all = pd.read_csv(filename, index_col=None, header=0)
        files_list.append(df_all)
    frame = pd.concat(files_list, axis=0, ignore_index=True)
    frame.to_csv(file_output_path, index=False)


if __name__ == '__main__':

    chrome_set_options = set_chrome_options()
    driver = webdriver.Chrome(options=chrome_set_options)
    get_url("https://globalfishingwatch.org/data-download/datasets/public-training-data-v1")
    print("Login to site")
    login_to_site(user_name='noy.amram@gmail.com', user_password='Israel2020')
    print("Start downloading")
    download_csv(xpath='//*[@id="root"]/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[1]/div[2]/button')
    download_csv(xpath='//*[@id="root"]/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/button')
    download_csv(xpath='//*[@id="root"]/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[3]/div[2]/button')
    download_csv(xpath='//*[@id="root"]/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[4]/div[2]/button')
    download_csv(xpath='//*[@id="root"]/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[5]/div[2]/button')
    download_csv(xpath='//*[@id="root"]/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[6]/div[2]/button')
    download_csv(xpath='//*[@id="root"]/div[2]/div/div/div[2]/div/div/div[1]/div[3]/div/div[7]/div[2]/button')
    print("Waiting for downloads to finish")
    download_wait(directory=WEB_SCRAPPING_FOLDER, timeout=600, nfiles=7)
    driver.close()
    print("Unifying CSV(s)")
    one_csv(path=WEB_SCRAPPING_FOLDER)
    print("Done")
