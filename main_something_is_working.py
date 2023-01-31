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
        d = {
            'type':'Meta',
            f'first {n} chars':self.string[:n]
        }
        # return json.dumps(d, indent=2)
        return d['type'] + ' object' + '\n' + d[f'first {n} chars']

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
        d = {
            'type':'Meta',
            f'first {n} chars':self.string[:n]
        }
        # return json.dumps(d, indent=2)
        return d['type'] + ' object' + '\n' + d[f'first {n} chars']

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

    def get_overview(self):
        def check_added(story_object):
            # iterate over context_objects, check if this story_object is in any of them
            for c in self.context_objects:
                if story_object in c.objects:
                    return True
            return False

        # iterate over story_objects, find which ones havent been included in a context yet.
        unadded = []
        for s in self.all_story_objects:
            if check_added(s) == False:
                unadded.append(s)
        finished = True if unadded == [] else False
        return {'unadded':unadded, 'finished':finished}

    def create_txt(self):
        chunks = []
        for c in self.context_objects:
            this_chunk = []
            for o in c.objects:
                this_chunk.append(o.string)
            chunks.append(''.join(this_chunk))
        return ''.join(chunks)

# create and store Story objects.
folder = 'stories'
paths = [f'{folder}/{f}' for f in os.listdir(folder)]
story_strings = list(map(text_read, paths))
story_objects = []
for p in paths:
    string = text_read(p)
    meta = f'[ the path to this file is:{p} ]\n'
    s_o = Story(string=string, custom_meta=meta)
    story_objects.append(s_o)
training_data = TrainingData(story_objects)

# this is where all the magic happens, huehueheuehueh
context_size = int(round(1.2*max([len(tokenize(o.string)) for o in story_objects]), 0))
# add the first context object, to start off the process
c = Context(context_size)
training_data.context_objects.append(c)
training_data.current_context = c

# returns an ansi escape sequence to color a string.  (ft is "first two", s is "string")
def col(ft, s):
    # black-30, red-31, green-32, yellow-33, blue-34, magenta-35, cyan-36, white-37
    u = '\u001b'
    numbers = dict([(string,30+n) for n, string in enumerate(('bl','re','gr','ye','blu','ma','cy','wh'))])
    n = numbers[ft]
    return f'{u}[{n}m{s}{u}[0m'

# prints stuff about the training data with pretty colors and indentation.
def for_terminal():
    lines = []
    ind = ' '*4
    ind_level = 0
    lines.append(col('ye', '--- for_terminal start ---'))
    for cn, c in enumerate(training_data.context_objects):
        ind_level = 1
        lines.append(f'{ind*ind_level}context number {col("cy",cn)}')
        for on, o in enumerate(c.objects):
            ind_level = 2
            lines.append(f'{ind*ind_level}object number {col("gr",on)}')
            ind_level = 3
            lines.append('\n'.join([f'{ind*ind_level}{line}' for line in str(o).split('\n')]))
    lines.append(col('ye', '--- for_terminal end ---'))
    return '\n'.join(lines)

loop_counter = 0
while True:
    print(f'loop_counter:{loop_counter}')
    print(for_terminal())

    # continue with current context, or make a new one
    if training_data.current_context.complete == True:
        # make a new one
        new_context = Context(context_size)
        training_data.current_context = new_context
        curc = training_data.current_context
        training_data.context_objects.append(curc)
    else:
        curc = training_data.current_context

    # get next story
    overview = training_data.get_overview()
    if overview['finished'] == True:
        print(col('ma', 'done with loop'))
        print(for_terminal())
        break
    next_story = overview['unadded'][0]
    
    # add story to context  (will add the associated metadata as well)
    curc.add_story(next_story)

    # check how full context is
    space_used = sum([len(tokenize(o.string)) for o in curc.objects])
    if space_used > curc.size:
        # shrink the latest story object to make it fit
        last_story = curc.objects[-1]
        current_size = len(tokenize(last_story.string))
        excess = space_used - curc.size
        new_size = current_size - excess
        if new_size < 0:
            raise Exception('new_size is negative. cant shrink to negative sizes bruv.')

        curc.objects[-1].shrink(new_size)
        curc.complete = True
    elif space_used < curc.size:
        pass
    else:
        curc.complete = True
    
    loop_counter += 1

# create txt file and do final check
res = training_data.create_txt()
text_create('training_data.txt', res)

print(f'context size: {context_size}')
for n, c in enumerate(training_data.context_objects):
    chunk = []
    for o in c.objects:
        chunk.append(o.string)
    text = ''.join(chunk)
    count = len(tokenize(text))
    text_create(f'chunk number {n}.txt', text)
    print(f'context number: {n}, token count {count}')

# log the end
logging.info('===== ===== =====')
logging.info('===== ===== =====')
logging.info('===== program finished =====')
logging.info('===== ===== =====')
logging.info('===== ===== =====')
