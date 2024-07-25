class Population:
    """
    Class that holds the entire population
    """

    def __init__(self):
        """
        Construtor da classe
        """
        self.population = []
        self.last_id = 0
        self.var_count = []
        self.probs = []
        self.probs_cluster = []
        self.fronts = []
        self.distances = []

    def __len__(self):
        """
        Função que retorna o tamnaho da população atual
        :return: tamnaho da população atual
        """
        return len(self.population)

    def __iter__(self):
        """
        Permite a iteração entre os objetos da classe
        :return:
        """
        return self.population.__iter__()

    def extend(self, new_individuals):
        """
        Aumenta a população atual com um conjunto de novas soluções
        :param new_individuals: conjunto de novos indivíduos
        :return:
        """
        self.population.extend(new_individuals)

    def append(self, new_individual):
        """
        Adiciona um único individuo novo à população atual
        :param new_individual: novo indivíduo
        :return:
        """
        self.population.append(new_individual)