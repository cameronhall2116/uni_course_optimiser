import pandas as pd

class Unit:
    def __init__(self, code, availability, prerequisites):
        self.code = code
        self.availability = availability
        self.prerequisites = prerequisites


def opto(units, completed_units, sem, year, courseYears):
    #format and initialise variables
    semCode = "S" + str(sem)
    startingSem = str(year) + " S" + str(sem)
    semList = [semCode]
    semYearList = [startingSem]
    course = {startingSem: ["MATH1722"]}

    temp_set = set()

    # add all semesters to dictionary
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

    # this loop iterates through every unit and tries to add to dictionary
    i = 0
    while i < len(units):
        unit = Unit(units[i][0], units[i][1], units[i][2])
        code = unit.code
        check = all(items in completed_units for items in unit.prerequisites)
        x = 0
        y = 0

        # this checks if any units that previously couldn't be added due to lacking prerequisites
        # can now be added
        if len(temp_set) > 0:
            temp_code = list(temp_set)[0]
            while y < (courseYears * 2):
                semCode = semYearList[y][len(semYearList[y]) - 1]
                check2 = set(unit.prerequisites).isdisjoint(course[semYearList[y]])
                if (check is True) and (check2 is True) and len(course[semYearList[y]]) < 4 \
                        and (semCode in str(unit.availability)) and (temp_code not in completed_units):
                    course[semYearList[y]].append(temp_code)
                    completed_units.append(temp_code)
                    temp_set.remove(temp_code)
                    break
                y += 1

        # this is the main loop for adding units to dictionary
        while x < (courseYears * 2):
            semCode = semYearList[x][len(semYearList[x])-1]
            check2 = set(unit.prerequisites).isdisjoint(course[semYearList[x]])
            if (check is True) and (check2 is True) and len(course[semYearList[x]]) < 4 \
                and (semCode in str(unit.availability)) and (code not in completed_units):
                course[semYearList[x]].append(code)
                completed_units.append(code)
                break
            x += 1
        if code not in completed_units:
            temp_set.add(code)
        i += 1

    # print the results in a pandas dataframe
    df = pd.DataFrame.from_dict(course, orient="index")
    df.transpose()
    print(df)



