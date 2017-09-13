#!/usr/bin/env python

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Login page for Waterloo Quest
LOGIN_URL = 'https://quest.pecs.uwaterloo.ca/psp/SS/?cmd=login&languageCd=ENG'

# The Quest app is inside an iframe with this ID
QUEST_IFRAME_ID = 'ptifrmtgtframe'

# Name of the input box that accepts a class number for enrollment
CLASS_NUM_INPUT = 'DERIVED_REGFRM1_CLASS_NBR'

# Xpath that only exists when adding a class has failed. This is a hacky way to check for
# failure, but Quest doesn't make it easy
FAILURE_XPATH = '//*[@id="win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0"]/div/img[@alt="Error"]'

def login_quest(username, password):
  '''Logs into waterloo Quest are returns the webdriver instance of the logged in session'''
  browser = webdriver.Chrome()
  browser.get(LOGIN_URL)
  assert 'Quest Home' in browser.title
  browser.find_element_by_name('userid').send_keys(username)
  browser.find_element_by_name('pwd').send_keys(password + Keys.RETURN)
  assert 'Quest' == browser.title
  return browser

def handle_new_state(browser):
  '''
  Because Quest is a single page web app, Selenium has trouble determining when a
  new 'state' of the app is finished loading. It runs into trouble when it tries to
  click something too quickly, hence the time.sleep.
  The Quest app is inside an iframe which is re-inserted into the DOM after every
  state change. After a change, the webdriver must switch to the new iframe.
  '''
  browser.switch_to.default_content()
  browser.switch_to.frame(QUEST_IFRAME_ID)
  time.sleep(0.5)

def click_link(browser, text, partial=False):
  handle_new_state(browser)
  if partial:
    browser.find_element_by_partial_link_text(text).click()
  else:
    browser.find_element_by_link_text(text).click()

def empty_cart(browser):
  '''
  Empty the user's shopping cart of classes. Assumes one is already on
  the correct page. The implementation of this function is extremely hacky,
  don't look at it. (The webdriver searches for the trashcan img used by quest, and
  clicks it.)
  '''
  time.sleep(0.5)
  try:
    browser.find_element_by_xpath('//img[@alt="Delete"]').click()
    empty_cart(browser)
  except NoSuchElementException:
    return

def add_class(quest_username, quest_password, class_num):
  '''
  Attempts to enroll a user specified by the given credentials into the given class.
  Returns true when it succeeds at enrolling the the class, false otherwise
  '''
  browser = login_quest(quest_username, quest_password)
  success = False
  try:
    click_link(browser, 'Enroll')
    click_link(browser, 'add')
    empty_cart(browser)

    handle_new_state(browser)
    browser.find_element_by_name(CLASS_NUM_INPUT).send_keys(class_num)
    browser.find_element_by_link_text('enter').click()

    click_link(browser, 'Next')
    click_link(browser, 'Next')
    click_link(browser, 'Proceed', True)
    click_link(browser, 'Finish', True)
    click_link(browser, 'my class schedule')
    handle_new_state(browser)
    css = 'span[id^="DERIVED_CLS_DTL_CLASS_NBR"]'
    for tag in browser.find_elements_by_css_selector(css):
      if str(class_num) == tag.text:
        success = True
  except Exception as e:
    print e
  finally:
    browser.quit()
  return success
