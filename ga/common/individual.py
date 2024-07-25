class Individual(object):
    """
    Class that contains the informations of an individual solution
    """

    def __init__(self, direction):
        """
        Class constructor
        :param direction: direção do problema (MAX se maximização ou MIN se minimização)
        """
        self.id = 0
        self.rank = None
        self.domination_count = None
        self.num_dominated = None
        self.dominated_solutions = None
        self.decision_vector = None
        self.objective = None
        self.came_from = None
        self.direction = direction











