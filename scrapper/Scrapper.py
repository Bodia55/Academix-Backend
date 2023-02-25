import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup, NavigableString

class Scrapper:
    def __init__(self, username, password):
        self.schedule_url = 'https://student.guc.edu.eg/Web/Student/Schedule/GroupSchedule.aspx'
        self.courses_url = 'https://cms.guc.edu.eg/apps/student/HomePageStn.aspx'
        self.username = username
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

    # prints the week's schedule as a 2d array with the index being the day, with starting index 0 for saturday
    def get_week_schedule_printer(self):
        week_schedule = []
        for i in range(0, 6):
            week_schedule.append(self.get_day_schedule_formatted_data(i))
        print(week_schedule)
    
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
            return
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', id='ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewcourses')
            course_rows = table.findChildren('tr', recursive=False)
            course_rows.pop(0)
            for course in course_rows:
                course_name = course.findChildren('td', recursive=False)[1].text
                courses.append(course_name)
            return courses
