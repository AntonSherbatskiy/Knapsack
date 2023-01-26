class input_parameter():
    def __init__(self) -> None:
        self.population_quantity = int(0)
        self.items_quantity = int(0)
        self.max_item_fitness = int(0) 
        self.max_weight = int(0)
        self.mutation_chance = float(0)
        self.iterations_quantity = int(0)
        self.crossing_type = str(None)
        self.crossing_successor = int(0) 
        self.is_local_upgrade = str(None)
        self.iterations_to_log = int(0)

    def input(self):
        self.population_quantity = int(input("Enter quantity of population: "))
        self.items_quantity      = int(input("Enter quantity of items in knapsack: "))
        self.max_item_fitness    = int(input("Enter max fitness per item: "))
        self.max_weight          = int(input("Enter max weight: "))
        self.mutation_chance     = float(input("Enter chance of mutation: "))
        self.iterations_quantity = int(input("Enter quantity of iterations: "))
        self.crossing_type       = str(input("Enter crossing type('prop' or 'point'): "))

        if self.crossing_type != "prop" and self.crossing_type != "point":
            raise ValueError("Only [prop] or [point] allowed!")

        self.crossing_successor  = int(input("\tEnter [1] to use standard crossing or enter [2] to use double crossing: "))

        if self.crossing_successor != 1 and self.crossing_successor != 2:
            raise ValueError("Only [1] or [2] allowed!")

        self.is_local_upgrade    = str(input("\tEnter [true] to use local upgrade or enter [false] to use standard module: "))
        self.iterations_to_log   = int(input("Enter iterations to log: "))

        if self.is_local_upgrade == "False".lower():
            self.is_local_upgrade = bool(False)
        else:
            self.is_local_upgrade = bool(True)