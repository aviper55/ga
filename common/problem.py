from common.individual import Individual
import random
from common.population import Population

class Problem:
    """
    Classe que controla o problema e os parâmetros de otimização
    """
    def __init__(self,
                 objective,
                 num_of_variables,
                 variables_range,
                 num_of_individuals,
                 direction,
                 num_of_generations,
                 mutation,
                 tournament_prob,
                 num_of_tour_particips,
                 constraints=None,
                 penalty_value=None,
                 expand=True):
        self.num_of_variables = num_of_variables
        self.tournament_prob = tournament_prob
        self.num_of_tour_particips = num_of_tour_particips
        self.num_of_individuals = num_of_individuals
        self.objective = objective
        self.expand = expand
        self.penalty_value=penalty_value
        self.variables_range = variables_range
        self.direction = direction
        self.num_of_generations = num_of_generations
        self.variables = self.set_variables()
        self.mutation = mutation
        self.constraints = constraints
        self.tabu = set()

    def set_variables(self):
        """
        Função que define as variáveis factíveis para o problema
        :return: O conjunto de variáveis factíveis para o problema
        """
        variables = [i for i in range(min(self.variables_range), max(self.variables_range) + 1)]
        
        return variables

    def create_initial_population(self):
        """
        Função que cria a população inicial de modo aleatório
        :return: returna a população com 'num_of_individuals' novas soluções
        """
        population = Population()
        for _ in range(self.num_of_individuals):
            if self.variables_range[-1] > 1:
                individual = self.generate_unique_individual()
            else:
                individual = self.generate_individual()
            individual.id = _
            individual.trace = [_ for i in range(self.num_of_variables)]
            self.calculate_objective(individual)
            population.append(individual)
            population.last_id = _
        return population

    def generate_individual(self):
        """
        Cria um novo indivíduo
        :return: o objeto do indivíduo
        """
        individual = Individual(self.direction)
        individual.decision_vector = [random.randint(min(self.variables_range), max(self.variables_range)) for x in range(self.num_of_variables)]
        return individual


    def generate_unique_individual(self):
        """
        Cria um novo indivíduo
        :return: o objeto do indivíduo
        """
        individual = Individual(self.direction)
        individual.decision_vector = random.sample(range(self.num_of_variables), self.num_of_variables)
        # individual.decision_vector = [random.randint(min(self.variables_range), max(self.variables_range)) for x in range(self.num_of_variables)]
        return individual
    
    def calculate_objective(self, individual):
        """
        Calcula a função objetivo do indivíduo
        :param individual: indivíduo recebido que deve ter sua função objetivo calculada
        :return: nothing
        """
        individual.objective = [f(individual.decision_vector) for f in self.objective]
        individual.objective = individual.objective[0]

