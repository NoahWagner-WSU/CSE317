import sys

#NOTE: I don't need to store alphabet since NFA output doesn't include alphabet
class NFA:
	def __init__(states, transitions, start_state, accept_states):
		self.states = states
		self.transitions = transitions
		self.start_state = start_state
		self.accept_states = accept_states

	#outputs NFA to stdout in structured way (like in specification files)
	def print():

	def union(NFA2, curr_state_id):
		transition1 = [curr_state_id, "E", self.start_state]
		transition2 = [curr_state_id, "E", NFA2.start_state]
		self.transitions.extend(NFA2.transitions)
		self.transitions.append(transition1)
		self.transitions.append(transition2)
		self.states.extend(NFA2.states)
		self.states.append(curr_state_id)
		self.accept_states.extend(NFA2.accept_states)
		self.start_state = curr_state_id
		return self

	def concat(NFA2):
		transitions = []
		for accept_state in self.accept_states:
			transitions.append([accept_state, "E", NFA2.start_state])
		self.transitions.extend(transitions)
		self.transitions.extend(NFA2.transitions)
		self.states.extend(NFA2.states)
		self.accept_states = NFA2.accept_states
		return self

	def star(curr_state_id):
		self.states.append(curr_state_id)
		transitions = []
		for accept_state in self.accept_states:
			transitions.append([accept_state, "E", self.start_state])
		self.transitions.extend(transitions)
		self.start_state = curr_state_id
		self.accept_states.append(curr_state_id)
		return self

input_file = open(sys.argv[1], "r")

for line in input_file:
	regex = line
	curr_state_id = 1
	NFAs = []
	for char in regex:
		# if alphabet char, make NFA that recognizes that char
			# add NFA to temp array
		# if | operator, pop two NFA's from array and call union(NFA1, NFA2)
			# add that NFA to temp array
		# if & operator, pop two NFA's from array and call concat(NFA1, NFA2)
			# add that NFA to temp array
		# if * operator, pop NFA from array and call star(NFA1)
			# add that NFA to temp array
		# else quit program and return error (if "\n" don't do anything)

		#NOTE: if we cannot pop 2 or 1 NFA's from array because there is less than that many, return error
			# 1 if * and 2 for | and & operations

	# print regex, start state, accept states, and NFA in specified format