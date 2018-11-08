'''

Program functions to be added by another program as a module, doesn't have main logic

This file came from https://github.com/1deterministic/Simple-Logical-Expression-Analyzer
The version used is in about.py in the same folder
It has the main symbols changed in order to not conflict with possible file names

'''

# defines the characters used

# logical operators
logical_and = "^"
logical_or = "|"
logical_not = "~"

# stack indicators
stack_in = "{"
stack_out = "}"

# returns information about this program
# you must have about.py on the same directory
def get_program_info():
    try:
        from . import about
        return about.name + " " + about.version + " " + about.codename + " " + about.build_date
    except:
        return "about.py is not on the same directory as slea.py"

# returns the substring that is under the influence of a previous logical_not operator
# retuns also (first) the index where the influence stopped
def get_not_substring(expr):
    expr = expr.replace(" ", "")

    out = []

    i = 0
    stack_level = 0
    while True:
        # if the expression already ended
        if i >= len(expr):
            # the substring affected is the entire string
            return i, expr
            break

        # if entering a stack
        elif expr[i] == stack_in:
            stack_level += 1

        # if exiting a stack
        elif expr[i] == stack_out:
            stack_level -= 1

        # if there is no (more) stack
        if stack_level == 0:
            # if there was found an operator character
            if expr[i] == logical_and or expr[i] == logical_or:
                # returns all the string until this point
                return i, expr[:i]

            # if another not was found
            elif expr[i] == logical_not:
                # ignore the second one (only the first logical not is considered)
                # hopefully is covered by the syntax analyzer
                return get_not_substring(expr[i + 1:])

        i += 1

    return out

# returns the substring that is under the influence of a previous stack_in
# retuns also (first) the index where the influence stopped
def get_stack_substring(expr):
    expr = expr.replace(" ", "")

    out = []

    i = 0
    stack_level = 1 # starts at 1 because a stack_in was already read before calling the function
    while True:
        # if the expression already ended
        if i >= len(expr):
            # the substring affected is the entire string
            # hopefully is covered by the syntax analyzer (returning unclosed stacks)
            return i, expr
            break

        # if another stack is detected
        elif expr[i] == stack_in:
            stack_level += 1

        # if a stack is ending
        elif expr[i] == stack_out:
            stack_level -= 1

        # if there is no more stacks to search
        # not another elif to prevent a stack_out from appearing in the first if
        if stack_level == 0:
            return i, expr[:i]

        i += 1

# mounts the syntax tree (a list actually) with the logical operations to evaluate
def get_syntax_tree(expr):
    expr = expr.replace(" ", "")

    out = []

    i = 0
    operator_index = -1
    subtree = []
    while True:
        # if the expression already ended
        if i >= len(expr):
            # if there is a subtree pending to be appended
            if not subtree == []:
                # append it before stopping
                out.append(subtree)

            # if there is no pending subtree
            else:
                # append whatever operand was after the last operator
                out.append(expr[operator_index + 1:i])

            # stops the loop
            break

        # if a stack_in is detected
        elif expr[i] == stack_in:
            # gets the substring affected by this stack
            subtree_len, substring = get_stack_substring(expr[i + 1:])
            # mounts another tree with this substring
            subtree = get_syntax_tree(substring)
            # skips the entire affected part
            i += subtree_len


        # if there was found an operator character
        elif expr[i] == logical_and or expr[i] == logical_or:
            # if there is an operator right next to another one
            if (operator_index == i - 1) and operator_index != -1:
                # ignores the second one
                # hopefully is covered by the syntax analyzer
                operator_index = i

            # if it's not the case
            else:
                # if there is no pending subtree to be appended
                if subtree == []:
                    # appends the first part of the expression as an operand
                    out.append(expr[operator_index + 1:i])
                    
                # if it is
                else:
                    # appends the subtree
                    out.append(subtree)
                    # cleans out the pending subtree
                    subtree = []

                # if the last operator found is not the first element of the string
                # hopefully is covered by the syntax analyzer
                if operator_index > 0:
                    # creates a subtree out of the current expression
                    aux = out
                    out = []
                    out.append(aux)

                # appends the operator
                out.append(expr[i])
                operator_index = i
            
        # if a logical_not is detected
        if expr[i] == logical_not:
            # gets the substring affected by this logical_not operator
            subtree_len, substring = get_not_substring(expr[i + 1:])
            # mounts another tree out of the affected substring
            subtree = [logical_not, get_syntax_tree(substring)]
            # skips the entire substring
            i += subtree_len
            
            # search the part affected by the not operation and add it as a subtree
            #subtree = [logical_not, get_not_substring(expr[i + 1:])]
            # if its a stack, return its tree in the place of the second element of subtree

        i += 1

    # prevents returning nested lists with only one element
    if len(out) == 1:
        return out[0]
    else:
        return out

# evaluates a generated tree in true or false
def evaluate_syntax_tree(tree, value_of, argument):
    if type(tree) == list:
        # empty operand
        if len(tree) == 0:
            return False
        # single operand on a list
        elif len(tree) == 1:
            return value_of(tree[0], argument)

        # double operand = not operation
        elif len(tree) == 2:
            return not evaluate_syntax_tree(tree[1], value_of, argument)
        # triple operand = and, or
        elif len(tree) == 3:
            if tree[1] == logical_and: return evaluate_syntax_tree(tree[0], value_of, argument) and evaluate_syntax_tree(tree[2], value_of, argument)
            if tree[1] == logical_or: return evaluate_syntax_tree(tree[0], value_of, argument) or evaluate_syntax_tree(tree[2], value_of, argument)
    
        return False
        
    # text operand
    elif type(tree) == str:
        return value_of(tree, argument)

# syntax analyzer
# returns the index of a syntax error or the string lenght if no error was found
def evaluate_syntax(expr, debug=False):
    # tracking automata states
    initial_state = True
    operand_state = False
    operator_state = False
    not_state = False # not requires a special approach
    stack_out_state = False # ending a stack requires another special approach

    # tracks entering and leaving stacks
    stack_level = 0
    
    i = 0
    while True:
        # if the expression already ended
        if i >= len(expr):
            # if the current state is a correct stopping state
            if stack_level == 0 and (initial_state or operand_state or stack_out_state):
                # returns correctly
                return i
            # if that's not the case
            else:
                # indicate the error on the last character, since the error didn't stop the function before
                return i - 1

        # automata initial state
        elif initial_state:
            # characters not allowed to start the expression
            if (
                expr[i] == logical_and or 
                expr[i] == logical_or or 
                expr[i] == stack_out
            ):
                return i

            # goes to the not state
            elif expr[i] == logical_not:
                initial_state = False
                not_state = True

            # increases the stack level but stays in the current state
            elif expr[i] == stack_in:
                stack_level += 1

            # goes to the operand state on any other character but space (' '), wich is ignored
            elif not expr[i] == " ":
                initial_state = False
                operand_state = True


        # automata operand state
        elif operand_state:
            # goes to the operand state on logical_and or logical_or
            if expr[i] == logical_and or expr[i] == logical_or:
                operand_state = False
                operator_state = True

            # error if logical_not after an operand
            elif expr[i] == logical_not:
                return i

            # increases the stack level but stays on the current state
            elif expr[i] == stack_in:
                return i

            # decreases the stack level and goes to the stack out state
            elif expr[i] == stack_out:
                # a stack_out is valid only with a previous stack in
                if stack_level > 0:
                    stack_level -= 1
                    operand_state = False
                    stack_out_state = True
                else:
                    return i
            
            # stays on the current state on any other character but space (' '), wich is ignored
            elif not expr[i] == " ":
                operand_state = True


        # automata operand state
        elif operator_state:
            # returns error on a subsequent operator except the not operator
            if expr[i] == logical_and or expr[i] == logical_or:
                return i

            # goes to the not state on logical_not operator
            elif expr[i] == logical_not:
                operator_state = False
                not_state = True

            # increases the stack level but stays on the current state
            elif expr[i] == stack_in:
                stack_level += 1

            # returns error on stack_out (can't stack_out right after an operator)
            elif expr[i] == stack_out:
                return i
                #stack_level -= 1
                #operator_state = False
                #stack_out_state = True

            # goes to the operand state on any other character but space (' '), wich is ignored
            elif not expr[i] == " ":
                operator_state = False
                operand_state = True


        # automata logical not state
        elif not_state:
            # returns error on any operator (doubled operators)
            if expr[i] == logical_and or expr[i] == logical_or or expr[i] == logical_not:
                return i

            # increases the stack level but stays on the current state
            elif expr[i] == stack_in:
                stack_level += 1

            # returns error on stack_out (can't stack out right after a not operator)
            elif expr[i] == stack_out:
                return i

            # goes to the operand state on any other character but space (' '), wich is ignored
            elif not expr[i] == " ":
                not_state = False
                operand_state = True


        # automata stack out state
        elif stack_out_state:
            # goes to the operator state on any logical operator but logical_not
            if expr[i] == logical_and or expr[i] == logical_or:
                stack_out_state = False
                operator_state = True

            # decreases the stack level but stays on the current state
            elif expr[i] == stack_out:
                # prevent stacking out too much
                if stack_level > 0:
                    stack_level -= 1
                else:
                    return i
            
            # returns error on any other character but space (' '), wich is ignored
            elif not expr[i] == " ":
                return i

        i += 1