class Furigana:
    def __init__(self):
        pass
    
    def addFurigana(self, tokenized_word_list):
        out = "<html style='background-color: #101013; color: white; font-size: 48px;'>"
        for entry in tokenized_word_list:
            if entry['reading']:
                out += "<ruby><rb>" + entry['headword'] + "</rb><rt>" + entry['reading'] + "</rt></ruby>"
                # " (" + entry['reading'] + ") "
            else:
                out += entry['headword']
        out += "</html>"
        return out

    def addRuby():
        pass