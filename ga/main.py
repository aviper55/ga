from algorithms.ga import GA
from common.problem import Problem
from benchmarks.onemax import OneMax

# Parâmetros do problema
num_of_variables = 100
num_of_individuals = 100
generations = 30
variables_range = [0,1]

# Parâmetros do algoritmo
tournament_prob = 1.0
num_of_tour_particips = 2
mutation = 1/num_of_variables

benchmark = OneMax()
direction = "MAX"

# define a classe de problema
problem = Problem(num_of_variables=num_of_variables,
                      num_of_individuals=num_of_individuals,
                      num_of_generations=generations,
                      objective=[benchmark.f1], # ATENÇÃO: aqui ele passa uma função
                      mutation=mutation,
                      variables_range=variables_range,
                      direction=direction,
                      tournament_prob=tournament_prob,
                      num_of_tour_particips=num_of_tour_particips)

ga = GA(problem=problem,
        elite_size=10)

ga.run()

