
from algorithms.ga import GA
from common.individual import Individual
import copy

class GAElite(GA):
    def non_dominated_sorting(self):
        fronts = [[]]
        for individual in self.population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other in self.population:
                if self.dominates(individual, other):
                    individual.dominated_solutions.append(other)
                elif self.dominates(other, individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                fronts[0].append(individual)
        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for individual in fronts[i]:
                for other in individual.dominated_solutions:
                    other.domination_count -= 1
                    if other.domination_count == 0:
                        other.rank = i + 1
                        next_front.append(other)
            i += 1
            fronts.append(next_front)
        return fronts[:-1]

    def dominates(self, individual1:Individual, individual2:Individual):
        better_in_all = True
        better_in_at_least_one = False
        individual1.fitness = [individual1.objective]
        individual2.fitness = [individual2.objective]
        for i in range(len(individual1.fitness)):
            if individual1.fitness[i] > individual2.fitness[i]:
                better_in_all = False
            if individual1.fitness[i] < individual2.fitness[i]:
                better_in_at_least_one = True
        return better_in_all and better_in_at_least_one

    def calculate_crowding_distance(self, front):
        for individual in front:
            individual.crowding_distance = 0
        num_objectives = len(self.problem.objective)
        for i in range(num_objectives):
            front.sort(key=lambda ind: ind.fitness[i])
            front[0].crowding_distance = float('inf')
            front[-1].crowding_distance = float('inf')
            for j in range(1, len(front) - 1):
                front[j].crowding_distance += (front[j +
                                               1].fitness[i] - front[j - 1].fitness[i])

    def create_offspring(self):
        children = []
        for k in range(self.problem.num_of_individuals -self.elite_size):
            # Seleciona dois pais por meio de torneio de seleção binária
            parent1 = self.do_tournament_selection()
            parent2 = self.do_tournament_selection()
            i=0
            while parent1.decision_vector == parent2.decision_vector:
                parent2 = self.do_tournament_selection()
                i+=1
                if i<20:
                    break


            # Cria um filho a partir do crossover de dois pontos dos pais
            child = self.operators.do_two_point_crossover(parent1=parent1, parent2=parent2, population=self.population)
            #child = self.operators.uniform_crossover(parent1=parent1, parent2=parent2, population=self.population)

            # Aplica a mutação bitflip no filho
            self.operators.do_bitflip(child)

            # Calcula a função objetivo
            self.problem.calculate_objective(child)

            # Adiciona o filho no conjunto de novas soluções
            children.append(copy.deepcopy(child))
        return children
    def select_elites(self, fronts):
        elites = []
        for front in fronts:
            self.calculate_crowding_distance(front)
            front.sort(key=lambda ind: ind.crowding_distance, reverse=True)
            elites.extend(front)
            if len(elites) >= self.elite_size:
                break
        return elites[:self.elite_size]

    def run(self):
        # Cria população inicial
        self.population = self.problem.create_initial_population()

        for i in range(self.problem.num_of_generations):
            # print("Generation: " + str(i))

            # Cria novas soluções
            
            children = self.create_offspring()
            fronts = self.non_dominated_sorting()
            elites = self.select_elites(fronts)
            # Adiciona as novas soluções na população
            self.population.extend(children)
            self.population.extend(elites)

            # Seleciona as num_individuals melhores soluções
            self.do_environmental_selection()

            # Identifica o valor da função objetivo do melhor individuo encontrado até o momento
            if self.problem.direction == 'MAX':
                best_so_far = max(self.population.population,
                                key=lambda obj: obj.objective)
            else:
                best_so_far = min(self.population.population,
                                key=lambda obj: obj.objective)
        
            self.convergence_array.append(best_so_far.objective)

        # Plota o gráfico de convergência
        self.plot_convergence()
        return best_so_far
