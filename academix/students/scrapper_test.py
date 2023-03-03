
# write tests for the scrapper here

from scrapper import Scrapper

scrapper = Scrapper('<username>', '<password>')

print(scrapper.get_gpa_please('2022-2023'))