import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mechanicalsoup

class Scrapper:
    def __init__(self, username, password):
        self.schedule_url = 'https://student.guc.edu.eg/Web/Student/Schedule/GroupSchedule.aspx'
        self.courses_url = 'https://cms.guc.edu.eg/apps/student/HomePageStn.aspx'
        self.username = username+"@student.guc.edu.eg"
        self.password = password

    # converts(returns) the index of the day given the day's name
    def get_day_index(self, day_name: str):
        day_name = day_name.lower()
        index = -1
        if day_name == 'saturday':
            index = 0
        elif day_name == 'sunday':
            index = 1
        elif day_name == 'monday':
            index = 2
        elif day_name == 'tuesday':
            index = 3
        elif day_name == 'wednesday':
            index = 4
        elif day_name == 'thursday':
            index = 5
        return index

    # scrappes the website for the day's schedule
    def get_day_schedule_data(self, day_index: int):
        day_schedule = []
        r = requests.get(self.schedule_url, auth=HttpNtlmAuth(self.username, self.password))
        if r.status_code != 200:
            print("An Error Occurred. Check Credentials And Try Again.")
            return
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            table: NavigableString = soup.find("table", id="scdTbl")
            children = table.findChildren("tr", recursive=False)
            children.pop(0)
            day = children[day_index]
            day_sessions = day.findChildren("td", recursive=False)
            for slot in day_sessions:
                tables = slot.findChildren("table", recursive=False)
                if len(tables) == 0:
                    continue
                elif len(tables) == 1: #its a tutorial
                    tut_infos = tables[0].findChildren("td", recursive=True)
                    day_schedule.append(tut_infos[2].text + " " + tut_infos[1].text)
                elif len(tables) > 1:
                    table = tables[1]
                    data = table.find("span")
                    day_schedule.append(data.text)
            return day_schedule
        
    # Get ID and Full name    
    def get_idname(self):
        r = requests.get(self.schedule_url, auth=HttpNtlmAuth(self.username, self.password))
        if r.status_code != 200:
            print("An Error Occurred. Check Credentials And Try Again.")
            return ["",""], False
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            span = soup.find("span",id="scdTpLbl")
            result = span.text.split(" - ")

            ## Returns ID and Full Name 
            return result, True

    # Get ID and Full name    
    def get_gpa_please(self, year):
        transcriptUrl = "https://student.guc.edu.eg/external/student/grade/Transcript.aspx"

        # Create a browser object with MechanicalSoup
        browser = mechanicalsoup.StatefulBrowser()

        # Set the authentication credentials
        browser.session.auth = HttpNtlmAuth(self.username, self.password)

        # Navigate to the web page
        res = browser.open(transcriptUrl)
        if res.status_code != 200:
            print("An Error Occurred. Check Credentials And Try Again.")
            return "", False
        else:
            # Get the option value from its text 
            option_value =  browser.page.find("option", string=year)['value']

            # Submit the form
            form = browser.select_form('form')
            form.set_select({'stdYrLst': option_value})
            res = browser.submit_selected()
            if res.status_code != 200:
                print("An Error Occurred. Check Credentials And Try Again. SC: ", res.status_code)
                return "", False
            else:
                # Extract the information you need from the resulting page
                return browser.page.find("span",id="cmGpaLbl").text, True


    # prints the week's schedule as a 2d array with the index being the day, with starting index 0 for saturday
    def get_week_schedule_printer(self):
        week_schedule = []
        for i in range(0, 6):
            week_schedule.append(self.get_day_schedule_formatted_data(i))
        print(week_schedule)

    # returns the week schedule data
    def get_week_schedule_data(self):
        week_schedule = []
        for i in range(0, 6):
            week_schedule.append(self.get_day_schedule_formatted_data(i))
        return week_schedule
    
    
    # returns a list representing the day's schedule
    def get_day_schedule_formatted_data(self, day_index: int):
        schedule = self.get_day_schedule_data(day_index)
        formatted_schedule = []
        for item in schedule:
            formatted_schedule.append(item.replace("\r\n\t\t\t\t\t\t\t\t\t\t\t\tTut\r\n\t\t\t\t\t\t\t\t\t\t\t\n", " Tut").replace("\r\n\t\t\t\t\t\t\t\t\t\t\t\tLab\r\n\t\t\t\t\t\t\t\t\t\t\t\n", " Lab"))
        return formatted_schedule

    # prints a list representing the day's schedule
    def get_day_schedule_formatted_printer(self, day_index: int):
        schedule = self.get_day_schedule_data(day_index)
        formatted_schedule = []
        for item in schedule:
            formatted_schedule.append(item.replace("\r\n\t\t\t\t\t\t\t\t\t\t\t\tTut\r\n\t\t\t\t\t\t\t\t\t\t\t\n", " Tut").replace("\r\n\t\t\t\t\t\t\t\t\t\t\t\tLab\r\n\t\t\t\t\t\t\t\t\t\t\t\n", " Lab"))
        print(formatted_schedule)

    # returns the courses as a list
    def get_courses_data(self):
        courses = []
        r = requests.get(self.courses_url, auth=HttpNtlmAuth(self.username, self.password))
        if r.status_code != 200:
            print("An Error Occurred. Check Credentials And Try Again.")
            return [], False
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', id='ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses')
            course_rows = table.findChildren('tr', recursive=False)
            course_rows.pop(0)
            for course in course_rows:
                course_name = course.findChildren('td', recursive=False)[1].text
                courses.append(course_name)
            return courses, True
        
    # get available years
    def get_available_years(self):
        available_years = []
        url = f'https://{self.username}:{self.password}@student.guc.edu.eg/external/student/grade/Transcript.aspx'
        try:
            chromedriver_autoinstaller.install()
            options = chromeOptions()
            options.headless = True
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--window-size=1920,1200')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            select_dropdown = driver.find_element(By.ID, 'stdYrLst')
            options = select_dropdown.find_elements(By.TAG_NAME, 'option')
            options.pop(0)
            for option in options:
                available_years.append(option.text)
            return available_years  
        except:
            geckodriver_autoinstaller.install()
            options = firefoxOptions()
            options.headless = True
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--window-size=1920,1200')
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            select_dropdown = driver.find_element(By.ID, 'stdYrLst')
            options = select_dropdown.find_elements(By.TAG_NAME, 'option')
            options.pop(0)
            for option in options:
                available_years.append(option.text)
            return available_years
        
    
    # gets the selected dropdown option value
    def get_selected_year_value(self, year):
        available_years = self.get_available_years()
        for i in range(1, len(available_years)):
            if available_years[i] == year:
                return i+1
        return -1

    # get your gpa for a specific year
    def get_gpa(self, uni_year):
        uni_year_value = self.get_selected_year_value(uni_year)
        url = f'https://{self.username}:{self.password}@student.guc.edu.eg/external/student/grade/Transcript.aspx'
        try:
            chromedriver_autoinstaller.install()
            options = chromeOptions()
            options.headless = True
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--window-size=1920,1200')
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except:
                return "", False
            drop_down_select = driver.find_element(By.ID, 'stdYrLst')
            option = drop_down_select.find_element(By.CSS_SELECTOR, f'option[value="{uni_year_value}"]')
            option.click()
            try:
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'Table4'))
                )
                rows = table.find_elements(By.TAG_NAME, 'tr')
                gpa_row = rows[len(rows)-1]
                gpa = gpa_row.find_element(By.TAG_NAME, 'span')
                return gpa.text, True
            except:
                return "", False
        except:
            geckodriver_autoinstaller.install()
            options = firefoxOptions()
            options.headless = True
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--window-size=1920,1200')
            driver = webdriver.Firefox(options=options)
            try:
                driver.get(url)
            except:
                return "", False
            drop_down_select = driver.find_element(By.ID, 'stdYrLst')
            option = drop_down_select.find_element(By.CSS_SELECTOR, f'option[value="{uni_year_value}"]')
            option.click()
            try:
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'Table4'))
                )
                rows = table.find_elements(By.TAG_NAME, 'tr')
                gpa_row = rows[len(rows)-1]
                gpa = gpa_row.find_element(By.TAG_NAME, 'span')
                return gpa.text, True
            except:
                return "", False
   
        
