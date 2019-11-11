#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 18:26:36 2019

@author: Juan Sebastián Herrera Cobo

This code solves the scheduling problem using a genetic algorithm. Implementation taken from pyeasyga

As input this code receives:
    1. T = number of jobs [integer]
    2. ni = number of operations of the job i [list of T elements]
    3. m = number of machines [integer]
    3. Mj´ = feasible machines for the operaion j of the job i [matrix of sum(ni) row,  each row with n' feasible machines]
    4. pj'k = processing time of the operation j' in the machine k [matrix of sum(ni) row,  each row with n' feasible machines]
"""
from time import time

# Inputs

#T = 2 # number of jobs
#ni =[2,2] # number of operations of the job i
#ma = 2 # number of machines
#Mij = [[1,2],[1],[2],[1,2]]
#pjk = [[3,4],[5,1000],[1000,6],[2,2]]

#T = 3 # number of jobs
#ni =[2,2,2] # number of operations of the job i
#ma = 2 # number of machines
#Mij = [[1,2],[1,2],[1],[1,2],[2],[1,2]]
#pjk = [[3,4],[5,4],[2,1000],[2,4],[1000,3],[1,2]]

#T = 4 # number of jobs
#ni =[1,3,2,2] # number of operations of the job i
#ma = 3 # number of machines
#Mij = [[1,2,3],[1,3],[3],[1,2],[1,3],[1,2],[1,2,3],[1,3]]
#pjk = [[3,4,3],[5,1000,5],[1000,1000,6],[2,4,3],[1,1000,3],[1,2,1000],[2,2,2],[1,1000,1000]]

#T = 3 # number of jobs
#ni =[2,3,4] # number of operations of the job i
#ma = 5 # number of machines
#Mij = [[1,2,3,4,5],[1,3,4],[3,2],[1,2,5],[1,3,4],[1,2],[1,2,3],[1,3,5],[1,5]]
#pjk = [[3,4,3,4,4],[5,1000,5,4,1000],[1000,4,6,1000,1000],[2,4,1000,1000,4],
#       [1,1000,3,4,1000],[1,2,1000,1000,1000],[2,2,2,1000,1000],[1,1000,1,1000,2],
#       [4,1000,1000,1000,3]]

T = 4 # number of jobs
ni =[2,3,4,2] # number of operations of the job i
ma = 6 # number of machines
Mij = [[1,2,3,4,5],[1,3,4,6],[1,3,2],[1,2,5],[1,2,3,4],[1,2,5],[1,2,3,6],[1,3,5],[1,5,6],
       [1,6],[2,3,4]]
pjk = [[3,4,3,4,4,1000],[5,1000,5,4,1000,4],[3,4,6,1000,1000,1000],[2,4,1000,1000,4,1000],
       [1,3,3,2,1000,1000],[1,3,1000,1000,2,1000],[2,2,2,1000,1000,2],[1,1000,1,1000,2,1000],
       [4,1000,1000,1000,3,3],[3,1000,1000,1000,1000,4],[1000,5,3,4,1000,1000]]

"""

The individual is a list with T*ni*2 digits. For each operation in each job it has the variable S and the variable X
The S for start time to process and the X for the machine where this operation will be done. E.g:
    
    individual = [S11,X11,S12,X12..........Sini,Xini]

But first of all a dataset to be used during the algorithm must be made

"""
from pyeasyga import pyeasyga # import the library to be used
import random

data=[]

data.append(T)
data.append(ni)
data.append(ma)
data.append(Mij)
data.append(pjk)

def is_data_ok(data):
  sum_ni=0
  for i in range(0,len(data[1])):
    sum_ni+=data[1][i]
  if len(data[1])!=data[0]:
    print("Data invalid. Please check the length of ni list")
    exit
  elif len(data[3])!=sum_ni:
    print("Data invalid. Please check the length of Mij list")
    exit
  elif len(data[4])!=sum_ni:
    print("Data invalid. Please check the length of pjk list")
    exit

is_data_ok(data)


"""
To create a random individual a function called create_individual is created. In this case, random values to S from 0 to the max
of pjk*T are generated and for X values between the feasible machines are generated
"""
def max_processing_time(data):
    pjk=data[4]
    max_time=0
    for i in range(0,len(pjk)):
        for j in range(0,len(pjk[i])):
            if pjk[i][j]>max_time and pjk[i][j]!=1000:
                max_time=pjk[i][j]
    return max_time


def create_individual(data):
    individual=[]
    start_times=[0]*data[2]
    jobs=data[0]
    list_to=[2,1,2,0,1,2,0,1,1,0]
    random_number=random.randint(0,len(list_to)-1)
    reference=list_to[random_number]
    if reference == 1:
      a=0
      for i in range(0,jobs):
          for j in range(0,data[1][i]):
              position_X=random.randint(0,len(data[3][a])-1)
              X=data[3][a][position_X]
              S=start_times[X-1]
              individual.append(S)
              individual.append(X)
              start_times[X-1]=start_times[X-1]+data[4][a][X-1]
              a+=1
    elif reference == 2:
      a=len(data[3])-1
      for i in range(0,jobs):
          for j in range(0,data[1][i]):
              position_X=random.randint(0,len(data[3][a])-1)
              X=data[3][a][position_X]
              S=start_times[X-1]
              individual.append(S)
              individual.append(X)
              start_times[X-1]=start_times[X-1]+data[4][a][X-1]
              a-=1
    else:
      for i in range(0,jobs):
          for j in range(0,data[1][i]):
              X=random.randint(1,data[2])
              max_time=max_processing_time(data)
              S=random.randint(0,max_time)
              individual.append(S)
              individual.append(X)
    return individual
  
def mutate(individual):
  mutate_index1=random.randrange(len(individual))
  mutate_index2=random.randrange(len(individual))
  #max_time=max_processing_time(data)
  if ((mutate_index1%2)==0 and (mutate_index2%2)==0) or ((mutate_index1%2)!=0 and \
      (mutate_index2%2!=0)):
    individual[mutate_index1], individual[mutate_index2] = individual[mutate_index2], individual[mutate_index1]
  elif (mutate_index1%2)==0 and (mutate_index2%2)!=0:
    #if individual[mutate_index1]>(max_time/2):
     # individual[mutate_index1]=individual[mutate_index1]+random.randint(-(max_time/2),(max_time/2))
    new_index=random.randrange(0,len(individual),2)
    individual[mutate_index1], individual[new_index] = individual[new_index], individual[mutate_index1]
    individual[mutate_index2]=random.randint(1,data[2])
  else:
    #if individual[mutate_index2]>(max_time/2):
     # individual[mutate_index2]=individual[mutate_index2]+random.randint(-(max_time/2),(max_time/2))
    new_index=random.randrange(0,len(individual),2)
    individual[mutate_index2], individual[new_index] = individual[new_index], individual[mutate_index2]
    individual[mutate_index1]=random.randint(1,data[2])
    
"""
The fitness function is divided in two parts: 1. the Cmax is calculated from the individual, 2. the restrictions of the 
problema are validated to count how many fouls has the individual. At the end the fitness value = cmax + fouls*constant
"""
def is_feasible_machine(operation,machine,data):
    Mij=data[3]
    count=0
    for i in range(0,len(Mij[operation])):
        if machine==Mij[operation][i]:
            count+=1
    if count == 0:
        return False
    else:
        return True

def operations_in_machine(machine,individual):
    result=[]
    i=0
    while i<len(individual):
        if individual[i+1]==machine:
            result.append(int(i/2))
        i+=2
    return result
    
def fitness(individual,data):
    fitness=0
    pjk=data[4]
    i=0
    for op in range(0,len(pjk)):
        if (individual[i]+pjk[op][individual[i+1]-1])>fitness:
            fitness=individual[i]+pjk[op][individual[i+1]-1]
        i+=2
    # ------restrictions---------------
    fouls=0
    j=0
    k=0
    # for each job, C of current operation must be less than the next
    for job in range(0,len(ni)):
        for op2 in range(0,ni[job]-1):
          if (individual[j]+pjk[k][individual[j+1]-1])>individual[j+2] or\
            individual[j]>=individual[j+2]:
              fouls+=4
          j+=2
          k+=1
        j+=2
        k+=1
    # an operation must be made in a feasible machine
    l=0
    while l<len(individual):
        if not is_feasible_machine(int(l/2),individual[l+1],data):
            fouls+=2
        l+=2
        
    # for each machine an operation must start at zero
    # for each mahcine, the operations cannot be mixed. Only one operation at a time
    count_zeros=0
    for machine2 in range(1,data[2]+1):
      #count_zeros=0
      operations2=operations_in_machine(machine2,individual)
      for op4 in range(0,len(operations2)):
        if individual[operations2[op4]*2]==0:
          count_zeros+=1
        start_reference=individual[operations2[op4]*2]
        end_reference=individual[operations2[op4]*2]+pjk[operations2[op4]][machine2-1]
        for op5 in range(0,len(operations2)):
          if op5 != op4:
            s=individual[operations2[op5]*2]
            c=individual[operations2[op5]*2]+pjk[operations2[op5]][machine2-1]
            if s<=start_reference and c>=end_reference:
              fouls+=2
            elif s>=start_reference and s<=end_reference and c<=end_reference:
              fouls+=2
            elif s<=start_reference and c>start_reference and c<=end_reference:
              fouls+=2
            elif s>=start_reference and s<end_reference and c>=end_reference:
              fouls+=2
      #if count_zeros != 1:
        #fouls+=1
    if count_zeros == 0:
      fouls+=1
    fitness=fitness+(fouls*1000)
    return fitness
 
"""
At the end the create_individual and the fitness functions are added to the ga. Then run and print the best individual
"""
steps=[]
count_increment=0

def genetic_algorithm_scheduling(data,counter,pop_size=100,num_generations=500):
  start_time=time()
  ga=pyeasyga.GeneticAlgorithm(data,maximise_fitness=False,population_size=pop_size,generations=num_generations,mutation_probability=0.3) # initialization of the algorithm
  ga.create_individual=create_individual
  ga.mutate_function=mutate
  ga.fitness_function=fitness
  ga.run()
  best_individual=ga.best_individual()
  steps.append(best_individual)
  best_fitness=best_individual[0]
  if best_fitness>1000 and counter<10:
    counter+=1
    new_generations=num_generations+100
    print("Incrementing generations to ",new_generations,"......")
    genetic_algorithm_scheduling(data,counter,pop_size,new_generations)
  elif best_fitness>1000 and counter==10:
    print("Feasible individual wasn't found!")
    print("Best infeasible individual: ",ga.best_individual())
    end_time=time()
    print("The execution time was: ",(end_time-start_time)," seconds")
  elif best_fitness<1000:
    end_time=time()
    print("Best feasible individual found! ",ga.best_individual())
    print("The execution time was: ",(end_time-start_time)," seconds")
    print("These were the different best individuals:")
    for i in range(0,len(steps)):
      print(steps[i])
    return steps
  

genetic_algorithm_scheduling(data,count_increment,pop_size=200)


