from sudachipy import tokenizer
from sudachipy import dictionary
import glob
import zipfile
import json

# Sudachi Parser
tokenizer_obj = tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.A

class Dictionary:
    def __init__(self):
        self.dictionary_path = 'res/dict'
        self.dictionary_list = []
        self.dictionary_map = []
        self.get_dictionaries()

    
    def get_dictionaries(self):
        self.dictionary_list = glob.glob(self.dictionary_path + '/*.zip')
        
    def set_dictionary(self, path):
        output_map = {}
        archive = zipfile.ZipFile(path, 'r')

        result = list()
        for file in archive.namelist():
            if file.startswith('term'):
                with archive.open(file) as f:
                    data = f.read()  
                    d = json.loads(data.decode("utf-8"))
                    result.extend(d)

        for entry in result:
            if (entry[0] in output_map):
                output_map[entry[0]].append(entry) 
            else:
                output_map[entry[0]] = [entry] # Using headword as key for finding the dictionary entry
        self.dictionary_map = output_map
    
    def look_up(self, sentence):
        tokenized_word_list = []
        out = []
        sentence = sentence.replace(" ", "")
        sentence = sentence.replace(" ", "") # two line breaks were breaking things
        words = [m.surface() for m in tokenizer_obj.tokenize(sentence, mode)]
        for word in words:
            try:
                for entry in self.dictionary_map[word]:
                        result = {
                            'headword': entry[0],
                            'reading': entry[1],
                            'tags': entry[2],
                            'glossary_list': entry[5],
                            'sequence': entry[6]
                        }
                        tokenized_word_list.append(result)
                        out.append(result)
                        break #FIX LATER: This makes it so it displays the first defintion of a word, which is good for now, but I would like a collapsible list of alternative definitions
            except Exception as e:
                print(e)
                result = {
                    'headword': word[0],
                    'reading': None,
                    'tags': None,
                    'glossary_list': None,
                    'sequence': None
                }
                tokenized_word_list.append(result)
                continue
        return tokenized_word_list, out

    def dict_scanner(self):
        pass


if __name__ == "__main__":
    dict = Dictionary()
    print(dict.dictionary_list[3])
    dict.set_dictionary(dict.dictionary_list[3])
    for entry in dict.look_up("掛ける"):
        print(entry)
