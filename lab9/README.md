LAB9
This project was made by:
    Salvatore Tartaglione s317815   
    Luana Pulignano s314156

We have implemented an Evolutionary Algorithm (GA) in which the main functions are:
-select_parent: we've selectd the parent based on tournament selection
-mutate: we've mutated 1 random gene 
-one_cut_cover: we've applied the one cut crossover to the genome of two individuals
The mutation and the one_cut_cover are choosen randomly based on a probability.

The main function uses a counter to track how many times the same max fitness values is reached in a row. If this value is reached 50 times in a row we stop the execution because we have found an optimal individual with a fitness value near to 1.

Results:    
    -POPULATION_SIZE= 100 , OFFSPRING_SIZE=20
        -PROBLEM_DIMENSION = 1:
            -fitness_calls: 42560
            -num_of_generations: 2123
            -best_fit_individual: 0.966
        -PROBLEM_DIMENSION = 2:
            -fitness_calls: 62340
            -num_of_generations: 3112
            -best_fit_individual: 0.9976
        -PROBLEM_DIMENSION = 5:           
            -fitness_calls: 61900
            -num_of_generations: 3090
            -best_fit_individual: 0.9966685
        -PROBLEM_DIMENSION = 10:           
            -fitness_calls: 56860
            -num_of_generations: 2838
            -best_fit_individual: 0.9955666677899999