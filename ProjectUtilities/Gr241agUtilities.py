"""
1. This folder can Store project/specific related functions
2. Note: For generic utilities that may be used in different projects, store in folder 'Utilities'
"""


# utils ...
def replace_chars_from_cmds(string):
    control_char = ['=', '/', ' ', '-']
    output_string = ''
    counter = 0
    for _char in string:
        if _char in control_char:
            if counter == 0:
                output_string = output_string + "_"
                counter = counter + 1
            else:
                output_string = output_string + ""
                counter = counter + 1
        else:
            counter = 0
            output_string = output_string + _char
    return output_string