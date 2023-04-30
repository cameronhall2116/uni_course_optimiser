import pandas as pd
import re

class Unit:
    def __init__(self, code, availability, prerequisites):
        self.code = code
        self.availability = availability
        self.prerequisites = prerequisites


def opto(units, completed_units, sem, year, courseYears):
    semCode = "S" + str(sem)
    startingSem = str(year) + " S" + str(sem)
    semList = [semCode]
    semYearList = [startingSem]
    course = {startingSem: ["MATH1722"]}

    for x in range(courseYears*2):
        if sem == 2:
            year+=1
            sem=1
            semester = str(year) + " S" + str(sem)
            semList.append("S" + str(sem))
            semYearList.append(semester)
            course[semester] = []
        elif sem == 1:
            sem=2
            semester = str(year) + " S" + str(sem)
            semList.append("S" + str(sem))
            semYearList.append(semester)
            course[semester] = []

    for i in units:
        unit = Unit(i[0], i[1], i[2])
        code = unit.code
        check = all(items in completed_units for items in unit.prerequisites)
        x = 0
        while x < (courseYears * 2)-1:
            semCode = semYearList[x][len(semYearList[x])-1]
            check2 = set(unit.prerequisites).isdisjoint(course[semYearList[x]])
            if (check is True) and (check2 is True) and len(course[semYearList[x]]) < 4 \
                and (semCode in str(unit.availability)) and (code not in completed_units):
                #print("Adding to dict...")
                course[semYearList[x]].append(code)
                completed_units.append(code)
            x+=1

    df = pd.DataFrame.from_dict(course, orient="index")
    df.transpose()
    print(df)



