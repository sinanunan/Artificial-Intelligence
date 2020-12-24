'''
A neural network algorithm that can train to predict the type of flowers
'''


import math
import random
import network_class
from time import sleep
import sys


random.seed(random.random())

LEARNING_RATE = 0.7 
EPOCH = 25          # The iterations
PREFERRED_RATE = 95 # Preferred accuracy
NEURON = [3, 7, 3]


# A helper function to multiply two matrices
# Used in checking the accuracy of the ANN
def multiply_matrices(matrix1, matrix2, neur1):

	result_matrix = [[0 for i in range(len(matrix2[0]))] for i in range(len(matrix1))]    
	for i in range(len(matrix1)):
		for j in range(len(matrix2[0])):
			for k in range(len(matrix2)):
				result_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
			result_matrix[i][j] += neur1[j]
	return result_matrix

# A helper function to multiply a matrix with a vector
# Used in backpropogation
def multiply_matrix_with_vector(matrix1, vector2):
	x = [0 for i in range(len(matrix1))]
	for i in range(len(matrix1)):
		for j in range(len(vector2)):
			x[i] += matrix1[i][j] * vector2[j]
	return x

# A helper function to multiply a vector with a matrix
# Used in forward propogation
def multiply_vector_with_matrix(vector1, matrix2, neur1):
	result_matrix = [0 for i in range(len(matrix2[0]))]
	for r in range(len(matrix2[0])):
		for c in range(len(matrix2)):
			result_matrix[r] += neur1[r]
			result_matrix[r] += vector1[c] * matrix2[c][r]
	return result_matrix



# The sigmoid function is used as an classic activation function 
def sigmoid_function(x):
	for i in range(len(x)):
		x[i] = 1 / (1 + math.exp(-x[i]))
	return x

# A function to train a neural network
def train(NeuralNetwork):
	for error in range(EPOCH):
		for y,x in enumerate(NeuralNetwork.train_info):
			
			hidden_output = forward_propogation(NeuralNetwork.weight1, NeuralNetwork.neur1, x)
			output = forward_propogation(NeuralNetwork.weight2, NeuralNetwork.neur2, hidden_output)
			
			target = [0, 0, 0]
			target[int(NeuralNetwork.train_class[y])] = 1

			delta_1 = backward_propogation(NeuralNetwork.weight2, NeuralNetwork.neur2, hidden_output, output, NEURON[2], NEURON[1], target)

			delta_2 = multiply_matrix_with_vector(NeuralNetwork.weight2, delta_1)
			for j in range(NEURON[1]):
				delta_2[j] = delta_2[j] * (hidden_output[j] * (1-hidden_output[j]))
			
			for i in range(NEURON[0]):
				for j in range(NEURON[1]):
					NeuralNetwork.weight1[i][j] -=  LEARNING_RATE * (delta_2[j] * x[i])
					NeuralNetwork.neur1[j] -= LEARNING_RATE * delta_2[j]
		
		if(error % 100 == 0):
			x = float(error) / EPOCH * 100

def forward_propogation(NNweight, NNneur, hidden_matrix):
	potential = multiply_vector_with_matrix(hidden_matrix, NNweight, NNneur)
	return sigmoid_function(potential)

def backward_propogation(NNweight, NNneur, x1, x2, range1, range2, target):
	delta = []
	for j in range(range1):
		delta.append(-1 * (target[j] - x2[j]) * x2[j] * (1 - x2[j]))
	for i in range(range2):
		for j in range(range1):
			NNweight[i][j] -= LEARNING_RATE * (delta[j] * x1[i])
			NNneur[j] -= LEARNING_RATE * delta[j]
	return delta
	

# A functioj to test the accuracy of the neural network
def check_accuracy(NeuralNetwork):
	
	initial_prediction   = multiply_matrices(NeuralNetwork.test_info, NeuralNetwork.weight1, NeuralNetwork.neur1)
	final_prediction     = multiply_matrices(initial_prediction, NeuralNetwork.weight2, NeuralNetwork.neur1)
	
	total_questions = len(final_prediction)
	correct_answers = 0
	
	prediction = []
	for x in final_prediction:
		prediction.append(max(enumerate(x), key=lambda x:x[1])[0])
	
	for i in range(total_questions):
		if(prediction[i] == NeuralNetwork.test_class[i]):
			correct_answers += 1
	
	percent = float(correct_answers) / total_questions * 100
	if (percent > PREFERRED_RATE):
		print("\nThe Neural Network has been trained")
		print("\nTesting results")
		print(str(correct_answers) + " true out of " + str(total_questions) + " tests.")
		print("Trained AI Accuracy: " + str(round(percent, 2)) + "\n\n")

	return percent

# This function gets input from the user and manually tests the neural network
def testANN(NeuralNetwork):

	sepal_len = float(input("Sepal Length: "))
	sepal_wid = float(input("Sepal Width: "))
	petal_len = float(input("Petal Length: "))
	petal_wid = float(input("Petal Width: "))
	
	input_matrix = [[sepal_len, sepal_wid, petal_len, petal_wid]]

	initial_prediction = multiply_matrices(input_matrix, NeuralNetwork.weight1, NeuralNetwork.neur1)
	final_prediction  = multiply_matrices(initial_prediction, NeuralNetwork.weight2, NeuralNetwork.neur1)

	print(final_prediction[0])
	print(max(final_prediction[0]))
	print(final_prediction[0][0])
	print(final_prediction[0][1])
	print(final_prediction[0][2])

	if(max(final_prediction[0]) == final_prediction[0][0]):
		print("\nPrediction: Iris-setosa")
	elif(max(final_prediction[0]) == final_prediction[0][1]):
		print("\nPrediction: Iris-versicolor")
	else:
		print("\nPrediction: Iris-virginica")




def main():
	
	if (len(sys.argv) != 2):
		print("Usage: ann.py [Iris-database]")
		exit()  
	print("\nCreating artificial neural network")
	sleep(1)
	print("Starting to train the neural network\n")
	sleep(1)
	percent = 0
	while (percent < PREFERRED_RATE):
		print("Continuing to train the neural network")
		ANN = network_class.NeuralNetwork(sys.argv[1])
		train(ANN)
		percent = check_accuracy(ANN)
		sleep(0.1)

	test_input = 'a'  	
	while (test_input != 'q'):
		test_input = input('Do you want to manually test the ANN? (y for yes/q for quit) ') 
		if (test_input == 'y'):
			testANN(ANN)
		elif (test_input != 'q'):
			print("input not recognized")



if __name__ == '__main__':
	main()
