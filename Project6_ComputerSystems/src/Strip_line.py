__author__ = 'E'
#Strip line is a short function that takes a string, finds and removes all the spaces and tabs in the string, and
#returns the string.
def strip_line(current_line):
    #Strip spaces and tabs and new line, add in a newline at the end.
    #Return the stripped line.
    return current_line.strip()

#Function to remove the comments from the string that is passed in.
def remove_comments(current_line):
    #Split the line at every occurrence of // and return the portion of the code to the left of the first comment sign.
    return current_line.split("//")[0]
