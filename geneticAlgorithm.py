'''
A genetic algorithm used to find the maximum total weight of items that can 
be inserted into a backpack that hold a maximum of 120 weight.
'''

#####################################################################
# ASSUMPTIONS BEFORE BEGINNING:                                     #
# No weight of an item can exceed the size of the backpack          #
#####################################################################

# imports
import sys, os
import random
import copy

# global variables
population_size = 10
backpack_size = 120


# Gene object with a name, weight, and importance
# Represents a box in the problem
# Contains a printing function defined (repr)
class gene(object):
	def __init__(self, name, weight, importance):
		self.weight = weight
		self.importance = importance
		self.name = name
	def __repr__(self):
		return(str(self.name))

# Chromosome object with a gene_list and fitness number
# Represents the backpack in the problem
# Contains a printing function for fitness and for the list of genes
class chromosome(object):
	def __init__(self, gene_list, fitness):
		self.gene_list = gene_list
		self.fitness = fitness
	def __repr__(self):
		return(str(self.fitness))
	def print_chromosome(self):
		print("Fitness = " + str(self.fitness))
		print("Backpack contents: "),
		for i in self.gene_list:
			print(i),
		print("\n")


# declare the gene_pool with the 7 boxes defined
gene_pool = []		
gene_pool.append(gene(1, 20, 6))
gene_pool.append(gene(2, 30, 5))
gene_pool.append(gene(3, 60, 8))
gene_pool.append(gene(4, 90, 7))
gene_pool.append(gene(5, 50, 6))
gene_pool.append(gene(6, 70, 9))
gene_pool.append(gene(7, 30, 4))


# sorts the population based on the chromosome's fitness
# sorts in order from highest fitness to lowest fitness
def sort_population(population):
	population.sort(key = lambda chromosome: chromosome.fitness, reverse = True)

# calculates the fitness of each chromosome
def get_fitness(chromosome):
	total_importance = 0
	for i in chromosome:
		total_importance += i.importance
	return total_importance

# creates a chromosome from the gene pool
# note: the total weight of each chromosome will be 120 or less
def create_chromosome(gene_pool):
	gene_list = copy.deepcopy(gene_pool)
	total_weight = 350
	genes_in_gene_list = 7

	# removes a random gene until the chromosome weight is less than or equal
	# 	to 120 (backpack size)
	while (total_weight > backpack_size):
		curr = gene_list.pop(random.randint(0,genes_in_gene_list - 1))
		total_weight = total_weight - curr.weight
		genes_in_gene_list -= 1
	return chromosome(gene_list, get_fitness(gene_list))

# defines the genetic algorithm and returns a population of chromosomes
# 	the number of chromosomes in a population is defined as 10
def genetic_algorithm(population):
	for p in range(5):
		for i in range(population_size):
			x = random.choice(population)
			y = random.choice(population)
			# generate a crossover
			child = crossover(x, y)
			# mutate on a 10% chance
			if (random.randint(0,9) == 0):
				child = mutate(child.gene_list)
			population.append(child)
		sort_population(population)
		population = population[:population_size]
	return population



# crossover function that generates a combination of two chromosomes
# 	then cuts from the new chromosome until weight reaches 120 or less
def crossover(x, y):
	new_list = []
	total_weight = 0
	# generate combination of chromosome that will not have repeats of the
	# 	same gene (box)
	for i in range(min(len(x.gene_list), len(y.gene_list))):
		if ((x.gene_list[i]).name != (y.gene_list[i]).name):
			if (not contains(new_list, y.gene_list[i].name)):
				new_list.append(y.gene_list[i])
				total_weight += y.gene_list[i].weight
		if (not contains(new_list, x.gene_list[i].name)):
			new_list.append(x.gene_list[i])
			total_weight += x.gene_list[i].weight
	
	# cuts genes from chromosome until weight equals 120 or less
	while (total_weight > backpack_size):
		curr = new_list.pop(random.randint(0,len(new_list) - 1))
		total_weight = total_weight - curr.weight
	
	return chromosome(new_list, get_fitness(new_list))

# mutation function that mutates a random gene as long as the new gene's weight
# 	is under or equal to 120
def mutate(chromosome_genes):
	good_weight = False
	chromosome_length = len(chromosome_genes)
	total_weight = 0
	for i in chromosome_genes:
		total_weight += i.weight
	
	# keeps trying to mutate until chromosome weight is valid
	while (not good_weight):
		rand_sack = (random.randint(0,6))
		while(contains(chromosome_genes, gene_pool[rand_sack].name)):
			rand_sack = (random.randint(0,6))
	
		# Checks if mutating a random gene to another randomly chosen gene would
		# 	violate less than or equal to 120 weight rule
		rand_pos = random.randint(0,chromosome_length - 1)
		if (total_weight - chromosome_genes[rand_pos].weight + gene_pool[rand_sack].weight <= backpack_size):
			good_weight = True
			chromosome_genes[rand_pos] = gene_pool[rand_sack]
	
	fitness = get_fitness(chromosome_genes)
	return chromosome(chromosome_genes, fitness)

# helper function that checks if a certain gene is within a list of genes
def contains(list, gene_name):
	for i in list:
		if(i.name == gene_name):
			return True
	return False

# main function for genetic algorithm homework
def main():
	# generate the first population
	population = []
	for i in range(population_size):
		population.append(create_chromosome(gene_pool))
	# generate optimal population
	population = genetic_algorithm(population)
	# print out population
	print("Final population after 5 generations:")
	j = 0;
	for i in population:
		j += 1 
		print("Rank: " + str(j))
		i.print_chromosome()


if __name__ == '__main__':
	main()
