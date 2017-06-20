# -*- coding: utf-8 -*-
import sys
import math
import numpy as np
from solution import Solution

class MetodoSimplex(object):
	def __init__(self, matrix):
		self.s = Solution(matrix)

	#verifica se primeira fase chegou ao fimPrimFase
	def endFistPhase(self, matrix, zArtif):
		if all(i <= 0 for i in matrix[0,1:]):
			if np.array_equal(matrix[0,:],zArtif):
				return True

			if matrix[0][0] == 0:
				return False
			else:
				return -2

	def primeiraFase(self, matrix, vb):
		print "\nIniciando primeira fase:"
		print ""

		print "Tableau inicial:"
		print np.matrix(matrix)
		print ""

		numLinhas = len(matrix)
		numColunas = len(matrix[0])

		zArt = matrix[0]
		count = 0
		output = True
		passo = 0

		for i in range(numColunas):
			if zArt[i] < 0:
				count += 1

		for i in range(1, numColunas):
			if self.s.artificial(matrix[:,i].transpose()):
				posicao, = np.unravel_index(matrix[:, i].argmax(), matrix[:, i].shape)
				matrix[0,:] = matrix[0,:] + matrix[posicao,:]

		print "Quadro Tableau"
		print np.matrix(matrix)
		print ""

		while not self.endFistPhase(matrix, zArt):
			output = self.endFistPhase(matrix, zArt)
			posicaoMaior, = np.unravel_index(matrix[0, 1:].argmax(), matrix[0, 1:].shape)
			posicaoMaior = posicaoMaior + 1 #precisa incrementar, visto que retorna a posicao relativa ao slice

			#cria um vetor para armazenar divisoes
			div = np.zeros(numLinhas - 2)

			for i in range(2, numLinhas):
				if matrix[i][posicaoMaior] > 0:
					div[i-2] = matrix[i][0] / matrix[i][posicaoMaior]

			#Procura menor divisao e guarda linha
			max = float("inf")
			posicaoMenor = 0
			for i in range(len(div)):
				if div[i] > 0 and div[i] < max:
					max = div[i]
					posicaoMenor = i
			posicaoMenor = posicaoMenor + 2
			
			pivo = matrix[posicaoMenor][posicaoMaior]

			vb[posicaoMenor] = posicaoMaior

			if pivo != 1:
				matrix[posicaoMenor, :] = matrix[posicaoMenor, :] / pivo #no codigo da Ana tem um ponto, ve o que means

			for i in range(len(matrix)):
				if i != posicaoMenor:
					if matrix[i][posicaoMaior] != 0:
						#calcula linhas
						#TODO: rever como faz o :
						matrix[i, :] = matrix[i, :] - matrix[i][posicaoMaior] * matrix[posicaoMenor, :]

			passo = passo + 1
			print "\nTableau - Primeira fase - Passo: ", passo
			print matrix

		if self.endFistPhase(matrix, zArt) == -2:
			output = -2
			print "Conjunto de soluções é vazio"

		return matrix, count, vb, output


	def simplex(self, matrix, vb):
		print "Iniciando simplex"
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

			div = np.zeros(numLinhas)

			for i in range(1, numLinhas):
				if matrix[i][posicaoMaior] > 0:
					div[i-1] = matrix[i][0] / matrix[i][posicaoMaior]

			#Procura o menor da divisao e guarda linhas
			max = float("inf")
			posicaoMenor = 0
			for i in range(len(div)):
				if div[i] > 0 and div[i] < max:
					max = div[i]
					posicaoMenor = i
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
				print "Tableau fornecido não possui solução viável. \nAbortando."
				return False

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
	
