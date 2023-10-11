import sys

# NFA structure, doesn't hold alhpabet or state sets because we don't need to output them
class NFA:
	# NFA's will take three arguments, states being integers
	def __init__(self, transitions, start_state, accept_state):
		# list of transitions (of the form [state1, "symbol", state2])
		self.transitions = transitions
		# the start state of the machine
		self.start_state = start_state
		# all NFAs must have one accept state
		self.accept_state = accept_state

	# outputs the NFAs attributes to stdout
	def print(self):
		# first print start and accept states
		print("Start: q" + str(self.start_state))
		print("Accept: q" + str(self.accept_state))

		# print all transitions in the form (qX, S) -> qY
		for transition in self.transitions:
			start = str(transition[0])
			symbol = str(transition[1])
			end = str(transition[2])
			print("(q" + start + ", " + symbol + ") -> q" + end)

	# unions this NFA with NFA2 (added states will have id starting at curr_state_id)
	def union(self, NFA2, curr_state_id):
		# add transitions from new start state to old start states
		transition1 = [curr_state_id, "E", self.start_state]
		transition2 = [curr_state_id, "E", NFA2.start_state]

		# add exiting transitions from old accept states to new accept state
		transition3 = [self.accept_state, "E", curr_state_id + 1]
		transition4 = [NFA2.accept_state, "E", curr_state_id + 1]

		# add transitions in a specific way to keep transitions array sorted
		self.transitions.append(transition3)
		self.transitions.extend(NFA2.transitions)
		self.transitions.append(transition4)
		self.transitions.append(transition1)
		self.transitions.append(transition2)

		# change start and accept states
		self.accept_state = curr_state_id + 1
		self.start_state = curr_state_id
		return self

	def concat(self, NFA2):
		# add transition from self to NFA2 start state
		self.transitions.append([self.accept_state, "E", NFA2.start_state])

		# add all of NFA2s transitions to self
		self.transitions.extend(NFA2.transitions)

		# change accept state to NFA2 accept state
		self.accept_state = NFA2.accept_state
		return self

	def star(self, curr_state_id):
		# add transitions from new start to start, and accept to new start
		self.transitions.append([self.accept_state, "E", curr_state_id])
		self.transitions.append([curr_state_id, "E", self.start_state])

		# udpate start and accept states
		self.start_state = curr_state_id
		self.accept_state = curr_state_id
		return self

input_file = None

# try to open input file, if failed, then exit
try:
	input_file = open(sys.argv[1], "r")
except FileNotFoundError:
	print("Error: must recieve input file")
	exit()

# all the valid non-operator characters the regex can contain
letters = ["a", "b", "c", "d", "e"]

for line in input_file:
	regex = line[:-1]
	curr_state_id = 1
	NFAs = []
	failed = False
	for char in regex:
		if char in letters:
			# if the character is in the alphabet, append a simple NFA just recognizing that character
			transitions = [[curr_state_id, char, curr_state_id + 1]]
			NFAs.append(NFA(transitions, curr_state_id, curr_state_id + 1))
			curr_state_id += 2
		elif char == "|":
			# error check the array for malformed input
			if len(NFAs) < 2:
				print("Error: Malformed Regular Expression: " + regex)
				failed = True
				break
			# union the two most recent NFAs in the array
			NFA1 = NFAs.pop()
			NFA2 = NFAs.pop()
			NFA2.union(NFA1, curr_state_id)
			NFAs.append(NFA2)
			curr_state_id += 2
		elif char == "&":
			# error check the array for malformed input
			if len(NFAs) < 2:
				print("Error: Malformed Regular Expression: " + regex)
				failed = True
				break
			# concat the two most recent NFAs in the array
			NFA1 = NFAs.pop()
			NFA2 = NFAs.pop()
			NFA2.concat(NFA1)
			NFAs.append(NFA2)
		elif char == "*":
			# error check the array for malformed input
			if(len(NFAs) < 1):
				print("Error: Malformed Regular Expression: " + regex)
				failed = True
				break
			# star the most recent NFA in the array
			NFA1 = NFAs.pop()
			NFA1.star(curr_state_id)
			NFAs.append(NFA1)
			curr_state_id += 1
		else:
			# the regex contains an unrecognizable character
			print("Error: unrecognized character: " + char + " in regular expression: " + regex)
			failed = True
			break
	if failed:
		print("\n", end="")
		continue
	elif len(NFAs) != 1:
		# one last error check for malformed input (happens when there are stray characters at end of regex)
		print("Error: Malformed Regular Expression: " + regex)
		print("\n", end="")
		continue
	# print the final NFA and its cooresponding regular expression
	final_NFA = NFAs.pop()
	print("RE: " + regex)
	final_NFA.print()
	print("\n", end="")