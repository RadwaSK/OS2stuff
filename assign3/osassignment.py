import numpy as np
from pulp import *


#Read from file
lines=[]
with open("test.txt") as file:
    for line in file:
        line = line.strip() #or some other preprocessing
        lines.append(line) #storing everything in memory!

NUM_JOBS=int(lines[0])
JOBS=[]
for i in range(1,NUM_JOBS+1):
    a_list = lines[i].split()
    map_object = map(int, a_list)
    list_of_integers = list(map_object)
    JOBS.append(list_of_integers)
#print (JOBS)
STATES=[0]*len(JOBS)
# new names for jobs
rename = 0
#take time from user
while(True):
    time = input("Enter time value: ")
    time=int(time)
    print(time)
    if(time <= 0):
        break




    #LP PROBLEM

    CHOICES_LIST=[]
    prob=LpProblem("SCHEDULE",LpMaximize)
    JOB_SUM=LpVariable("JOB_SUM",lowBound=0)
    TIME_TAKEN=LpVariable("TIME_TAKEN" , lowBound=0)
    JOB_SUM = 0
    TIME_TAKEN =0

    for x in range(len(JOBS)):
        if(len(JOBS[x]) != 0):
            INDICES=range(1 ,len(JOBS[x])+1)
            choices=LpVariable.dicts("Choice"+str(x),(INDICES),cat='Binary')
            CHOICES_LIST.append(choices)
            prob += choices[1] <= 1

            for i in INDICES[1:]:
                prob+=choices[i] <= (lpSum([choices[v] for v in INDICES[0:i-1]]))*(1/(i-1))


            JOB_SUM+=lpSum([CHOICES_LIST[x][v] for v in INDICES])
            TIME_TAKEN+=lpSum([CHOICES_LIST[x][v]*JOBS[x][v-1] for v in INDICES])
        else:
            CHOICES_LIST.append([])
        rename=rename+1


    prob+=JOB_SUM
    prob+=TIME_TAKEN <= time
    status=prob.solve()
    print("number of Jobs executed: "+str(value(prob.objective)))
    for i in range(len(CHOICES_LIST)):
        if(len(CHOICES_LIST[i])!=0):
            for x,y in CHOICES_LIST[i].items():
                if(y.varValue == 1):
                    del JOBS[i][0]
                    STATES[i]+=1


    print("states of current jobs :")
    print (STATES)
    #for i in range(len(JOBS)):
     #   print(STATES[i])
      #  if(STATES[i] != 0):
       ##      del JOBS[i][0]
        #print('here ?')

   # print (JOBS)















