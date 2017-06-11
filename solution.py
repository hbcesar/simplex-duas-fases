# -*- coding: utf-8 -*-
import sys
import numpy as np

class Solution(object):
	def __init__(self, matrix):
		self.linhas = len(matrix)
		self.colunas = len(matrix[0])

	#verifica se vetor é canonico
	def canonico(self, vector):
		#lembrar de transpor matriz
		temp = np.array(vector)
		temp = temp.transpose()

		base = np.eye(self.linhas)

		for i in range(self.linhas):
			if np.array_equal(temp, base[i,:]):
				return True

		return False

	#verifica solucao, caso alguma coluna da matriz tenha todos elementos menores ou iguais a zero, nao possui solucao
	def noSolution(self, matrix):

		for i in range(1, self.colunas): #percorre as colunas da matriz
			allNegative = True

			for j in range(self.linhas): #percorre as linhas de uma coluna
				if matrix[j][i] >= 0: #se encontrar elemento maior que zero, significa que aquela coluna é valida
					allNegative = False
					break

			if(allNegative): #se nao encontrou elemento positivo naquela coluna, aborta.
				print("Encontrada coluna com todos elementos negativos: Tableau não possui solução.")
				print("Abortando")
				return True


		# if any(all(i <= 0 for i in matrix[1:,:])) and any(all(i is not 0 for i in matrix[1:,0])):
		# 	return True
		# else:
		# 	return False

	#Verifica se dado um Tableau
	#todos os zj - cj são menores ou iguais a zero, ou seja
	#se ja é solução otima.
	def optimalSolution(self, matrix):

		# for cell in matrix[0][1:]:
		# 	if cell > 0:
		# 		return False
		# return True
		if all(i <= 0 for i in matrix[0,1:]):
			return True
		else:
			return False

	#Verifica se, depois de chegar na solução ótima,
	#existe alguma variável não básica cujo zj-cj = 0
	def multipleSolution(self, matrix):
		for i in range(1, self.colunas):
			if not self.canonico(matrix[:,i]) and matrix[0][i] is 0:
				return True
			else:
				return False

	#Verifica se depois de chegar na ótima, existe alguma variável básica igual a zero
	def degenerada(self, matrix):
		for i in range(1, self.colunas):
			if self.canonico(matrix[:,i]):
				posicao, = np.unravel_index(matrix[:,i].argmax(), matrix[:,i].shape)

				if matrix[posicao][0] == 0:
					return True

		return False

	def mountSolution(self, matrix):
		x = np.zeros(self.colunas -1)

		for i in range(1, self.colunas):
			if self.canonico(matrix[:,i]):
				posicao, = np.unravel_index(matrix[:,i].argmax(), matrix[:,i].shape)
				x[i-1] = matrix[posicao][0]

		z = matrix[0][0]

		return x, z

	def artificial(self, matrix):
		bases = np.eye(self.linhas - 1, dtype=int)

		for i in range(self.linhas - 1):
			#verificar se da segunda linha em diante forma uma base
			if np.array_equal(bases[i,:], matrix[1:]):
				if matrix[0] == -1:
					return True

		return False