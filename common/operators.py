import random



class Operators():
    def __init__(self,
                 problem):
        self.problem = problem



    def uniform_crossover(self, parent1, parent2, population):
        """
        Função que realiza o crossover uniforme
        :param parent1: objeto do pai numero 1
        :param parent2: objeto do pai numero 2
        :param population: população de soluções
        :return: uma solução filha criada a partir do crossover dos pais 1 e 2
        """
        population.last_id += 1
        child1 = self.problem.generate_individual()
        child1.id = population.last_id

        for i in range(len(parent1.decision_vector)):
            if random.random() > 0.5:
                child1.decision_vector[i] = parent1.decision_vector[i]
            else:
                child1.decision_vector[i] = parent2.decision_vector[i]

        return child1

    def do_two_point_crossover(self, parent1, parent2, population):
        """
        Função que realiza o crossover de dois pontos
        :param parent1: objeto do pai numero 1
        :param parent2: objeto do pai numero 2
        :param population: população de soluções
        :return: uma solução filha criada a partir do crossover dos pais 1 e 2
        """

 

        population.last_id += 1
        if self.problem.variables_range[-1] > 1:
            # integer
            child1 = self.problem.generate_unique_individual()
        else:
            child1 = self.problem.generate_individual()
        child1.id = population.last_id


        geneA = int(random.random() * len(parent1.decision_vector) - 2)
        geneB = int(random.random() * len(parent1.decision_vector) - 2)

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(0, startGene):
            child1.decision_vector[i] = parent1.decision_vector[i]

        for i in range(startGene, endGene):
            child1.decision_vector[i] = parent2.decision_vector[i]

        for i in range(endGene, len(parent1.decision_vector)):
            child1.decision_vector[i] = parent1.decision_vector[i]

        return child1


    def do_bitflip(self, child):
        """
        Função que realiza a mutação bit-flip
        :param child: Solução filha 
        :return: Solução filha com mutação bit-flip aplicada
        """
        if self.problem.variables_range[-1] > 1:
            return self.swap_mutation(child)
        num_of_features = len(child.decision_vector)
        for gene in range(num_of_features):
            u = random.uniform(0, 1)
            prob = self.problem.mutation
            if u < prob:
                if child.decision_vector[gene] == 1:
                    child.decision_vector[gene] = 0
                else:
                    child.decision_vector[gene] = 1

    # def do_bitflip_int(self, child):
    #     """
    #     Perform a bit-flip mutation on an individual's decision vector.
        
    #     """
    #     # Select a random position in the decision vector
    #     position = random.randint(0, len(child.decision_vector) - 1)
        
    #     # Generate a new value within the specified range, ensuring it's different from the current value
    #     current_value = child.decision_vector[position]
    #     new_value = current_value
    #     while new_value == current_value:
    #         new_value = random.randint(min(self.problem.variables_range), max(self.problem.variables_range))
        
    #     # Apply the mutation
    #     child.decision_vector[position] = new_value
    def swap_mutation(self,child):
        if random.random() < self.problem.mutation:
            num_of_features = len(child.decision_vector)
            i, j = random.sample(range(num_of_features), 2)
            decision = child.decision_vector
            decision[i], decision[j] = decision[j], decision[i]
            child.decision_vector = decision

