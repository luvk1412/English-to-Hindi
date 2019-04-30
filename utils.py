import codecs
import nltk
import LRParser

def Tokenise(s):
    sentences = s.strip().split('.')
    f_sentences = []
    for val in sentences:
        if val != '':
            f_sentences.append(val)
    words = []
    for sentence in f_sentences:
        tmp = sentence.strip().split(',')
        for tmp_sentence in tmp:
            tmp_words = tmp_sentence.strip().split()
            for word in tmp_words:
                words.append(word.strip())
    return words
def Load_Dictionary():
    files = ['noun.txt', 'pronouns.txt', 'verbm.txt', 'verbf.txt', 'verbplu.txt','adjective.txt', 'prepositions.txt']
    words = {}
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            word_class =  file.split('.')[0]
            words[word_class] = {}
            for line in lines:
                line = line.strip().split('-')
                words[word_class][line[0]] = line[1]
    return words
def Load_TranslationRules():
    EntoHn_rules = {}
    with open('Rules.txt','r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().split('-')
            lhs = line[0].strip()
            rhs = line[1].strip()
            EntoHn_rules[lhs] = rhs
    return EntoHn_rules

def get_tagged_sentence(sentence_en):
    input_en_words = Tokenise(sentence_en)
    tagged_en_words = nltk.pos_tag(input_en_words)
    grammar_en = ''
    flag = 0
    for val in tagged_en_words:
        if flag == 0:
            grammar_en+=val[1]
            flag = 1
        else:
            grammar_en += ('+'+val[1])
    return grammar_en

def Translate_EN_HN(s):
    if not LRParser.process_input(s):
        return '1'
    words = Load_Dictionary()
    EntoHn_rules = Load_TranslationRules()
    tokkened_s = Tokenise(s)
    word_class = {'TO':'prepositions','IN':'prepositions','JJ':'adjective','JJR':'adjective','JJS':'adjective','NN':'noun','NNS':'noun','NNP':'noun','NNPS':'noun','VB':'verbm','VBD':'verbm','VBG':'verbm','VBN':'verbm','VBP':'verbm','VBZ':'verbm','PRP':'pronouns', 'PRP$':'pronouns'}
    if tokkened_s[0] == 'she' or tokkened_s[0] == 'She':
        word_class['VB'] = 'verbf'
        word_class['VBD'] = 'verbf'
        word_class['VBG'] = 'verbf'
        word_class['VBN'] = 'verbf'
        word_class['VBP'] = 'verbf'
        word_class['VBZ'] = 'verbf'
    if tokkened_s[0] == 'they' or tokkened_s[0] == 'They':
        word_class['VB'] = 'verbplu'
        word_class['VBD'] = 'verbplu'
        word_class['VBG'] = 'verbplu'
        word_class['VBN'] = 'verbplu'
        word_class['VBP'] = 'verbplu'
        word_class['VBZ'] = 'verbplu'
    for item in tokkened_s:
        flag = 0
        for key, val in words.items():
            if item in val:
                flag = 1
                break
        if flag == 0:
            return '2'
         
    tagged_s = get_tagged_sentence(s)
    if tagged_s not in EntoHn_rules:
        print(tagged_s)
        return '3'
    grammar_hin = EntoHn_rules[tagged_s]
    print(tagged_s+'-'+grammar_hin)
    grammar_en_words = tagged_s.strip().split('+')
    grammar_hin_words = grammar_hin.split('+')
    output_hin = ''
    for i, grammar_word in enumerate(grammar_hin_words):
        ind = grammar_en_words.index(grammar_word)
        if i == len(grammar_hin_words) - 1:
            output_hin += words[word_class[grammar_word]][tokkened_s[ind]]
        else:
            output_hin += words[word_class[grammar_word]][tokkened_s[ind]] + ' '
    return output_hin



if __name__ == '__main__':
    sentence_en = input()
    sentence_hindi = Translate_EN_HN(sentence_en)
    print(sentence_hindi)
