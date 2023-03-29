import os

class GetKnownWords:
    def __init__(self):
        self.dictionary = self.load_dictionary()
    
    def load_dictionary(self):
        os.chdir('C:\\Users\\jv_ca\\TCC\\backend')
        Dictionary_Palavras_conhecidas ='.\\ia\\PalavrasConhecidas\\Dictionary_Palavras_conhecidas.txt'
        with open(Dictionary_Palavras_conhecidas, 'r') as f:
            dictionary = eval(f.read())
        return dictionary

    def get_dict(self):
        return self.dictionary

    def get_values(self):
        return list(self.dictionary.values())

    def write_values_to_file(self):
        values = self.get_values()
        os.chdir('C:\\Users\\jv_ca\\TCC\\backend')
        palavras_conhecidas_pela_ai = '.\\ia\\PalavrasConhecidas\\palavras_conhecidas_pela_ai.txt'
        with open(palavras_conhecidas_pela_ai, 'w') as f:
            f.write(';'.join(values))