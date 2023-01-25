import json, os

'''
General overview.

    classes.
        - Meta and Story pairs:
            + 
'''

def text_read(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents

def text_create(path, content=''):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# placeholder
def tokenize(string):
    return string.split(' ')

# placeholder
def untokenize(tokens):
    return ' '.join(tokens)

# placeholder
def get_meta(string):
    words = string.split(' ')
    word_count = {word:words.count(word) for word in list(set(words))}
    top_n = 5
    word_count = dict(sorted(word_count.items(), key=lambda tup: tup[1], reverse=True)[:top_n])

    kv_joiner = ':'
    entry_joiner = ', '
    edges = ('[ ', ' ]')
    middle = entry_joiner.join([kv_joiner.join([k,str(v)]) for k,v in word_count.items()])
    result = edges[0] + middle + edges[1]
    return result

class Context:
    def __init__(self):
        self.string = ''
        self.tokens = []
        self.objects = []
        self.token_count = 0

    def add_text(self, meta):
        self.meta_list.append(meta)

    def add_story(self, story):
        self.story_list.append(story)
    
    def validate(self):
        # check types
        for o in self.objects:
            if type(o) not in (Meta, Story):
                exit()

        # check token length
        for o in self.objects:
            if o.token_count != len(o.tokenize(o.string)):
                exit()
            if o.token_count != len(o.tokens):
                exit()
        if self.token_count != len(self.tokens()):
            exit()
        if self.token_count != len(tokenize(self.string)):
            exit()

    def count_tokens(self):
        count = 0
        for o in self.objects:
            count += o.token_count
        return count

    def update(self):
        self.token_count = self.count_tokens()
    
    def analysis(self):
        pass

class Meta:
    def __init__(self, string, meta_obj):
        self.string = string
        self.story_obj = story_obj

class Story:
    def __init__(self, string, meta_obj):
        self.string = string
        self.meta_obj = meta_obj

'''
Singleton.  (this is not enforced programmatically)
Has a representation of the entire training set:
- knows how each story's metadata and text content is distributed
- knows how everything is tokenized
- knows for each 2048 token chunk:
    + which stories and metadata are there
    + how many tokens everything takes up

(this allows for elegant visualizations and overviews, hopefully)
'''
class TrainingData:
    def __init__(self):
        pass

folder = 'stories'
paths = [f'{folder}/{f}' for f in os.listdir(folder)]
story_strings = list(map(text_read, paths))
meta_objects = []
story_objects = []
for s in story_strings:
    














