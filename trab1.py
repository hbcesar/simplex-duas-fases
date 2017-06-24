# -*- coding: utf-8 -*-
import sys
import os.path
import numpy as np
from solution import Solution
from metodoSimplex import MetodoSimplex

def main(argv):
	filename = raw_input('Digite o Nome do Arquivo com a Matriz de Entrada: ')

	if not os.path.exists(filename):
		print('Arquivo inválido.\nAbortando')
		sys.exit(1)

	matrix = []

	matrix = np.loadtxt(filename, delimiter = " ", skiprows = 2)

	#pega o ultimo da lista
	#apaga o ultimo da lista
	#adiciona no começo
	newmatrix = []
	for row in matrix:
		last = row[-1]
		row = np.delete(row, -1)
		row = np.insert(row, 0, last)
		newmatrix.append(row)

	matrix = np.array(newmatrix)
	vb = np.zeros(len(matrix))

	#cria classe MetodoSimplex
	simplex = MetodoSimplex(matrix)

	#verifica no arquivo de entrada se é duas fases ou nao
	with open(filename, 'r') as f:
		fases = f.readline().rstrip()

	#executa duas fases
	if fases == "2":
		matrix[0,:] = (-1) * matrix[0,:]
		matrix[1,:] = (-1) * matrix[1,:]
		matrix, count, vb = simplex.primeiraFase(matrix, vb)

		print('\nFim da primeira fase\n')
		print "Za:", matrix[0], "\n"
		print "Iniciando Segunda fase:"

		matrix, x, z = simplex.simplex(matrix, vb)

	#executa apenas uma fase	
	elif fases == "1":
		print "Iniciando simplex..."
		matrix[0,:] = (-1) * matrix[0,:]
		matrix, x, z = simplex.simplex(matrix, vb)

	else:
		print('Opção inválida')



if __name__ == '__main__':
	main(sys.argv)
