import json, os

'''
General overview.

    classes.
        - Meta and Story pairs:
            + contain references to one another
            + Story creates a Meta instance when initialized.
        - Context
            + will implement the logic for filling up a context of 2048 tokens
            + contains references to Meta and Story instances
        - TrainingData
            + (intended as something to) provide an overview of:
                - 2048 chunks
                - locations of story text and metadata text

    rest.
        - tokenize/untokenize
            + placeholder
        - get_meta
            + placeholder
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
    word_count = dict(sorted(word_count.items(), key=lambda tup: tup[1], reverse=False)[:])

    kv_joiner = ':'
    entry_joiner = ', '
    edges = ('[ ', ' ]')
    middle = entry_joiner.join([kv_joiner.join([k,str(v)]) for k,v in word_count.items()])
    result = edges[0] + middle + edges[1]
    return result

# a lot of nonsense is here.. need to remove and rewrite stuff.
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
    def __init__(self, string, story_object):
        self.string = string
        self.story_object = story_object

class Story:
    def __init__(self, string):
        self.string = string
        self.meta_object = Meta(
            string=get_meta(self.string),
            story_object=self
        )

'''
Singleton class.  (which is not enforced programmatically)

Has a representation of the entire training set:
- knows how each story's metadata and text content is distributed
- knows how everything is tokenized
- knows for each 2048 token chunk:
    + which stories and metadata are there
    + how many tokens everything takes up

(this potentially allows for elegant visualizations and overviews)
'''
class TrainingData:
    def __init__(self):
        self.chunks = {}
        self.story_objects = {}
        self.meta_objects = {}
training_data = TrainingData()

folder = 'stories'
paths = [f'{folder}/{f}' for f in os.listdir(folder)]
story_strings = list(map(text_read, paths))
meta_objects = []
story_objects = []
for s in story_strings:
    s_o = Story(s)
    m_o = s_o.meta_object
    story_objects.append(s_o)
    meta_objects.append(m_o)

for s, m in zip(story_objects, meta_objects):
    print(s, m)
    print(s.meta_object == m)
    print(s == m.story_object)
    print(m.string)
    print('---')
    print(s.string)
    print('------------------')













