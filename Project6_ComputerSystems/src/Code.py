__author__ = 'E'
import Parser
#Reads in a list length five representing the output of Parser function commandType, symbol, comp, dest, jump.
#Dictionaries are declared for the different possibilities that are possible for c-commands.
#Return the binary equivalent of a-command and c-command based on the conversion to binary (a) and the c-pneumonics.

dest_dict = {"null":"000", "M":"001", "D":"010", "MD":"011", "A":"100", "AM":"101", "AD":"110", "AMD":"111", "":"000"}
jump_dict = {"null":"000", "JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111",
             "":"000"}
notacomp_dict = {"0":"101010", "1":"111111", "-1":"111010", "D":"001100", "A":"110000", "!D":"001101", "!A":"110001",
                 "-D":"001111", "-A":"110011", "D+1":"011111", "A+1":"110111", "D-1":"001110", "A-1":"110010",
                 "D+A":"000010", "D-A":"010011", "A-D":"000111", "D&A":"000000", "D|A":"010101"}
acomp_dict = {"M":"110000", "!M":"110001", "-M":"110011", "M+1":"110111", "M-1":"110010", "D+M":"000010",
              "D-M":"010011", "M-D":"000111", "D&M":"000000", "D|M":"010101"}

def a_command(col2):
    #As per the specs, 0+binary15 digit number representing memory addres.
    return "0" + bin(int(col2))[2::].zfill(15)

def c_notacomp(this_line):
    #Use the dictionaries to look up the correct binary translations.
    return "1110" + notacomp_dict.get(this_line[3]) + dest_dict.get(this_line[2]) +  jump_dict.get(this_line[4])

def c_acomp(this_line):
    #Use the dictionaries to look up the correct binary translations.
    return "1111" + acomp_dict.get(this_line[3]) + dest_dict.get(this_line[2]) + jump_dict.get(this_line[4])

def get_bin(AC_list):
    #If statements to determine which function to call.
    if AC_list[0] == "A_COMMAND":
        return a_command(AC_list[1])
    elif AC_list[3] in notacomp_dict:
        return c_notacomp(AC_list)
    else:
        return c_acomp(AC_list)
