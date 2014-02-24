__author__ = 'E'


class SymbolTable:
    #Constructor that creates a dictionary and an index for the variables that start at RAM[16] in memory.
    def __init__(self):
        self.mem_dict = {"SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4, "R0":0, "R1":1, "R2":2, "R3":3,"R4":4, "R5":5,
                         "R6":6, "R7":7, "R8":8, "R9":9,"R10":10, "R11":11, "R12":12, "R13":13, "R14":14, "R15":15,
                         "SCREEN":16384, "KBD":24576}
        self.curr_mem = 16

    #Check that a key is in the dictionary.  If it is not, add it.  Two specifications--key/value pair can be provided
    #or a key can be provided and the value is curr_mem location in RAM to be allocated.
    def add_mem_address(self, key, value=None):
        if key not in self.mem_dict:
            if value is not None:
                self.mem_dict[key] = value
            else:
                self.mem_dict[key] = self.curr_mem
                self.curr_mem += 1

    #Return the memory address for a given key.
    def get_mem_address(self, key):
        return self.mem_dict.get(key)
