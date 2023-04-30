from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd
from optimiser import *
from optimiser2 import *

'''req = Request(
    url='https://handbooks.uwa.edu.au/majordetails?code=mjd-physc#dsmlevel1',
    headers={'User-Agent': 'Mozilla/5.0'}
)'''

req = Request(
    url='https://handbooks.uwa.edu.au/majordetails?code=MJD-ARIDM#dsmlevel1',
    headers={'User-Agent': 'Mozilla/5.0'}
)

webpage = urlopen(req).read()

# unit list = [{code: {availability: ,prerequisites}}]

unit_list = []

soup = BeautifulSoup(webpage, 'html.parser')
table_rows = soup.find_all('tr')
count = 1

del table_rows[0]

for i in table_rows:
    count+=1
    print(i)
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

completed_units = ["CHEM1003", "MATH1721", "PHYS1030", "MATH1720", "MATH1722", "CITS1001"]
updated_unit_list = []
for units in unit_list:
    if units[0] not in completed_units:
        updated_unit_list.append(units)


df = pd.DataFrame.from_records(updated_unit_list, columns=['Unit', 'Availability', 'Prerequisites'])

print(df)
#print(updated_unit_list)


#optimise(updated_unit_list, 'S2')
#optimise2(updated_unit_list)

opto(updated_unit_list, completed_units, 2, 2023, 4)

