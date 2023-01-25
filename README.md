# NAI-chonky (in development)
- chunking algorithm for NAI modules
- conversation that made me start this project: https://discord.com/channels/836774308772446268/837402685824565278/1066498372132950087
- the basic idea is, create module training data in such a way that the module learns that each context starts with metadata
  + simulating having metadata in Memory, in a NovelAI story.
  + the hard part is to create chunks of exactly 256-token-multiples, to have precise control over how each chunk looks.
- ![Screenshot_1](https://user-images.githubusercontent.com/112716905/214617548-5f6d65e9-fc6e-4a4c-b3f3-4955fe9451fd.png)

