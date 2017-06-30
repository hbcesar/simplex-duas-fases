# -*- coding: utf-8 -*-
import sys
import math
import numpy as np
from solution import Solution

class MetodoSimplex(object):
	def __init__(self, matrix):
		self.s = Solution(matrix)

	#verifica se primeira fase chegou ao fim
	def endFistPhase(self, matrix, zArtif):
		if all(i <= 0 for i in matrix[0,1:]):
			if np.array_equal(matrix[0,:],zArtif):
				return True

	#calcula a primeira fase
	def primeiraFase(self, matrix, vb):
		print "\nIniciando primeira fase:"
		print ""

		print "Tableau inicial:"
		print np.matrix(matrix)
		print ""

		numLinhas = len(matrix) - 2
		numColunas = len(matrix[0]) - 1

		zArt = matrix[0]
		count = 0
		passo = 0

		for i in range(numColunas + 1):
			if zArt[i] < 0:
				count += 1

		for i in range(1, numColunas + 1):
			if self.s.artificial(matrix[:,i].transpose()):
				posicao, = np.unravel_index(matrix[:, i].argmax(), matrix[:, i].shape)
				matrix[0,:] = matrix[0,:] + matrix[posicao,:]

		print "Quadro Tableau"
		print np.matrix(matrix)
		print ""

		while not self.endFistPhase(matrix, zArt):
			posicaoMaior, = np.unravel_index(matrix[0, 1:].argmax(), matrix[0, 1:].shape)
			posicaoMaior = posicaoMaior + 1 #precisa incrementar, visto que retorna a posicao relativa ao slice

			#cria um vetor para armazenar divisoes
			div = np.zeros(numLinhas)
			for i in range(numLinhas):
				div[i] = float("inf")


			for i in range(2, numLinhas + 2):
				if matrix[i][posicaoMaior] > 0:
					div[i-2] = matrix[i][0] / matrix[i][posicaoMaior]

			#Procura menor divisao e guarda linha
			posicaoMenor, = np.unravel_index(div.argmin(), div.shape)
			posicaoMenor = posicaoMenor + 2

			pivo = matrix[posicaoMenor][posicaoMaior]

			if pivo == 0:
				sys.exit(1)

			if pivo != 1:
				matrix[posicaoMenor, :] = matrix[posicaoMenor, :] / pivo

			for i in range(len(matrix)):
				if i != posicaoMenor:
					if matrix[i][posicaoMaior] != 0:
						matrix[i, :] = matrix[i, :] - matrix[i][posicaoMaior] * matrix[posicaoMenor, :]

			passo = passo + 1
			print "\nTableau - Primeira fase - Passo: ", passo
			print matrix

		#confere se e possivel continuar para segunda fase
		if matrix[0][0] != 0:
			print "Conjunto de soluções é vazio\n"
			print "Za:", matrix[0][0]
			print "Fim\n"
			sys.exit(1)

		return matrix, count, vb

	#realiza segunda fase
	def simplex(self, matrix, vb):
		print "Tableau inicial:"
		print matrix
		print ""

		numLinhas = len(matrix)
		numColunas = len(matrix[0])
		numVB = numLinhas
		passo = 0

		if self.s.noSolution(matrix):
			sys.exit(1)

		if self.s.optimalSolution(matrix):
			if self.s.multipleSolution(matrix):
				print "Problema possui múltiplas soluções..."
			else:
				print "Solucao única encontrada."

			if self.s.degenerada(matrix):
				print "Problema possui solução degenerada."

			x,z = self.s.mountSolution(matrix)

			print "Quadro ótimo:"
			print(matrix)
			print "X* = ", x
			print "Z* = ", z

			return matrix, x, z

		while not self.s.optimalSolution(matrix):
			posicaoMaior, = np.unravel_index(matrix[0, 1:].argmax(), matrix[0, 1:].shape)
			posicaoMaior = posicaoMaior + 1 #precisa incrementar, visto que retorna a posicao relativa ao slice

			#cria um vetor para armazenar divisoes
			div = np.zeros(numLinhas)
			for i in range(numLinhas):
				div[i] = float("inf")

			for i in range(1, numLinhas):
				if matrix[i][posicaoMaior] > 0:
					div[i-1] = matrix[i][0] / matrix[i][posicaoMaior]

			#Procura o menor da divisao e guarda linhas
			#Procura menor divisao e guarda linha
			posicaoMenor, = np.unravel_index(div.argmin(), div.shape)
			posicaoMenor = posicaoMenor + 1

			pivo = matrix[posicaoMenor][posicaoMaior]

			vb[posicaoMenor] = posicaoMaior

			if pivo != 1:
				matrix[posicaoMenor, :] = matrix[posicaoMenor, :] / pivo


			for i in range(numLinhas):
				if i != posicaoMenor:
					if matrix[i][posicaoMaior] != 0:
						#calcula todas as linhas
						matrix[i, :] = matrix[i, :] - matrix[i][posicaoMaior] * matrix[posicaoMenor, :]

			if self.s.noSolution(matrix):
				sys.exit(1)

			if self.s.optimalSolution(matrix):
				if self.s.multipleSolution(matrix):
					print "Problema possui múltiplas soluções..."
				else:
					print "Solucao única encontrada."

				if self.s.degenerada(matrix):
					print "Problema possui solução degenerada."

				x,z = self.s.mountSolution(matrix)

				print "\nQuadro ótimo:"
				print(matrix), "\n"
				print "X* = ", x
				print "Z* = ", z
			else:
				passo = passo + 1
				print "Tableu do passo: ", passo
				print np.matrix(matrix)
				print ""

		return matrix, x, z
