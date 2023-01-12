class Furigana:
    def __init__(self):
        pass
    
    def addFurigana(self, tokenized_word_list):
        out = "<html style='background-color: #101013; color: white; font-size: 48px;'>"
        for entry in tokenized_word_list:
            if entry.reading:
                out += "<ruby><rb>" + entry.headword + "</rb><rt>" + entry.reading[0] + "</rt></ruby>"
                # " (" + entry['reading'] + ") "
            else:
                out += entry.headword
        out += "</html>"
        return out

    def addRuby():
        pass

if __name__ == "__main__":
    pass
    # for entry in out:
    # if entry['reading'] is not None and entry['reading'] != ['']:
    #     print("Word: "+ entry['headword'])
    #     print("Reading: "+ ", ".join(entry['reading']))
    #     print("Definition: "+ ", ".join(list(itertools.chain.from_iterable(entry['glossary_list']))))
    #     print("")