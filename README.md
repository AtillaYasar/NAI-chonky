# NAI-chonky (in development)
- chunking algorithm for NAI modules
- conversation that made me start this project: https://discord.com/channels/836774308772446268/837402685824565278/1066498372132950087
- the basic idea is, create module training data in such a way that the module learns that each context starts with metadata
  + simulating having metadata in Memory, in a NovelAI story.
  + the hard part is to create chunks of exactly 256-token-multiples, to have precise control over how each chunk looks.
- ![Screenshot_1](https://user-images.githubusercontent.com/112716905/214617548-5f6d65e9-fc6e-4a4c-b3f3-4955fe9451fd.png)

## progress updates
- from jan 27th, when thinking about the app:
  + ![chonky updates 27](https://user-images.githubusercontent.com/112716905/214974378-d609e812-058c-4ba7-9a10-e1b920b54c92.png)
- jan 31st:
  + uploaded main.py, which is the beginning of a refactor.
  + "why on earth would you upload the *beginning* of a refactor?"
    - "idk."
  + i had a solution with the simplifying assumptions of, "every story is bigger than the total context size, and you only put the part of the story inside the context that fits, and discard the rest".
    - then tried to expand on that solution by removing making the context size bigger than the biggest story (so that the program has to account for multiple stories in a context), but the code was too messy and very frustrating to work with, so i started a refactor.
  + state of classes right now:
    - ![classes](https://user-images.githubusercontent.com/112716905/216024724-9c0f0640-cacb-467d-b52d-19585fa4f699.png)
