import left_recursion


input_file = open("test.txt", "r")
grammar = input_file.readlines()
dictionar = {}
for line in  grammar:
    line = line.split('->')
    line[0] = line[0].strip()
    line[1] = line[1].strip()
    if line[0] not in dictionar:
        dictionar[line[0]] = line[1]
    else:
        dictionar[line[0]] += '|'+line[1]
output_file = open("tt.txt","w")
for key in dictionar:
    output_file.write(key + "->" + dictionar[key] + "\n")
output_file.close()    
input_file = open("tt.txt","r")
grammar = input_file.readlines()  

terminals = "abcdefghijklmnopqrstuvwxyz+"
non_terminals = terminals.upper()
terminals = terminals + "+*()"
epsilon = "@"
start_symbol = grammar[0][0]


def get_rules():
    rules = {}

    for rule in grammar:
        temp = rule.split("->")
        lhs = temp[0].strip()
        rhs = temp[1].strip()
        generations = list(map(lambda x: x.strip(), rhs.split("|")))
        rules[lhs] = generations
    return rules


def get_transformed_rules():
    rules = left_recursion.get_transformed(grammar)
    new_rules = {}

    for rule in rules:
        new_rules[rule["lhs"]] = rule["rhs"]

    return new_rules    


def first(x, rules):
    first_set = set()

    if len(x) == 1:
        if x in terminals or x == epsilon:
            first_set.add(x)
        
        if x in non_terminals:
            generations = rules[x]
            
            for generation in generations:
                get_set = first(generation, rules)
                first_set = first_set.union(get_set)
    else:
        for element in x:
            if element in terminals:
                first_set.add(element)
                break
            elif element in non_terminals:
                non_terminal_first = first(element, rules)

                if not epsilon in non_terminal_first:
                    first_set = first_set.union(non_terminal_first)
                    break
                else:
                    first_set = first_set.union(non_terminal_first)

    return first_set


def get_rules_containing_element(x, rules):
    containing_list = []

    for lhs, rhs in rules.items():
        if x == lhs:
            continue
        
        for generation in rhs:
            if x in generation:
                containing_list.append((generation, lhs))
    
    return containing_list


def follow(x, rules):
    follow_set = set()

    if x == start_symbol:
        follow_set.add("$")
    
    get_rules = get_rules_containing_element(x, rules)

    for rule, lhs in get_rules:
        for i in range(len(rule)):
            if rule[i] != x:
                continue
            
            if i == len(rule) - 1:
                follow_set = follow_set.union(follow(lhs, rules))
            else:
                beta = rule[(i + 1):]
                first_set = first(beta, rules)   

                if epsilon in first_set:
                    first_set.remove(epsilon)
                    follow_set = follow_set.union(first_set)
                    follow_set = follow_set.union(follow(lhs, rules))
                else:
                    follow_set = follow_set.union(first_set)
    
    return follow_set


all_rules = get_transformed_rules()

for k in all_rules.keys():
    get_set = first(k, all_rules)
    print(k)
    print(get_set)
    print(follow(k, all_rules))

parse_table = {}

for lhs in all_rules:
    for generation in all_rules[lhs]:
        first_set = first(generation, all_rules)

        for element in first_set:
            if element != epsilon:
                key = lhs + "," + element
                parse_table[key] = lhs + " -> " + generation

        if epsilon in first_set:
            follow_set = follow(lhs, all_rules)

            for elem in follow_set:
                key = lhs + "," + elem

                if elem != epsilon:
                    parse_table[key] = lhs + " -> " + generation

            if "$" in follow_set:
                key = lhs + ",$"
                parse_table[key] = lhs + " -> " + generation

for k, v in parse_table.items():
    print("{0}\t{1}".format(k, v))

input_string = input()
input_string = input_string + "$"
input_stack = list(reversed(list(input_string)))

stack = [start_symbol]

is_accepted = False

while len(stack) > 0:
    input_char = input_stack[-1]
    print(stack, input_char)
    stack_char = stack.pop()

    if input_char == '$' and len(stack) == 0:
        is_accepted = True
        break
    
    if stack_char == input_char:
        input_stack.pop()
        continue
    
    key = stack_char + "," + input_char

    if key not in parse_table:
        break
    
    rule = parse_table[key]
    rhs = rule.split("->")[1].strip()
    rhs = list(reversed(rhs))

    for element in rhs:
        if element != epsilon:
            stack.append(element)

if is_accepted:
    print("The string is accepted")
else:
    print("The String is not accepted")
