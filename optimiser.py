from itertools import chain, repeat, count, islice
import itertools
from collections import Counter

class Unit:
    def __init__(self, code, availability, prerequisites):
        self.code = code
        self.availability = availability
        self.prerequisites = prerequisites

def optimise(frame, startingSem):
    units_per_sem = 4
    timespent = 0

    if startingSem == 'S2':
        otherSem = 'S1'
    elif startingSem == 'S1':
        otherSem = 'S2'
    else:
        return
    #goal is to fit all frame data in minimum timespent

    #combine data in all possible variation given set rules

    unitNum = len(frame)

    combos = itertools.product(frame, repeat=unitNum)
    updated_combos = []
    masterCounter = 0
    for combo in combos:
        if (combo[0][0] != "CITS1401"):
            break
        #print(masterCounter)
        masterCounter+=1
        if masterCounter == 10:
            break
        x = 0
        bad_combo = False
        #print("\nThis is the combo", combo)
        while x <= unitNum:
            #print("Checking accurate semester order...")
            try:
                if startingSem not in (combo[x][1] and combo[x+1][1] and combo[x+2][1] and combo[x+3][1]):
                    bad_combo = True
                    break
                if otherSem not in (combo[x+4][1] and combo[x+5][1] and combo[x+6][1] and combo[x+7][1]):
                    bad_combo = True
                    break
            except:
                break
            x += 8
        if bad_combo == True:
            #print("BREAKING FOR SEMS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", masterCounter, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            continue
        completed_units = ["CHEM1003", "MATH1721", "PHYS1030", "MATH1720", "MATH1722"]
        bad_combo2 = False
        for unit in combo:
            prereqs = unit[2]
            for p in prereqs:
                #print("Checking all prerequisites have been completed...")
                if p not in completed_units:
                    bad_combo2 = True
                    #print("Missing prerequisite")
                    #print("Moving onto next combo")
                    break
                else:
                    completed_units.append(unit[0])
                    bad_combo2 = False
                    #print("Valid so far...")
                    continue
            if bad_combo2 == True:
                #print("BREAKING FOR UNITS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", masterCounter, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                break
        if bad_combo == True:
            #print("\n BAD COMBO -------------------------------------------------")
            continue
        else:
            #print("Checking for duplicates...")
            #print(combo)
            final_set = set()
            #print(combo)
            for x in combo:
                final_set.add(x[0])
            #print(final)
            #combo_clean =[]
            if len(final_set) != 12:
                break
            else:
                print(final_set)
            #print('Combo Cleaned...')
            #print(combo_clean)
            '''itemsCheck = False
            final_list = []
            print("Checking accuracy...")
            for item in frame:
                if item in combo_clean:
                    itemsCheck = True
                    final_list.append(item)
                else:
                    itemsCheck = False
                #print(final_list)
               # print(len(final_list))
                #print(final_list)
            if len(final_list) == len(frame):
                print("Confirmed:", final_list)


            if itemsCheck is True:
                #print("Combination is valid", combo_clean)
                updated_combos.append(final_list)
            else:
                #print("Bad combo")
                continue

    #for y in updated_combos:
        #print(y)'''




