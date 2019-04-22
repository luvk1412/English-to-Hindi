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

def parser():
    print('hi')

translator= Translator(to_lang="Hindi")
translation = translator.translate("Good Morning!")
print(translation.decode('utf-8'))