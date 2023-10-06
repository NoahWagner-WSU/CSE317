import sys

class NFA:
	def __init__(states, alphabet, transition_func, start_state, accept_states):
		self.states = states
		self.alphabet = alphabet
		self.transition_func = transition_func
		self.accept_states = accept_states

	#outputs NFA to stdout in structured way (like in specification files)
	def print():


	# each method returns a new NFA
	@staticmethod
	def union(NFA1, NFA2):

	@staticmethod
	def concat(NFA1, NFA2):

	@staticmethod
	def star(NFA1):

input_file = open(sys.argv[1], "r")

for regex in input_file:
	for char in regex
		# if alphabet char, make NFA that recognizes that char
			# add NFA to temp array
		# if | operator, pop two NFA's from array and call union(NFA1, NFA2)
			# add that NFA to temp array
		# if & operator, pop two NFA's from array and call concat(NFA1, NFA2)
			# add that NFA to temp array
		# if * operator, pop NFA from array and call star(NFA1)
			# add that NFA to temp array
		# else quit program and return error

		#NOTE: if we cannot pop 2 or 1 NFA's from array because there is less than that many, return error
			# 1 if * and 2 for | and & operations
