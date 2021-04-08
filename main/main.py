#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time
import csv
import sys

def get_username_password():
    result = []

    try:
      # read username and password for Login
      with open ("files/username_password.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter= ",")

        # ignore header
        next(csv_reader)

        # Login data    
        for row in csv_reader:
            username = row[0]
            password = row[1]

        # append Login data to list
        result.append(username)
        result.append(password)

        # return list with username and passwort
        return result

    except:
        print("\nException with username and passwort")
        return

# get input of user
def get_selected_course(driver):

    try:
        input = sys.argv[1]
    except IndexError:
        print("argument for shortform missing")
        print("try again")
        driver.close()
        quit()


    with open("files/courses.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)

        # ignore header
        next(csv_reader)

        # if short term of course listed in csv, return title of course
        for row in csv_reader:
            if input == row[1]:
                return row[0]
        
        # else exit and close webdriver
        print("course not listed")
        driver.close()
        quit()

# log into chosen course
def get_course(driver, course_name):
    get_course_card_view(driver, course_name)

# course format as cards    
def get_course_card_view(driver, course_name):
    try:
        # list of given course titles - card overview
        course_title_card = WebDriverWait(driver, 4).until(ec.visibility_of_all_elements_located((By.CLASS_NAME, 'multiline')))

        # search for corsesponding course name - card overview
        for title in course_title_card:
            # if true open course
            if title.text == course_name:
                title.click() 
                return True

    # if courses not in 'card overview' format, check for list format
    except TimeoutException:    
        get_course_list_view(driver, course_name)

        return False

# course format as list
def get_course_list_view(driver, course_name):
    try:
        # list of given course titles - list
        course_title_list = WebDriverWait(driver, 2).until(ec.visibility_of_element_located((By.PARTIAL_LINK_TEXT, course_name)))
        course_title_list.click()

        return True 

    # if courses not in 'list overview' format, check for summary format
    except TimeoutException:
        get_course_summary_view(driver, course_name)

        return False

# course format summarized
def get_course_summary_view(driver, course_name):
    try:
        # list of given course titles - summary
        course_title_summary = WebDriverWait(driver,2).until(ec.visibility_of_element_located((By.PARTIAL_LINK_TEXT, course_name)))
        course_title_summary.click()
        
        return True 
    
    except TimeoutException:
        print("view for courses does not exist")
        driver.close()
        return False

def main():

    login_data = get_username_password()

    username   = login_data[0]
    password   = login_data[1]

    # Firefox webdriver
    driver = webdriver.Firefox()

    # Full screen
    driver.maximize_window()

    # wait for 15 seconds until Error is thrown 
    # ensures that no error is thrown when page is not loaded yet
    driver.set_page_load_timeout(15)

    # name for selected course
    course_name = get_selected_course(driver)

    # open website
    driver.get("https://moodle.hs-bochum.de")

    # insert login data
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)

    # enter login
    driver.find_element_by_class_name("button").click()

    # wait
    time.sleep(1.5)

    # show page for chosen course 
    get_course(driver, course_name)
  

if __name__ == "__main__":
    main()   
        