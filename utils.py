from translate import Translator

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
words = {}
words['noun'] = {'work':'kam'}
words['pronoun'] = {'he':'voh'}
words['verb'] = {'does':'krta hai'}
EntoHn = {}
EntoHn['pronoun-verb-noun'] = 'pronoun-noun-verb'
sentence_en = input()
input_en_words = Tokenise(sentence_en)
grammar_en = ''
print(input_en_words)
for i in range(len(input_en_words)):
    if i == len(input_en_words) - 1:
        for attribute, at_dict in words.items():
            if input_en_words[i] in at_dict:
                grammar_en += attribute
    else:
        for attribute, at_dict in words.items():
            if input_en_words[i] in at_dict:
                grammar_en += (attribute+'-')
grammar_en_words = grammar_en.split('-')
grammar_hin = EntoHn[grammar_en]
grammar_hin_words = grammar_hin.split('-')
output_hin = ''
for i, grammar_word in enumerate(grammar_hin_words):
    ind = grammar_en_words.index(grammar_word)
    if i == len(grammar_hin_words) - 1:
        output_hin += words[grammar_word][input_en_words[ind]]
    else:
        output_hin += words[grammar_word][input_en_words[ind]] + ' '
    
print(output_hin)