LAB9
This project was made by:
    Salvatore Tartaglione s317815   
    Luana Pulignano s314156

We have implemented an Evolutionary Algorithm (GA) in which the main functions are:
-select_parent: we've selectd the parent based on tournament selection
-mutate: we've mutated 1 random gene 
-one_cut_cover: we've applied the one cut crossover to the genome of two individuals
The mutation and the one_cut_cover are choosen randomly based on a probability.
Results:    
    -POPULATION_SIZE= 100 , NUMBER_OF_GENERATIONS = 100,OFFSPRING_SIZE=20,
        -PROBLEM_DIMENSION = 1:
            -fitness_calls: 2100
            -best_fit_individual: 0.627
        -PROBLEM_DIMENSION = 2:
            -fitness_calls: 2100
            -best_fit_individual: 0.6254
        -PROBLEM_DIMENSION = 5:           
            -fitness_calls: 2100
            -best_fit_individual: 0.677395
        -PROBLEM_DIMENSION = 10:           
            -fitness_calls: 2100
            -best_fit_individual: 0.73012255685