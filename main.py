from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd
from optimiser2 import *

# Ask user for major course code and units completed so far

course_code = ''
valid_course = False
while valid_course is False:
    course_code = input("Please enter the course code for your major (it should have the structure "
                        "MJD-PHYSC): ")
    if len(course_code) != 9:
        print("Invalid course code entered.")
    else:
        valid_course = True

completed_units = ''
valid_unit = False
while valid_unit is False:
    completed_units = input("Please enter the units you've completed so far, separating them "
                            "with a comma (if none hit enter): ")
    completed_units = completed_units.upper()
    completed_units = completed_units.split(',')
    for x in completed_units:
        if len(x) != 8 and completed_units != ['']:
            print("Invalid unit entered.")
            valid_unit = False
        else:
            valid_unit = True

# Format url using the course code entered

course_url = "https://handbooks.uwa.edu.au/majordetails?code=" + course_code + "#dsmlevel1"

req = Request(
    url=course_url,
    headers={'User-Agent': 'Mozilla/5.0'}
)

# Scrape the webpage

webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')
table_rows = soup.find_all('tr')
paragraphs = soup.find_all('p')

count = 1

del table_rows[0]

unit_list = []

# Scrape relevant info

for i in table_rows:
    count+=1
    availability_item = str(i.contents[1])
    availability = re.findall("[A-Z][0-9]", availability_item)
    unit_code_item = str(i.contents[3])
    unit_code_list = re.findall("[A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]", unit_code_item)
    if unit_code_list == []:
        continue
    else:
        unit_code = unit_code_list[0]
    unit_details_full = i.contents[7].find_all('dd')
    unit_details = unit_details_full[0]
    prereq_list = []
    for x in unit_details:
        stringx = str(x)
        prereq_items = re.findall("[A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]", stringx)
        try:
            prereq = prereq_items[0]
            if 'X' not in prereq:
                prereq_list.append(prereq)
        except:
            continue
    unit_tup = (unit_code, availability, prereq_list)
    unit_list.append(unit_tup)

completed_units = ["CHEM1003", "MATH1721", "PHYS1030", "MATH1720", "MATH1722", "CITS1001", "CITS5505"
                   "PPHE2211", "PPHE3327", "CITS1002", "PHIL1007", "CITS3004", "SCIE2100", "CITS2401"]

updated_unit_list = []
for units in unit_list:
    if units[0] not in completed_units:
        updated_unit_list.append(units)

df = pd.DataFrame.from_records(updated_unit_list, columns=['Unit', 'Availability', 'Prerequisites'])

opto(updated_unit_list, completed_units, 2, 2023, 4)

