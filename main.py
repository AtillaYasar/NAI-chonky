class Tracker:
    def __init__(self):
        self.stuff = []

class MyClass:
    def __init__(self):
        self.attribute = 'placeholder'
        tracker.stuff.append(self)

tracker = Tracker()
for i in range(3):
    o = MyClass()
    for ob in tracker.stuff:
        print(tracker.stuff)
        assert tracker.stuff.count(ob) == 1

'''
General overview.
(was outdated, so i deleted it)

Progress in general:
- i am refactoring the code
- just removed a lot of stuff that made everything complex and made me pull my hair out
'''


import json, os, time, logging

t0 = time.time()
from transformers import GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
t1 = time.time()-t0


logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.info('===== ===== =====')
logging.info('===== ===== =====')
logging.info('===== started logging =====')
logging.info('===== ===== =====')
logging.info('===== ===== =====')

logging.info(f'getting tokenizer took {t1} seconds')

# example from logging docs  (for myself)
'''
import logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
'''

def text_read(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents

def text_create(path, content=''):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

'''
tokenize and untokenize functions require this at the top:
    from transformers import GPT2Tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
'''
# string --> list of token ids
def tokenize(string):
    t0 = time.time()

    tokens = tokenizer.encode(string)

    logging.info(f'tokenizing took {time.time()-t0} seconds')
    return tokens
# list of token ids --> string
def untokenize(tokens):
    t0 = time.time()

    string = tokenizer.decode(tokens)

    logging.info(f'tokenizing took {time.time()-t0} seconds')
    return string

# basically for doing json.dumps(obj, indent=2) on an object, but first dealing with things that would return an error
def serializable_json(obj, custom_serializer=None):
    def default_serializer(obj):
        return '<<this object is not serializable>>'
    if custom_serializer == None:
        f = default_serializer
    else:
        f = custom_serializer

    return json.dumps(obj, indent=2, default=f)

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

'''
returns the first item of an iterator where checker(item) evaluates to True.
if the item is not found, will raise an error, unless you pass an on_unfound value.
'''
def search_iterator(lst, checker, on_unfound='give an error'):
    if on_unfound == 'give an error':
        return next( (item for item in lst if checker(item)) )
    else:
        return next( (item for item in lst if checker(item)), default=on_unfound )

class Meta:
    def __init__(self, string, story_object):
        self.string = string
        self.story_object = story_object
    def __repr__(self):
        n = 20
        return f'Meta object: first {n} chars:' + self.string[:n]

class Story:
    def __init__(self, string, custom_meta=None):
        prefix = ''
        suffix = '\n'
        self.string = ''.join([prefix, string, suffix])

        if custom_meta == None:
            metadata = get_meta(string, top_n=10, reverse=False)
        else:
            assert type(custom_meta) is str
            metadata = custom_meta
        self.meta_object = Meta(
            string=metadata,
            story_object=self
        )
    def __repr__(self):
        n = 20
        return f'Story object: first {n} chars:' + self.string[:n]

    def shrink(self, new_size):
        if type(new_size) is not int:
            raise Exception('new_size must be int')
        tokens = tokenize(self.string)
        self.string = untokenize(tokens[:new_size])

class Context:
    def __init__(self, size):
        self.objects = []
        self.size = size
        self.complete = False
    
    def add_story(self, story_object):
        meta_object = story_object.meta_object
        self.objects.append(meta_object)
        self.objects.append(story_object)

'''
(aspirations for) the TrainingData class are listed below:

Has a representation of the entire training set:
- knows how each story's metadata and text content is distributed
- knows how everything is tokenized
- knows for each {context_size} token chunk:
    + which stories and metadata are there
    + how many tokens everything takes up

(this potentially allows for elegant visualizations and overviews)
'''
class TrainingData:
    def __init__(self, all_story_objects):
        self.all_story_objects = all_story_objects
        self.context_objects = []
        self.current_context = None

    # Context calls this to know how to fill a piece of context.
    def get_overview(self):
        raise Exception('this is not written yet.')
    
    def create_txt(self):
        raise Exception('not written yet.')

# create and store Story objects.
folder = 'stories'
paths = [f'{folder}/{f}' for f in os.listdir(folder)]
story_strings = list(map(text_read, paths))
story_objects = []
for s in story_strings:
    s_o = Story(s)
    story_objects.append(s_o)
training_data = TrainingData(story_objects)

# this is where all the magic happens, huehueheuehueh
context_size = int(round(1.2*max([len(tokenize(o.string)) for o in story_objects]), 0))
loop_counter = 0
while True:
    print(f'loop_counter:{loop_counter}')

    # continue current context, or make a new one
    pass

    # get next story
    pass
    
    # add story to context
    pass
    
    loop_counter += 1

# create txt file and do final check
res = ''.join(training_data.create_txt)
text_create('training_data.txt', res)
if not len(tokenize(res)) == context_size*len(training_data.chunks):
    raise Exception('final token count went wrong')

# log the end
logging.info('===== ===== =====')
logging.info('===== ===== =====')
logging.info('===== program finished =====')
logging.info('===== ===== =====')
logging.info('===== ===== =====')