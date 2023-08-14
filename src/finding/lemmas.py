# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import quote
from os import path
from pathlib import Path
import os
import pandas as pd
from numpy.core.numeric import nan
import re
import logging

'''
Created on 21 jul. 2023

@author: jose-lopez

'''


def install_browser():

    print(f'Checking Google Chrome installation....' + "\n")

    with os.popen("google-chrome --version") as f:
        browser = f.readlines()

    if len(browser):

        print(f'Google Chrome version: {browser[0]}' + "\n")

    else:

        print(f'... Installing Google Chrome' + "\n")

        try:

            print(os.popen('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb').read())
            print(os.popen('apt install ./google-chrome-stable_current_amd64.deb').read())

        except Exception as e:

            print("An exception was raised whilst the installation of google-chrome was going on.")
            print(e)

            exit(1)


def get_browser():

    options = webdriver.ChromeOptions()

    options.add_argument('--no-sandbox')

    options.add_argument('--disable-dev-shm-usage')

    options.add_argument("--headless=new")

    options.add_argument("--disable-web-security")

    options.add_argument("--disable-extensions")

    options.add_argument("--disable-notifications")

    options.add_argument("--ignore-certificate-errors")

    options.add_argument("--allow-running-insecure-content")

    options.add_argument("--no-default-browser-check")

    options.add_argument("--no-first-run")

    options.add_argument("--no-proxy-server")

    options.add_argument("--disable-blink-features=AutomationController")

    try:

        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    except Exception as e:

        print("An exception was raised whilst Selenium's webdriver was trying to open google-chrome.")
        print(e)

        exit(1)

    return browser


def get_lemma(browser, file, line, token, logger, logs):

    # url_base = "https://logeion.uchicago.edu/morpho/"

    # url = url_base + quote(token)

    url = 'https://logeion.uchicago.edu/morpho/%E1%BC%90%CE%BA%CE%B1%CE%BB%CE%BB%CF%89%CF%80%CE%AF%CE%B6%CE%BF%CE%BD%CF%84%CE%BF'

    browser.get(url)  # navigate to URL

    try:

        # Waiting for a totally deployed URL.

        WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "Short Definition"))

    except NoSuchElementException as e:

        lemma = nan

        print(f'Getting URL error: An exception of type NoSuchElementException in File: {file} at line: {line}, token {token}' + "\n")
        print(f'URL: {url}' + "\n")

        logs.write(f'Getting URL error: An exception of type NoSuchElementException in File: {file} at line: {line}, token {token}' + "\n")
        logs.write(f'URL: {url}' + "\n")
        logs.write(f'{logger.exception("Exception Occurred while code Execution: " + str(e))}' + "\n")

    except TimeoutException as e:

        lemma = nan

        print(f'Getting URL error: An exception of type TimeoutException in File: {file} at line: {line}, token {token}' + "\n")
        print(f'URL: {url}' + "\n")

        logs.write(f'Getting URL error: An exception of type TimeoutException in File: {file} at line: {line}, token {token}' + "\n")
        logs.write(f'URL: {url}' + "\n")
        logs.write(f'{logger.exception("Exception Occurred while code Execution: " + str(e))}' + "\n")

    except Exception as e:

        lemma = nan

        print(f'Getting URL error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
        print(f'URL: {url}' + "\n")

        print(f'Getting URL error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
        print(f'URL: {url}' + "\n")
        print(f'{logger.exception("Exception Occurred while code Execution: " + str(e))}' + "\n")

        logs.write(f'Getting URL error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
        logs.write(f'URL: {url}' + "\n")
        logs.write(f'{logger.exception("Exception Occurred while code Execution: " + str(e))}' + "\n")

    else:

        try:

            browser.find_element(By.XPATH, "//*[contains(text(), 'Could not find the search term')]")

            lemma = nan

        except NoSuchElementException:

            try:

                possible_lemma = browser.find_element(By.CSS_SELECTOR, 'a.ng-binding').text

            except NoSuchElementException as e:

                lemma = nan

                print(f'Getting scraping error: An exception of type NoSuchElementException in File: {file} at line: {line}, token {token}' + "\n")
                print(f'URL: {url}' + "\n")

                logs.write(f'Getting scraping error: An exception of type NoSuchElementException in File: {file} at line: {line}, token {token}' + "\n")
                logs.write(f'URL: {url}' + "\n")
                logs.write(f'{logger.exception("Exception Occurred while code Execution: " + str(e))}' + "\n")

            except Exception as e:

                lemma = nan

                print(f'Getting scraping error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
                print(f'URL: {url}' + "\n")

                logs.write(f'Getting scraping error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
                logs.write(f'URL: {url}' + "\n")
                logs.write(f'{logger.exception("Exception Occurred while code Execution: " + str(e))}' + "\n")

            else:

                invalid_lemma = re.search(r'[a-zA-Z0-9]+', possible_lemma)

                if invalid_lemma:

                    lemma = nan

                else:

                    lemma = possible_lemma

    finally:

        try:

            return lemma

        except Exception as e:

            print(f'Getting return lemma error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
            print(f'URL: {url}' + "\n")

            logs.write(f'Getting return lemma error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
            logs.write(f'URL: {url}' + "\n")
            logs.write(f'{logger.exception("Exception Occurred while code Execution: " + str(e))}' + "\n")

            logs.close()

            exit()


def check_token(token):

    warning = False

    invalid_token = re.search("[^\u1F00-\u1FFF\u0370-\u03FF\.',;·ʼ]", token)

    if invalid_token:

        warning = True

    return warning


if __name__ == '__main__':

    install_browser()

    folders = ['processed', 'warnings', 'logs']

    root = "./text/"
    corpus = root + "corpus"

    for folder in folders:
        _path = root + folder
        if not path.exists(_path):
            os.mkdir(_path)

    processed_files = 0

    browser = get_browser()

    files = [str(x) for x in Path(corpus).glob("**/*.csv")]

    files_to_process = len(files)

    warnings_in_file = []

    logger = logging.getLogger()

    for file in files:

        file_name = "/" + file.split("/")[-1]

        file_root_name = file_name.split(".")[0]

        processed_files += 1

        processed_file = root + folders[0] + file_root_name + "_processed.csv"

        new_lemmas_file = root + folders[0] + file_root_name + "_new_lemmas.csv"

        warnings_file = root + folders[1] + file_root_name + "_warnings" + ".csv"

        logs_file = root + folders[2] + file_root_name + "_logs" + ".csv"

        logs = open(
            logs_file, 'w', encoding="utf8")

        warnings_in_file = []

        new_lemmas_in_file = []

        input_df = pd.read_csv(file)

        print(f'Getting lemmas for {file} file: {processed_files} | {files_to_process}' + "\n")

        for x in input_df.index:

            token = input_df.loc[x, "token"]

            lemma = input_df.loc[x, "lemma"]

            warning = check_token(token)

            if warning:

                warnings_in_file.append([x, token])

            if lemma is nan:

                lemma = get_lemma(browser, file, x, token, logger, logs)

                print(f'Token {token}       lemma : {lemma}')

                new_lemmas_in_file.append([x, token, lemma])

                input_df.loc[x, "lemma"] = lemma

        input_df.to_csv(processed_file)

        # Building the warnings' file, if there are any, for the file on process.

        if len(warnings_in_file) != 0:

            print(f'Warnings found for {file} file. A report in {warnings_file}')

            warnings_df = pd.DataFrame(warnings_in_file, columns=['line', 'token'])

            warnings_df.to_csv(warnings_file)

        new_lemmas_in_file_df = pd.DataFrame(new_lemmas_in_file, columns=['line', 'token', 'lemma'])

        new_lemmas_in_file_df.to_csv(new_lemmas_file)

        logs.close()

    print(f'..... done')
