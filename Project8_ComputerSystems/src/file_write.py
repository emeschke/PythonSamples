__author__ = 'E'

#This is a dictionary that holds all the possible combos for the C_ARITHMETIC commands.
C_ARITHMETIC = {"add": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"],
                "sub": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D"],
                "neg": ["D=0", "@SP", "A=M-1", "M=D-M"],
                "eq": ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "@FALSE", "D;JNE", "@SP", "A=M-1","M=-1", "@CONTINUE",
                       "0;JMP", "(FALSE)", "@SP", "A=M-1", "M=0", "(CONTINUE)"],
                "gt": ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "@FALSE", "D;JLE", "@SP", "A=M-1","M=-1", "@CONTINUE",
                       "0;JMP", "(FALSE)", "@SP", "A=M-1", "M=0", "(CONTINUE)"],
                "lt": ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "@FALSE", "D;JGE", "@SP", "A=M-1","M=-1", "@CONTINUE",
                       "0;JMP", "(FALSE)", "@SP", "A=M-1", "M=0", "(CONTINUE)"],
                "and": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M"],
                "or": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M"],
                "not": ["@SP", "A=M-1", "M=!M"]
                }
#This is a dictionary that holds all the input arguments for push and pop, except static (which is simple and push only)
C_PUSHPOP = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", "pointer": 3, "temp": 5}

#Global counter to keep track of how many time C_ARITHMETIC statements with jumps are written.
#Is it a bad idea to have this global?
counter = 0
func_counter = 0

#Write the initialization routine for the file.
def write_init(output):
    bootstrap =  ["@256", "D=A", "@0", "M=D", "@Sys.vm.Sys.init", "0;JMP"]
    try:
        with open(output, "a") as outputFile:
            print "File " + output + " opened successfully."
            #Loop over the content (a list of parsed lines representing commands)
            for i in bootstrap:
                    outputFile.writelines(i + "\n")
    except IOError:
        #If it couldn't print to output, exit.
        print "Couldn't open output file."
        return 1


#A function to write open the file, loop through the content, translate it to VM code and write to the output file.
def write_to_file(filename, content, output):
    try:
        with open(output, "a") as outputFile:
            print "File " + output + " opened successfully."
            #Loop over the content (a list of parsed lines representing commands)
            for i in content:
                #Get the translated set of commands for each input line as a list and write to file.
                for j in translate(i, filename):
                    outputFile.writelines(j + "\n")

    except IOError:
        #If it couldn't print to output, exit.
        print "Couldn't open output file."
        return 1


def translate(i, filename):
    #translate function takes the input list and a filename (necessary for static) and routes to the right sub-function
    if i[0] == "push":
        return push(i, filename)
    elif i[0] == "pop":
        return pop(i, filename)
    elif i[0] in C_ARITHMETIC:
        return arith(i)
    elif i[0] == "label":
        return label(i, filename)
    elif i[0] == "goto":
        return goto(i, filename)
    elif i[0] == "if-goto":
        return ifgoto(i, filename)
    elif i[0] == "function":
        return func(i, filename)
    elif i[0] == "call":
        return call(i, filename)
    elif i[0] == "return":
        return ret(i)


#Returns the code for the push command, routes to the switches based on argument 1; returns proper code for push
def push(i, filename):
    if i[1] == "constant":
        #Constant address value is substituted in.
        value = "@"+i[2]
        return [value, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    elif i[1] in ("local", "argument", "this", "that"):
        #Correct mnemonic is substituted using dictionary lookup; offset is concatentated from @ and input 2.
        place1 = "@" + C_PUSHPOP[i[1]]
        place2 = "@" + str(i[2])
        return[place1, "D=M", place2, "A=D+A", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    elif i[1] in ("pointer", "temp"):
        #Dictionary returns a string that is base of pointer/temp.  Offset is added to that and hardcoded.
        place = "@" + str(int(i[2]) + C_PUSHPOP[i[1]])
        return[place, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    elif i[1] == "static":
        #String is constructed from the filename.offset and hardcoded in instruction list.
        place = "@" + filename + "." + str(i[2])
        return [place, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

#Returns the code for the pop command.
def pop(i, filename):
    #Correct mnemonic is substituted using dictionary lookup; offset is concatentated from @ and input 2.
    if i[1] in ("local", "argument", "this", "that"):
        place1 = "@" + C_PUSHPOP[i[1]]
        place2 = "@" + str(i[2])
        return[place1, "D=M", place2, "D=D+A", "@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]
    elif i[1] in ("pointer", "temp"):
        #Dictionary returns a string that is base of pointer/temp.  Offset is added to that and hardcoded.
        place = "@" + str(int(i[2]) + C_PUSHPOP[i[1]])
        return["@SP", "AM=M-1", "D=M", place, "M=D"]
    elif i[1] == "static":
        #String is constructed from the filename.offset and hardcoded in instruction list.
        place = "@" + filename + "." + str(i[2])
        return ["@SP", "AM=M-1", "D=M", place, "M=D"]

#Returns the code for the different arithmetic commands.
def arith(i):
    #Call to the global counter function.  This will set the proper positioning for (CONTINUE) format lines.
    global counter
    #(FALSE) and (CONTINUE) need to be differentiated by specific line, so they the counter is appended to them each
    #time the program runs.  If a jmp statement is called, it increments the global counter.
    fal = "FALSE" + str(counter)
    cont = "CONTINUE" + str(counter)
    #If not a statement requiring a jump, look up translation in dictionary.
    if i[0] not in ('eq', 'gt', 'lt'):
        return C_ARITHMETIC[i[0]]
    #Else branches to cover jump syntax, substitutes in the counter appended FALSE and CONTINUE statements.
    elif i[0] == 'eq':
        counter +=1
        return ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "@"+fal, "D;JNE", "@SP", "A=M-1","M=-1", "@"+cont,
                "0;JMP", "("+fal+")", "@SP", "A=M-1", "M=0", "("+cont+")"]
    elif i[0] == 'gt':
        counter +=1
        return ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "@"+fal, "D;JLE", "@SP", "A=M-1","M=-1", "@"+cont,
                       "0;JMP", "("+fal+")", "@SP", "A=M-1", "M=0", "("+cont+")"]
    elif i[0] == 'lt':
        counter +=1
        return ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "@"+fal, "D;JGE", "@SP", "A=M-1","M=-1", "@"+cont,
                       "0;JMP", "("+fal+")", "@SP", "A=M-1", "M=0", "("+cont+")"]

#Returns the code for a label.
def label(i, filename):
    return ["(" + filename + "." + i[1] + ")"]

#Returns the code for a goto
def goto(i, filename):
    return ["@" + filename + "." + i[1], "0;JMP"]

#Returns the code for an if-goto
def ifgoto(i, filename):
    return ["@SP", "AM=M-1", "D=M", "@" + filename + "." + i[1], "D;JNE"]

#Returns the code for a function declaration.
def func(i, filename):
    return ["(" + filename + "." + i[1] + ")", "@" + i[2], "D=A", "@SP", "M=M+D", "@" + i[2], "D=A-1",
            "(" + filename + "." + i[1] + "_set" + ")", "@" + "END_" + filename + "." + i[1], "D;JLT", "@LCL",
            "A=D+M", "M=0", "D=D-1", "@" + filename + "." + i[1] + "_set", "0;JMP",
            "(END_" + filename + "." + i[1] + ")"]

#Returns the code for a function call.
def call(i, filename):
    global func_counter
    return_address = filename + "." + i[1] + "." + str(func_counter)
    #These variables concatenate the name for the function call and the return address.
    #The return address must be unique for each time the function is called.
    file_call = filename + "." + i[1]
    func_counter += 1
    return ["@"+ return_address, "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
            "@SP", "D=M", "@" + str(i[2]), "D=D-A", "@5", "D=D-A", "@ARG", "M=D",
            "@SP", "D=M", "@LCL", "M=D", "@" + file_call, "0;JMP", "(" + return_address + ")"]

#Returns the code for the return keyword.
def ret(i):
    return ["@LCL", "D=M", "@R13", "M=D", "@5", "D=A", "@LCL", "A=M-D", "D=M", "@R14", "M=D", "@SP", "A=M-1", "D=M",
            "@ARG", "A=M", "M=D", "D=A", "@SP", "M=D+1", "@R13", "AM=M-1", "D=M", "@THAT", "M=D", "@R13", "AM=M-1",
            "D=M", "@THIS", "M=D", "@R13", "AM=M-1", "D=M", "@ARG", "M=D", "@R13", "AM=M-1", "D=M", "@LCL", "M=D",
            "@R14", "A=M", "0;JMP"]

