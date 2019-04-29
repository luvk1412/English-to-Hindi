productions = {}
with open('test.txt', 'r') as f:
    content = f.readlines()

for line in content:
    line = line.split('->')
    line = [val.strip() for val in line]
    if line[0] not in productions:
        productions[line[0]] = [line[1]]
    else:
        productions[line[0]].append(line[1])


for key, val in productions.items():
    print(key, ':', len(val))

def parser(sentence, pos, symbol = 'S'):
    if symbol == 'N':
        print('Enter',pos)
    ar_symbol = productions[symbol]
    for term in ar_symbol:
        flag = 0

        match_ct = 0
        new_pos = pos
        if symbol =='N' and term == 'p+n':
            print(term,pos, new_pos)
            flag = 1
        for letter in term:
            if letter.isupper():

                if new_pos >= len(sentence):
                    break
                if flag == 1:
                    print('nt', new_pos, sentence, letter)
                new_pos_tmp = parser(sentence, new_pos, letter)
                if new_pos_tmp >= new_pos:
                    match_ct += 1
                    new_pos = new_pos_tmp
                    continue
                else:
                    break
                
            else:
                if flag == 1:
                    print('t', new_pos, sentence, letter)
                if new_pos >= len(sentence):
                    break
                if sentence[new_pos] == letter:
                    new_pos += 1
                    match_ct += 1
                    continue
                else:
                    break
        if flag == 1:
            print(match_ct)
        if match_ct == len(term):
            print(term + ':-')
        if match_ct == len(term):
            return new_pos
    return pos


sentence = input()
sentence += '$'
ind = parser(sentence, 0)
print(ind)
if sentence[ind] == '$':
    print('Accepted')
else:
    print('Not Accepetd')