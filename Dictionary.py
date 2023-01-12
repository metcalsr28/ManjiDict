from sudachipy import tokenizer
from sudachipy import dictionary
import glob
import zipfile
import json
import itertools
from JapaneseWord import JapaneseWord

# Sudachi Parser
tokenizer_obj = tokenizer_obj = dictionary.Dictionary(dict_type="full").create()
mode = tokenizer.Tokenizer.SplitMode.C

class Dictionary:
    def __init__(self):
        self.dictionary_path = 'res/dict'
        self.dictionary_list = []
        self.dictionary_map = []
        self.search_history = []
        self.search_index = 0
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
        out = []
        sentence = sentence.replace(" ", "")
        sentence = sentence.replace("…", "...")
        sentence = sentence.replace("\n", "")

        tokens = tokenizer_obj.tokenize(sentence, mode)

        words = self.recombine(tokens)

        for word in words:
            nextWord = JapaneseWord()
            try:
                for entry in self.dictionary_map[word]:
                    nextWord.headword = entry[0]
                    if entry[1] not in nextWord.reading:
                        nextWord.reading.append(entry[1])
                    if entry[2] not in nextWord.tags:
                        nextWord.tags.append(entry[2])
                    if entry[5] not in nextWord.glossary:
                        nextWord.glossary.append(entry[5])
                    if entry[6] not in nextWord.sequence and len(nextWord.sequence) < 4:
                        nextWord.sequence.append(str(entry[6]))
                out.append(nextWord)
                nextWord = JapaneseWord()

            except Exception as e:
                #print("T1 Ex: " + str(e))
                try:
                    corrected_words = [m.dictionary_form() for m in tokenizer_obj.tokenize(word, mode)]
                    print(corrected_words)
                    for corrected_word in corrected_words:
                        for entry in self.dictionary_map[corrected_word]:
                            #print(entry[0])
                            nextWord.headword = word
                            if entry[1] not in nextWord.reading:
                                nextWord.reading.append(entry[1])
                            if entry[2] not in nextWord.tags:
                                nextWord.tags.append(entry[2])
                            if entry[5] not in nextWord.glossary:
                                nextWord.glossary.append(entry[5])
                            if entry[6] not in nextWord.sequence and len(nextWord.sequence) < 4:
                                nextWord.sequence.append(str(entry[6]))
                        out.append(nextWord)
                        nextWord = JapaneseWord()
                        break
                except Exception as e2:
                    try:
                        #print("T2 Ex: " + str(e2))
                        corrected_words = [m.normalized_form() for m in tokenizer_obj.tokenize(word, mode)]
                        for corrected_word in corrected_words:
                            for entry in self.dictionary_map[corrected_word]:
                                nextWord.headword = corrected_word
                                if entry[1] not in nextWord.reading:
                                    nextWord.reading.append(entry[1])
                                if entry[2] not in nextWord.tags:
                                    nextWord.tags.append(entry[2])
                                if entry[5] not in nextWord.glossary:
                                    nextWord.glossary.append(entry[5])
                                if entry[6] not in nextWord.sequence and len(nextWord.sequence) < 4:
                                    nextWord.sequence.append(str(entry[6]))
                            out.append(nextWord)
                            nextWord = JapaneseWord()

                    except Exception as e3:
                        #print("T3 Ex: " + str(e3))
                        nextWord = JapaneseWord(word, None, None, None, None, None)
                        out.append(nextWord)
        return out

    def recombine(self, tokens):
        words = []
        for x in range(len(tokens)):
            if (tokens[x].part_of_speech()[0] == "助詞" or tokens[x].part_of_speech()[0] == "助動詞") and x != 0:
                words[-1] = words[-1] + str(tokens[x])
            elif (tokens[x].part_of_speech()[5] == "連用形-一般" and tokens[x-1].part_of_speech()[0] != "副詞" and tokens[x-1].part_of_speech()[5] != "仮定形-一般") and x != 0:
                words[-1] = words[-1] + str(tokens[x])
            elif (tokens[x].part_of_speech()[5] == "連用形-一般" and tokens[x-1].part_of_speech()[5] != "仮定形-一般") and x != 0:
                words[-1] = words[-1] + str(tokens[x])
            else:
                words.append(str(tokens[x]))
        return words


if __name__ == "__main__":
    pass
    # dict = Dictionary()
    # #print(dict.dictionary_list[3])
    # dict.set_dictionary(dict.dictionary_list[3])
    # out = dict.look_up("日本が国連安保理 非常任理事国に 石兼国連大使「責任大きい」")
    # for entry in out:
    #     if entry['reading'] is not None and entry['reading'] != ['']:
    #         #print("Word: "+ entry['headword'])
    #         #print("Reading: "+ ", ".join(entry['reading']))
    #         #print("Definition: "+ ", ".join(list(itertools.chain.from_iterable(entry['glossary_list']))))
    #         #print("")
