import sys

# TODO
# add basic file ops

debug = False
save_bytecode = False
arguments = ["--help", "-h", "--version", "-v", "--debug", "-d", "--save-bytecode", "-b"]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] not in arguments:
		infile = open(sys.argv[1])
	else:
		if sys.argv[1] == arguments[0] or sys.argv[1] == arguments[1]:
			print "MINIM INTERPRETER 1.1"
			print "Programmed by Draven Stedman"
			print "Copyleft 2014-2017 Draven Stedman"
			print "-----"
			print "Execute file: \"minim [file]\""
			print "For help: \"minim -h\" or \"minim --help\""
			print "For version: \"minim -v\" or \"minim --version\""
                        print "To turn debug mode on while interpreting: \"minim -d [file]\" or \"minim --debug [file]\""
                        print "To save bytecode: \"minim -b [file]\" or \"minim --save-bytecode [file]\""
			sys.exit()
		elif sys.argv[1] == arguments[2] or sys.argv[1] == arguments[3]:
			print "MINIM INTERPRETER"
			print "Version 1.1"
		elif sys.argv[1] == arguments[4] or sys.argv[1] == arguments[5]:
			debug = True
                        infile = open(sys.argv[2])
                elif sys.argv[1] == arguments[6] or sys.argv[1] == arguments [7]:
                        save_bytecode = True
                        infile = open(sys.argv[2])
                        bytecodefilename = sys.argv[2].split(".")[0] + ".mib"
		else:
			print "Invalid arguments: "+str(sys.argv[1])
    else:
        print "Error: no arguments"
        sys.exit()
else:
    sys.exit()

iil = []
iil_line = ""

lines = infile.readlines()
for i in lines:
	# check if comments or whitespace.
	if i.strip().startswith("//") or i.isspace():
		pass # just pass over that bizness
	elif i.strip().strip("\n").endswith("begin"):
		iil.append(i.strip().strip("\n") + "{") # Add the string plus a left bracket
	elif i.strip().strip("\n").endswith("stopf;") or i.strip().strip("\n").endswith("stopl;") or i.strip().strip("\n").endswith("stopif;"):
		blah = i.strip().strip("\n")
		blah = "} " + blah + ";"
		iil.append(blah.strip("\n"))
	elif i.strip().endswith(";") and not i.startswith("\t"):
		iil.append(i.strip("\n")+";")
	else:
		iil.append(i.strip(" \t\n"))
for i in iil:
	iil_line += i

if save_bytecode:
    open(bytecodefilename, "w").write(iil_line)

##############################################################################################################################

programme = iil_line.split(";;")
line = 0 

killed = False

functions = {}	# Functions are like this: functions["blah"] = {args = [], function = []}
		# Args get interpreted as local vars.
variables = {}	# Variables can be either global or local (if they're local they get destroyed as soon as the scope ends) and can be ints, floats, or strings.
		# Variable format: variables["var"] = {type = "string" or "int" or "float" or "bool", scope = "global" or "local", value = (whatever)}

def Interpret(codeline):
	global line
	global killed
	blah = codeline.split(" ")	
	if 'die' in codeline and not 'if' in codeline:
		killed = True
	if codeline.startswith("fn") or codeline.startswith("if") or codeline.startswith("goto"):
		if not codeline.startswith("goto"):
			x = codeline.split("{")[1].split(";")
			del x[len(x)-1]
		if codeline.startswith("fn"):
			# i put my thing down
			# flip it and reverse it
			stuff = codeline.split(" ")
			name = stuff[1][0:stuff[1].index("(")]
			# fn blah() {}
			functions[name] = {}
			functions[name]["args"] = stuff[1][stuff[1].index("(")+1:stuff[1].index(")")]
			functions[name]["calls"] = []
			for i in x:
				functions[name]["calls"].append(i)
		elif codeline.startswith("if"):
			xyzzy = codeline[codeline.index("(")+1:codeline.index(")")]
			if eval_expr(xyzzy):
				for i in x:
					if killed:
						break
						break
						sys.exit()	
					else:
						Interpret(i)
		elif codeline.startswith("goto"):
			line = int(codeline[5:])-1
		else:
			pass
	elif codeline.startswith("//"):
		pass # It's a comment bruh
	elif codeline.startswith("int") or codeline.startswith("float") or codeline.startswith("str") or codeline.startswith("bool"):
                if codeline.startswith("int"):
                    try:
                        variables[blah[1]] = {"datatype": 'int', 'scope': "global", "value": int(blah[3])}
                    except ValueError:
                        print "Type error on line "+str(line)+": Variable data type does not match data."
                        sys.exit()
                elif codeline.startswith("float"):
                    try:
                        variables[blah[1]] = {"datatype": 'float', 'scope': 'global', 'value': float(blah[3])}
                    except ValueError:
                        print "Type error on line "+str(line)+": Variable data type does not match data."
                        sys.exit()
                elif codeline.startswith("str"):
                    if "\"" in blah[3]:
                        variables[blah[1]] = {'datatype': 'str', 'scope': 'global', 'value': blah[3].strip("\"")}
                    else:
                        print "Type error on line "+str(line)+": Variable data type does not match data."
                        sys.exit()
                elif codeline.startswith("bool"):
                    if blah[3] == "TRUE" or blah[3] == "FALSE":
                        variables[blah[1]] = {'datatype': 'bool', 'scope': 'global', 'value': blah[3]}
                    else:
                        print "Type error on line "+str(line)+": Variable data type does not match data."
                        sys.exit()
                else:
                    # this shouldn't be able to happen so add an error in case it does
                    print "Error: Type check system fucked up. See lines 116-131 of MINIM interpreter source to find issue."
                    sys.exit()
	elif codeline.startswith("puts("):
		if "\"" in codeline:
			print codeline[codeline.index("(\"")+2:codeline.index("\")")]
		else:
			print variables[codeline[codeline.index("(")+1:codeline.index(")")]]['value']
	elif codeline.startswith("gets("):
		xyz = codeline[5:codeline.index(",")]
		zyx = codeline[codeline.index(",")+1:codeline.index(")")-1].lstrip("\" ")
		if xyz in variables:
			variables[xyz]['value'] = str(raw_input(zyx))
		else:
			variables[xyz] = {"value": str(raw_input(zyx)), "datatype": "str", 'scope': 'global'}
	elif "(" in codeline:
		if codeline[0:codeline.index("(")] in functions:
			for i in functions[codeline[0:codeline.index("(")]]["calls"]:
				Interpret(i)
		else:
			pass
	elif blah[0] in variables:
		if blah[1] == "=":
			variables[blah[0]]["value"] = blah[2]
		elif blah[1] == "+=":
			if variables[blah[0]]['datatype'] == "float":
				variables[blah[0]]["value"] = float(variables[blah[0]]["value"]) + float(blah[2])
			elif variables[blah[0]]['datatype'] == "int":
				variables[blah[0]]["value"] = int(variables[blah[0]]["value"]) + int(blah[2])
			elif variables[blah[0]]['datatype'] == "str":
				variables[blah[0]]["value"] = str(variables[blah[0]]["value"]) + str(blah[2])
			else:
				pass
		elif blah[1] == "-=":
			if variables[blah[0]]['datatype'] == "float":
				variables[blah[0]]["value"] = float(variables[blah[0]]["value"]) - float(blah[2])
			elif variables[blah[0]]['datatype'] == "int":
				variables[blah[0]]["value"] = int(variables[blah[0]]["value"]) - int(blah[2])
			elif variables[blah[0]]['datatype'] == "str":
				print "Syntax error: can't subtract from strings"
				exit(1)
			else:
				pass
		elif blah[1] == "*=":
			if variables[blah[0]]['datatype'] == "float":
				variables[blah[0]]["value"] = float(variables[blah[0]]["value"]) * float(blah[2])
			elif variables[blah[0]]['datatype'] == "int":
				variables[blah[0]]["value"] = int(variables[blah[0]]["value"]) * int(blah[2])
			elif variables[blah[0]]['datatype'] == "str":
				print "Syntax error: can't multiply strings"
				exit(1)
			else:
				pass
		elif blah[1] == "/=":
			if variables[blah[0]]['datatype'] == "float":
				variables[blah[0]]["value"] = float(variables[blah[0]]["value"]) / float(blah[2])
			elif variables[blah[0]]['datatype'] == "int":
				variables[blah[0]]["value"] = str(variables[blah[0]]["value"]) / str(blah[2])
			elif variables[blah[0]]['datatype'] == "str":
				print "Syntax error: can't divide strings"
				exit(1)
			else:
				pass
		elif blah[1] == "%=":
			if variables[blah[0]]['datatype'] == "float":
				variables[blah[0]]["value"] = float(variables[blah[0]]["value"]) % float(blah[2])
			elif variables[blah[0]]['datatype'] == "int":
				variables[blah[0]]["value"] = int(variables[blah[0]]["value"]) % int(blah[2])
			elif variables[blah[0]]['datatype'] == "str":
				print "Syntax error: can't modulo strings"
				exit(1)
			else:
				pass
		else:
				pass
        elif codeline.startswith("file"):
            # This means the code here is dealing with files obv
            if codeline.startswith("filewrite"):
                # File writing handler
            elif codeline.startswith("fileread"):
                # File reading handler
            elif codeline.startswith("fileappend"):
                # File append handler
            else:
                print "Error: either it's not a thing or it's not implemented, see todo/changelog."
                sys.exit()
        else:
		pass

def eval_expr(expression):
	expr_tokenised = expression.split(" ")
	if debug:
		print expr_tokenised
		if len(expr_tokenised) > 1:
			if expr_tokenised[0] in variables:
				print variables[expr_tokenised[0]]['value']
			else:
				pass
			if expr_tokenised[2] in variables:
				print variables[expr_tokenised[2]]['value']
			else:
				pass
		else:
			print "True"
	else:
		pass
	if len(expr_tokenised) > 1:
		if "and" in expr_tokenised:
			# TODO: evaluate multiple expressions.
			return eval_expr(expression.split(" and ")[0]) and eval_expr(expression.split(" and ")[1])
		elif "or" in expr_tokenised:
			# TODO: evaluate multiple expr.
			return eval_expr(expression.split(" or ")[0]) or eval_expr(expression.split(" or ")[1])
		elif "xor" in expr_tokenised:
			return eval_expr(expression.split(" xor ")[0]) ^ eval_expr(expression.split(" xor ")[1])
		if expr_tokenised[1] == "==":
			if expr_tokenised[0] in variables:
				if expr_tokenised[2] in variables:
					if variables[expr_tokenised[0]]['value'] == variables[expr_tokenised[2]]["value"]:
						return True
					else:
						return False
				else:
					if variables[expr_tokenised[0]] == expr_tokenised[2].strip("\""):
						return True
					else:
						return False
			else:
				return expr_tokenised[0].strip("\"") == expr_tokenised[2].strip("\"")
		elif expr_tokenised[1] == ">":
			if expr_tokenised[0] in variables:
				if expr_tokenised[2] in variables:
					if variables[expr_tokenised[0]]['datatype'] in ["int","float"] and variables[expr_tokenised[2]]['datatype'] in ["int","float"]:
						if variables[expr_tokenised[0]]['datatype'] == "int":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return int(variables[expr_tokenised[0]]["value"]) > float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return int(variables[expr_tokenised[0]]["value"]) > int(variables[expr_tokenised[2]]["value"])
						elif variables[expr_tokenised[0]]['datatype'] == "float":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return float(variables[expr_tokenised[0]]["value"]) > float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return float(variables[expr_tokenised[0]]["value"]) > int(variables[expr_tokenised[2]]["value"])
				else:
					if variables[expr_tokenised[0]]['datatype'] == "int":
						return int(variables[expr_tokenised[0]]["value"]) > int(expr_tokenised[2])
					elif variables[expr_tokenised[0]]['datatype'] == 'float':
						return float(variables[expr_tokenised[0]]["value"]) > float(expr_tokenised[2])
					else:
						print "Syntax error: given comparison non-computable"
						exit(1)
			else:
				return float(expr_tokenised[0]) > float(expr_tokenised[2])
		elif expr_tokenised[1] == "<":
			if expr_tokenised[0] in variables:
				if expr_tokenised[2] in variables:
					if variables[expr_tokenised[0]]['datatype'] in ["int","float"] and variables[expr_tokenised[2]]['datatype'] in ["int","float"]:
						if variables[expr_tokenised[0]]['datatype'] == "int":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return int(variables[expr_tokenised[0]]["value"]) < float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return int(variables[expr_tokenised[0]]["value"]) < int(variables[expr_tokenised[2]]["value"])
						elif variables[expr_tokenised[0]]['datatype'] == "float":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return float(variables[expr_tokenised[0]]["value"]) < float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return float(variables[expr_tokenised[0]]["value"]) < int(variables[expr_tokenised[2]]["value"])
				else:
					if variables[expr_tokenised[0]]['datatype'] == "int":
						return int(variables[expr_tokenised[0]]['value']) < int(expr_tokenised[2])
					elif variables[expr_tokenised[0]]['datatype'] == 'float':
						return float(variables[expr_tokenised[0]]["value"]) < float(expr_tokenised[2])
					else:
						print "Syntax error: given comparison non-computable"
						exit(1)
			else:
				return float(expr_tokenised[0]) < float(expr_tokenised[2])
		elif expr_tokenised[1] == "<=":
			if expr_tokenised[0] in variables:
				if expr_tokenised[2] in variables:
					if variables[expr_tokenised[0]]['datatype'] in ["int","float"] and variables[expr_tokenised[2]]['datatype'] in ["int","float"]:
						if variables[expr_tokenised[0]]['datatype'] == "int":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return int(variables[expr_tokenised[0]]["value"]) <= float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return int(variables[expr_tokenised[0]]["value"]) <= int(variables[expr_tokenised[2]]["value"])
						elif variables[expr_tokenised[0]]['datatype'] == "float":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return float(variables[expr_tokenised[0]]["value"]) <= float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return float(variables[expr_tokenised[0]]["value"]) <= int(variables[expr_tokenised[2]]["value"])
				else:
					if variables[expr_tokenised[0]]['datatype'] == "int":
						return int(variables[expr_tokenised[0]]["value"]) <= int(expr_tokenised[2])
					elif variables[expr_tokenised[0]]['datatype'] == 'float':
						return float(variables[expr_tokenised[0]]["value"]) <= float(expr_tokenised[2])
					else:
						print "Syntax error: given comparison non-computable"
						exit(1)
			else:
				return float(expr_tokenised[0]) <= float(expr_tokenised[2])
		elif expr_tokenised[1] == ">=":
			if expr_tokenised[0] in variables:
				if expr_tokenised[2] in variables:
					if variables[expr_tokenised[0]]['datatype'] in ["int","float"] and variables[expr_tokenised[2]]['datatype'] in ["int","float"]:
						if variables[expr_tokenised[0]]['datatype'] == "int":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return int(variables[expr_tokenised[0]]["value"]) >= float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return int(variables[expr_tokenised[0]]["value"]) >= int(variables[expr_tokenised[2]]["value"])
						elif variables[expr_tokenised[0]]['datatype'] == "float":
							if variables[expr_tokenised[2]]['datatype'] == "float":
								return float(variables[expr_tokenised[0]]["value"]) >= float(variables[expr_tokenised[2]]["value"])
							elif variables[expr_tokenised[2]]['datatype'] == "int":
								return float(variables[expr_tokenised[0]]["value"]) >= int(variables[expr_tokenised[2]]["value"])
				else:
					if variables[expr_tokenised[0]]['datatype'] == "int":
						return int(variables[expr_tokenised[0]]["value"]) >= int(expr_tokenised[2])
					elif variables[expr_tokenised[0]]['datatype'] == 'float':
						return float(variables[expr_tokenised[0]]["value"]) >= float(expr_tokenised[2])
					else:
						print "Syntax error: given comparison non-computable"
						exit(1)
			else:
				return float(expr_tokenised[0]) >= float(expr_tokenised[2])
		elif expr_tokenised[1] == "!=":
			if expr_tokenised[0] in variables:
				if expr_tokenised[2] in variables:
					if variables[expr_tokenised[0]]['value'] == variables[expr_tokenised[2]]["value"]:
						return False
					else:
						return True
				else:
					if variables[expr_tokenised[0]] == expr_tokenised[2].strip("\""):
						return False
					else:
						return True
			else:
				return expr_tokenised[0].strip("\"") != expr_tokenised[2].strip("\"")
		else:
			pass
	else:
		if expr_tokenised[0] == "true" or expr_tokenised[0] == "1":
			return True
		elif expr_tokenised[0] == "false" or expr_tokenised[0] == "0":
			return False
		else:
			pass

while line < len(programme):
	if killed:
		break
		sys.exit()
	else:
		Interpret(programme[line])
		line += 1

if debug:
	print "DEBUG INFORMATION"
	print variables
	print functions
