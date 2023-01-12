# word = JapaneseWord("あの人", "あのひと", "pn", 611, ["he","she","that person"], 1000440);
class JapaneseWord:
  def __init__(self, headword='', reading=None, tags=None, sequence=None, glossary=None, id=None):
    self.headword = headword
    self.reading = reading
    self.tags = tags
    self.sequence = sequence
    self.glossary = glossary
    self.id = id
    self.stem = ""
    self.okurigana = ""

    if self.reading == None:
        self.reading = []
    if self.tags == None:
        self.tags = []
    if self.sequence == None:
        self.sequence = []
    if self.glossary == None:
        self.glossary = []
    if self.id == None:
        self.id = -1