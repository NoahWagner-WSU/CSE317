import sys

#NOTE: I don't need to store alphabet or states since NFA output doesn't include them
class NFA:
	def __init__(self, transitions, start_state, accept_state):
		self.transitions = transitions
		self.start_state = start_state
		self.accept_state = accept_state

	#outputs NFA to stdout in structured way (like in specification files)
	# def print():

	def union(self, NFA2, curr_state_id):
		transition1 = [curr_state_id, "E", self.start_state]
		transition2 = [curr_state_id, "E", NFA2.start_state]
		transition3 = [self.accept_state, "E", curr_state_id + 1]
		transition4 = [NFA2.accept_state, "E", curr_state_id + 1]
		self.transitions.extend(NFA2.transitions)
		self.transitions.append(transition1)
		self.transitions.append(transition2)
		self.transitions.append(transition3)
		self.transitions.append(transition4)
		self.accept_state = curr_state_id + 1
		self.start_state = curr_state_id
		return self

	def concat(self, NFA2):
		self.transitions.append([self.accept_state, "E", NFA2.start_state])
		self.transitions.extend(NFA2.transitions)
		self.accept_state = NFA2.accept_state
		return self

	def star(self, curr_state_id):
		self.transitions.append([self.accept_state, "E", curr_state_id])
		self.transitions.append([curr_state_id, "E", self.start_state])
		self.start_state = curr_state_id
		self.accept_state = curr_state_id
		return self

input_file = open(sys.argv[1], "r")

letters = ["a", "b", "c", "d", "e"]

for line in input_file:
	regex = line
	curr_state_id = 1
	NFAs = []
	for char in regex:
		if char in letters:
			transitions = [[curr_state_id, char, curr_state_id + 1]]
			NFAs.append(NFA(transitions, curr_state_id, curr_state_id + 1))
			curr_state_id += 2
		elif char == "|":
			if len(NFAs) < 2:
				print("Error: Malformed Input")
				exit()
			NFA1 = NFAs.pop()
			NFA2 = NFAs.pop()
			NFA1.union(NFA2, curr_state_id)
			NFAs.append(NFA1)
			curr_state_id += 2
		elif char == "&":
			if len(NFAs) < 2:
				print("Error: Malformed Input")
				exit()
			NFA1 = NFAs.pop()
			NFA2 = NFAs.pop()
			NFA2.concat(NFA1)
			NFAs.append(NFA2)
		elif char == "*":
			if(len(NFAs) < 1):
				print("Error: Malformed Input")
				exit()
			NFA1 = NFAs.pop()
			NFA1.star(curr_state_id)
			NFAs.append(NFA1)
			curr_state_id += 1
		elif char != "\n":
			print("Error: unrecognized character: " + char)
			exit()
	# print regex, start state, accept states, and NFA in specified format
	final_NFA = NFAs.pop()
	print("___TRANSITIONS___")
	print(final_NFA.transitions)
	print("___START_STATE___")
	print(final_NFA.start_state)
	print("___ACCEPT_STATES___")
	print(final_NFA.accept_state)