class OneMax:

    def f1(self, decision_vector):
        """
        Função de benchmark simples, que apenas soma os valores do vetor de decisão de um indivíduo
        :param decision_vector: vetor de decisão de um indivíduo
        :return:
        """
        return sum(decision_vector)