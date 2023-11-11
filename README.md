Lab2 solution made with Salvatore Tartaglione s317815

In Lab 2, we implemented a solution using the evolutionary strategy (1+lambda). Key components include:
-Population:
 Each individual in the population possesses a genome representing both the row index and  the number of elements to be removed from that row. This genome essentially defines a  single move.

-generate_child Function:
 The generate_child function creates a child based on a normal distribution, and this  process is adapted within the strategy.

-Fitness Evaluation:
 The fitness function evaluates the number of rows with an odd count of sticks. A lower  count corresponds to a higher score.

-Main Evolutionary Strategy (es) Function:
 The es function serves as the main strategy. It involves generating, ordering, and   producing lambda children by selecting the best parent. Additionally, the function counts   the number of fitness calls to dynamically adapt the sigma value. Finally, the worst parent  from the previous population is replaced with the children. The function concludes by   returning the best individual from the latest generation.