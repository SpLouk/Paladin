#!/usr/bin/env python

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

LOGIN_URL = 'https://quest.pecs.uwaterloo.ca/psp/SS/?cmd=login&languageCd=ENG'

def login_quest(credentials_file):
  credentials = json.loads(open(credentials_file).read())
  browser = webdriver.Chrome()
  browser.get(LOGIN_URL)
  assert 'Quest Home' in browser.title
  username = browser.find_element_by_name('userid')
  pwd = browser.find_element_by_name('pwd')
  username.send_keys(credentials.get('username'))
  pwd.send_keys(credentials.get('password') + Keys.RETURN)
  assert 'Quest' == browser.title
  return browser

def click_link(browser, text, partial=False):
  time.sleep(0.5)
  browser.switch_to.default_content()
  browser.switch_to.frame('ptifrmtgtframe')
  if partial:
    browser.find_element_by_partial_link_text(text).click()
  else:
    browser.find_element_by_link_text(text).click()

def empty_cart(browser):
  time.sleep(0.5)
  try:
    browser.find_element_by_xpath('//img[@alt="Delete"]').click()
    empty_cart(browser)
  except NoSuchElementException:
    return

def add_class(credentials_file, class_num):
  browser = login_quest(credentials_file)
  click_link(browser, 'Enroll')
  click_link(browser, 'add')
  empty_cart(browser)

  browser.switch_to.default_content()
  browser.switch_to.frame('ptifrmtgtframe')
  browser.find_element_by_name('DERIVED_REGFRM1_CLASS_NBR').send_keys(class_num)
  browser.find_element_by_link_text('enter').click()

  click_link(browser, 'Next')
  click_link(browser, 'Next')
  click_link(browser, 'Proceed', True)
  click_link(browser, 'Finish', True)
  time.sleep(0.5)
  browser.switch_to.default_content()
  browser.switch_to.frame('ptifrmtgtframe')
  success = len(browser.find_elements_by_xpath('//*[@id="win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0"]/div/img[@alt="Error"]')) == 0
  browser.quit()
  return success
