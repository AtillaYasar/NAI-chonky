import json, os
from transformers import GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

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
    tokens = tokenizer.encode(string)
    return tokens

# placeholder
def untokenize(tokens):
    string = tokenizer.decode(tokens)
    return string

# placeholder
def get_meta(
    string,
    top_n = 10,
    reverse = True,
    kv_joiner = ':',
    entry_joiner = ', ',
    edges = ('[ ', ' ]'),
    prefix = '',
    suffix = '\n'
):
    words = string.split(' ')
    word_count = {word:words.count(word) for word in list(set(words))}
    word_count = dict(sorted(word_count.items(), key=lambda tup: tup[1], reverse=reverse)[:top_n])

    middle = entry_joiner.join([kv_joiner.join([k,str(v)]) for k,v in word_count.items()])

    result = ''.join([prefix, edges[0], middle, edges[1], suffix])
    return result

# a lot of nonsense is here.. need to remove and rewrite stuff.
class Context:
    def __init__(self, size):
        self.objects = []
        self.size = size
    
    def fill(self):
        '''
        get info from training_data
        use info to fill context
        '''
        overview = training_data.get_overview()
        candidates = overview['candidates']
        self.objects = [
            candidates['meta'][0],
            candidates['story'][0]
        ]

        checkres = self.check_if_full()
        check_all_chunks('after checkres')
        if not checkres[0]:
            print(checkres[1])
            exit()
        else:
            training_data.filled(self)
            check_all_chunks('after training_data.filled')

    def check_if_full(self):
        '''
        conditions:
            - token count == self.size
            - starts with meta, has corresponding story right after
            - each story is bigger than the context size, so
                + each context just has [metadata, story piece]
                + (this is a simplifying and temporary assumption)
        '''

        def len_checker(objects):
            return len(objects) == 2

        def first_meta(objects):
            return type(objects[0]) is Meta

        def second_story(objects):
            return type(objects[1]) is Story

        def token_counter(objects):
            # tokenize seperately, combine lists, untokenize, retokenize, count.
            tokens = []
            for o in self.objects:
                tokens += tokenize(o.string)
            rejoined = untokenize(tokens)
            tokens = tokenize(rejoined)
            count = len(tokens)
            
            return count == self.size
        def token_counter_solver(objects):
            story_space = self.size - len(tokenize(objects[0].string))
            objects[1].shrink(new_size=story_space)

            if not token_counter(objects):
                exit('token_counter_solver implementation failed')
            else:
                pass
                #exit('solver worked lmao')
            return objects

        constraints = [
            {
                'name':'len_checker',
                'checker':len_checker,
                'error description':'need exactly 2 objects',
                'solver':None
            },
            {
                'name':'first_meta',
                'checker':first_meta,
                'error description':'first object should be meta',
                'solver':None
            },
            {
                'name':'second_story',
                'checker':second_story,
                'error description':'second object should be story',
                'solver':None
            },
            {
                'name':'token_counter',
                'checker':token_counter,
                'error description':'token count not exactly self.size',
                'solver':token_counter_solver
            },
        ]

        for con in constraints:
            if con['checker'](self.objects):
                pass
            else:
                if con['solver'] != None:
                    con['solver'](self.objects)
                else:
                    return (False, con)

        return (True, '')

class Meta:
    def __init__(self, string, story_object):
        self.string = string
        self.story_object = story_object

class Story:
    def __init__(self, string):
        prefix = ''
        suffix = '\n'
        self.string = ''.join([prefix, string, suffix])
        self.meta_object = Meta(
            string=get_meta(self.string, top_n=10, reverse=False),
            story_object=self
        )
    
    def shrink(self, new_size):
        self.string = untokenize(tokenize(self.string)[:new_size])

'''
Singleton class.  (which is not enforced programmatically)

(aspirations below)
Has a representation of the entire training set:
- knows how each story's metadata and text content is distributed
- knows how everything is tokenized
- knows for each 2048 token chunk:
    + which stories and metadata are there
    + how many tokens everything takes up

(this potentially allows for elegant visualizations and overviews)
'''
class TrainingData:
    def __init__(self, story_objects, meta_objects):
        self.chunks = []
        self.story_objects = story_objects
        self.meta_objects = meta_objects
        self.context_objects = []

    # Context calls this to know how to fill a piece of context.
    def get_overview(self):
        # list of all objects present
        added_obj = []
        for c in self.context_objects:
            added_obj += c.objects

        # candidates are those that arent present
        candidates = {'meta':[], 'story':[]}
        for s,m in zip(self.story_objects, self.meta_objects):
            if s not in added_obj:
                candidates['story'].append(s)
            if m not in added_obj:
                candidates['meta'].append(m)

        return {
            'candidates':candidates
        }

    def filled(self, context):
        # add to collection
        self.context_objects.append(context)
        check_all_chunks('first')

        # to make a chunk, tokenize parts, combine, untokenize
        tokens = []
        for o in context.objects:
            tokens += tokenize(o.string)
        new_chunk = untokenize(tokens)
        self.chunks.append(new_chunk)

        check_all_chunks('second')

def check_all_chunks(moment):
    debugging = True
    if not debugging:
        return 0
    print('==========')
    print(f'starting, moment = {moment}')
    for c in training_data.chunks:
        assert len(tokenize(c)) == context_size
    print(f'ended, moment = {moment}')
    print('==========')


folder = 'stories'
paths = [f'{folder}/{f}' for f in os.listdir(folder)]
story_strings = list(map(text_read, paths))
meta_objects = []
story_objects = []
# create and store Meta and Story pairs
for s in story_strings:
    s_o = Story(s)
    m_o = s_o.meta_object
    story_objects.append(s_o)
    meta_objects.append(m_o)
training_data = TrainingData(meta_objects=meta_objects, story_objects=story_objects)

# checking if stuff goes as expected
for s, m in zip(story_objects, meta_objects):
    assert s.meta_object == m
    assert s == m.story_object
    continue
    print(s, m)
    print(m.string)
    print('---')
    print(s.string)
    print('------------------')

context_objects = []
context_size = min([len(tokenize(o.string)) for o in story_objects])

for i in range(len(story_strings)):
    c_o = Context(context_size)
    c_o.fill()
    check_all_chunks(f'inside loop, {i}')


#print(training_data.chunks[0])
#print('------------')
objects = training_data.context_objects[0].objects
d = [{'type':str(type(o)), 'string':o.string} for o in objects]
#print(json.dumps(d, indent=2))
#print(objects[0].string.count('\n'))

chunk_joiner = ''
res = chunk_joiner.join(training_data.chunks)
text_create('playground_res.txt', res)
check_all_chunks('at the end')

# final check
print(len(tokenize(res)), len(tokenize(res))/context_size, context_size*len(training_data.chunks))
assert len(tokenize(res)) == context_size*len(training_data.chunks)
