import sys

class NFA:
	def __init__(self, transitions, start_state, accept_state):
		self.transitions = transitions
		self.start_state = start_state
		self.accept_state = accept_state

	def print(self):
		print("Start: q" + str(self.start_state))
		print("Accept: q" + str(self.accept_state))
		for transition in self.transitions:
			start = str(transition[0])
			symbol = str(transition[1])
			end = str(transition[2])
			print("(q" + start + ", " + symbol + ") -> q" + end)

	def union(self, NFA2, curr_state_id):
		transition1 = [curr_state_id, "E", self.start_state]
		transition2 = [curr_state_id, "E", NFA2.start_state]
		transition3 = [self.accept_state, "E", curr_state_id + 1]
		transition4 = [NFA2.accept_state, "E", curr_state_id + 1]
		self.transitions.append(transition3)
		self.transitions.extend(NFA2.transitions)
		self.transitions.append(transition4)
		self.transitions.append(transition1)
		self.transitions.append(transition2)
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
	regex = line[:-1]
	curr_state_id = 1
	NFAs = []
	failed = False
	for char in regex:
		if char in letters:
			transitions = [[curr_state_id, char, curr_state_id + 1]]
			NFAs.append(NFA(transitions, curr_state_id, curr_state_id + 1))
			curr_state_id += 2
		elif char == "|":
			if len(NFAs) < 2:
				print("Error: Malformed Regular Expression: " + regex)
				failed = True
				break
			NFA1 = NFAs.pop()
			NFA2 = NFAs.pop()
			NFA2.union(NFA1, curr_state_id)
			NFAs.append(NFA2)
			curr_state_id += 2
		elif char == "&":
			if len(NFAs) < 2:
				print("Error: Malformed Regular Expression: " + regex)
				failed = True
				break
			NFA1 = NFAs.pop()
			NFA2 = NFAs.pop()
			NFA2.concat(NFA1)
			NFAs.append(NFA2)
		elif char == "*":
			if(len(NFAs) < 1):
				print("Error: Malformed Regular Expression: " + regex)
				failed = True
				break
			NFA1 = NFAs.pop()
			NFA1.star(curr_state_id)
			NFAs.append(NFA1)
			curr_state_id += 1
		else:
			print("Error: unrecognized character: " + char + " in regular expression: " + regex)
			failed = True
			break
	if failed:
		print("\n", end="")
		continue
	elif len(NFAs) != 1:
		print("Error: Malformed Regular Expression: " + regex)
		print("\n", end="")
		continue
	final_NFA = NFAs.pop()
	print("RE: " + regex)
	final_NFA.print()
	print("\n", end="")