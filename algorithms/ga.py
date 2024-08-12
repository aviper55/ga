import copy
import matplotlib.pyplot as plt
from common.operators import Operators
import random
import heapq
class GA:
    def __init__(self, problem, elite_size):
        self.problem = problem
        self.operators = Operators(problem=self.problem)
        self.population = None
        self.convergence_array = []
        self.elite_size = elite_size

    def plot_convergence(self):
        # cria a figura
#        plt.style.use('seaborn-white')
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        # define o eixo x
        x_axis = [i for i in range(self.problem.num_of_generations)]

        # define o eixo y
        y_axis = self.convergence_array

        # formata o tamanho da fonte nos eixos
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.ylabel("Valor da função objetivo", fontsize=16)
        plt.xlabel("Gerações", fontsize=16)

        # plota o gráfico
        plt.plot(x_axis,y_axis, marker='o', color='blue', linestyle='None')
        plt.show()
        plt.savefig('convergence.png')


    def do_tournament_selection(self):
        try:
            # Seleciona num_of_tour_particips individuos aleatoriamente na população atual
            participants = random.sample(self.population.population, self.problem.num_of_tour_particips)

            # Avalia qual possui a maior função objetivo e retorna-o
            if self.problem.direction == 'MAX':
                best = max(participants, key=lambda obj: obj.objective)
            else:
                best = min(participants, key=lambda obj: obj.objective)
            
            return best
        except Exception as e:
            print("Error in tournament selection:")
            print(e)

    def create_offspring(self):
        children = []
        for k in range(self.problem.num_of_individuals):
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

            # Aplica a mutação bitflip no filho
            self.operators.do_bitflip(child)

            # Calcula a função objetivo
            self.problem.calculate_objective(child)

            # Adiciona o filho no conjunto de novas soluções
            children.append(copy.deepcopy(child))
        return children

    def do_environmental_selection(self):
        # Remove os piores individuos da população, mantendo apenas os num_of_individuals melhores
        if self.problem.direction == 'MAX':
            new_population = heapq.nlargest(self.problem.num_of_individuals, self.population.population, key=lambda obj: obj.objective)
        else:
            new_population = heapq.nsmallest(self.problem.num_of_individuals, self.population.population, key=lambda obj: obj
            .objective)
        self.population.population = new_population

    def run(self):
        # Cria população inicial
        self.population = self.problem.create_initial_population()

        for i in range(self.problem.num_of_generations):
            # print("Generation: " + str(i))

            # Cria novas soluções
            children = self.create_offspring()

            # Adiciona as novas soluções na população
            self.population.extend(children)

            # Seleciona as num_individuals melhores soluções
            self.do_environmental_selection()

            # Identifica o valor da função objetivo do melhor individuo encontrado até o momento
            best_so_far = max(self.population.population, key=lambda obj: obj.objective)

            # Adiciona no vetor de convergência o melhor indivíduo encontrado até o momento
            self.convergence_array.append(best_so_far.objective)

        # Plota o gráfico de convergência
        self.plot_convergence()
        return best_so_far