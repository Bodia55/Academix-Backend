# write tests for the scrapper here

from scrapper import Scrapper

scrapper = Scrapper('<username>', '<password>')

print(scrapper.get_gpa('2022-2023'))