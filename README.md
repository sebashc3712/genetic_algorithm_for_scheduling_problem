# Genetic algorithm for solving scheduling problem
An implementation of genetic algorithm for solving the scheduling problem in flexible job shop

This code solves the scheduling problem using a genetic algorithm. Implementation taken from pyeasyga
As input this code receives:

    1. T = number of jobs [integer]
    2. ni = number of operations of the job i [list of T elements]
    3. m = number of machines [integer]
    3. Mj´ = feasible machines for the operaion j of the job i [matrix of sum(ni) row,  each row with n' feasible machines]
    4. pj'k = processing time of the operation j' in the machine k [matrix of sum(ni) row,  each row with n' feasible machines]

An example of the input is shown below:

    T = 4 # number of jobs
    ni =[2,3,4,2] # number of operations of the job i
    ma = 6 # number of machines
    Mij = [[1,2,3,4,5],[1,3,4,6],[1,3,2],[1,2,5],[1,2,3,4],[1,2,5],[1,2,3,6],[1,3,5],[1,5,6],
           [1,6],[2,3,4]]
    pjk = [[3,4,3,4,4,1000],[5,1000,5,4,1000,4],[3,4,6,1000,1000,1000],[2,4,1000,1000,4,1000],
           [1,3,3,2,1000,1000],[1,3,1000,1000,2,1000],[2,2,2,1000,1000,2],[1,1000,1,1000,2,1000],
           [4,1000,1000,1000,3,3],[3,1000,1000,1000,1000,4],[1000,5,3,4,1000,1000]]

The individual is a list with T*ni*2 digits. For each operation in each job it has the variable S and the variable X
The S for start time to process and the X for the machine where this operation will be done. E.g:

    individual = [S11,X11,S12,X12..........Sini,Xini]
    
To get more information you can read the guide in the repository. However it's only available in spanish. The traslation into english is on going.

## Use of the algorithm

To use the algorithm you only have to download the file and import it:

    import scheduling_ga_JSHC.py

And then in your code call the function:

     genetic_algorithm_scheduling(data,counter,pop_size=100,num_generations=500)

it receives the data in the format mentioned before, an integer variable (counter), the population size (pop_size) and the number of generations (num_generations)

This functions increases the number the generations when a feasible solution is not found with the current number of generations (this depends on the complexity of the problem)

## License

MIT
