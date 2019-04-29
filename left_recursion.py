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
non_terminals = "abcdefghijklmnopqrstuvwxyz".upper()
used_non_terminals = set(list(non_terminals))
# print(used_non_terminals)
epsilon = "@"


def get_all_nonterminals(rules):
    all_non_terminals = []

    for rule in rules:
        all_non_terminals.append(rule["lhs"])
    
    return all_non_terminals


def get_rule_with_lhs(lhs, rules):
    for rule in rules:
        if rule["lhs"] == lhs:
            return rule


def detect_simple_left_recursion(rule):
    lhs = rule["lhs"]
    
    for non_terminal in rule["rhs"]:
        if non_terminal[0] == lhs:
            return True
    return False
            

def correct_simple_left_recursion(rule):
    lhs = rule["lhs"]
    new_non_terminal = used_non_terminals.pop()
    new_rules = []
    a_terminals = list(filter(lambda x: x[0] != lhs, rule["rhs"]))
    a_non_terminals = list(filter(lambda x: x[0] == lhs, rule["rhs"]))

    first_rule = {
        "lhs": lhs,
        "rhs": [x + new_non_terminal for x in a_terminals]
    }

    new_rules.append(first_rule)

    new_non_terminals = []

    second_rule = {
        "lhs": new_non_terminal,
        "rhs": [x[1:] + new_non_terminal for x in a_non_terminals] + ["@"]
    }

    new_rules.append(second_rule)
    
    return new_rules


def eliminate_left_recursion(rules):
    all_non_terminals = get_all_nonterminals(rules)
    
    for i in range(1, len(all_non_terminals)):
        for j in range(i):
            Aj = get_rule_with_lhs(all_non_terminals[j], rules)
            Ai = get_rule_with_lhs(all_non_terminals[i], rules)

            substr = ""
            found = False

            for idx in range(len(Ai["rhs"])):
                if Ai["rhs"][idx][0] == all_non_terminals[j]:
                    substr = Ai["rhs"][idx][1:]
                    found = True
                    del Ai["rhs"][idx]
                    break

            if found:
                new_rules = [x + substr for x in Aj["rhs"]]
                
                for elem in new_rules:
                    Ai["rhs"].append(elem)


def print_rule(rule):
    rhs = " | ".join(rule["rhs"])
    print("{0} -> {1}".format(rule["lhs"], rhs))


def get_transformed(grammar):
    rules = []

    for rule in grammar:
        temp = rule.split("->")
        lhs = temp[0].strip()
        rhs = temp[1].strip()
        used_non_terminals.remove(lhs)
        # print(used_non_terminals)
        generations = list(map(lambda x: x.strip(), rhs.split("|")))
        payload = {
            "lhs": lhs,
            "rhs": generations
        }

        rules.append(payload)

    tranformed_rules = []

    eliminate_left_recursion(rules)

    for rule in rules:
        if detect_simple_left_recursion(rule):
            corrected_rules = correct_simple_left_recursion(rule)

            for x in corrected_rules:
                tranformed_rules.append(x)
        else:
            tranformed_rules.append(rule)
    
    return tranformed_rules


if __name__ == '__main__':
    rules = get_transformed(grammar)
    for rule in rules:
        print(len(rule['rhs']))
        print_rule(rule)
