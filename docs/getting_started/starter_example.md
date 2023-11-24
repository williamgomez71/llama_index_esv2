# Starter Tutorial

```{tip}
Make sure you've followed the [installation](installation.md) steps first.
```

This is our famous "5 lines of code" starter example.

## Download data

This example uses the text of Paul Graham's essay, ["What I Worked On"](http://paulgraham.com/worked.html). This and many other examples can be found in the `examples` folder of our repo.

The easiest way to get it is to [download it via this link](https://raw.githubusercontent.com/run-llama/llama_index/main/examples/paul_graham_essay/data/paul_graham_essay.txt) and save it in a folder called `data`.

## Set your OpenAI API key

LlamaIndex uses OpenAI's `gpt-3.5-turbo` by default. Make sure your API key is available to your code by setting it as an environment variable. In MacOS and Linux, this is the command:

```
export OPENAI_API_KEY=XXXXX
```

and on windows it is

```
set OPENAI_API_KEY=XXXXX
```

## Load data and build an index

In the same folder where you created the `data` folder, create a file called `starter.py` file with the following:

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
```

This builds an index over the documents in the `data` folder (which in this case just consists of the essay text, but could contain many documents).

Your directory structure should look like this:

<pre>
├── starter.py
└── data
    └── paul_graham_essay.txt
</pre>

## Query your data

Add the following lines to `starter.py`

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
```

This creates an engine for Q&A over your index and asks a simple question. You should get back a response similar to the following: `The author wrote short stories and tried to program on an IBM 1401.`

## Viewing Queries and Events Using Logging

Want to see what's happening under the hood? Let's add some logging. Add these lines to the top of `starter.py`:

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
```

You can set the level to `DEBUG` for verbose output, or use `level=logging.INFO` for less.

## Storing your index

By default, the data you just loaded is stored in memory as a series of vector embeddings. You can save time (and requests to OpenAI) by saving the embeddings to disk. That can be done with this line:

```python
index.storage_context.persist()
```

By default, this will save the data to the directory `storage`, but you can change that by passing a `persist_dir` parameter.

Of course, you don't get the benefits of persisting unless you load the data. So let's modify `starter.py` to generate and store the index if it doesn't exist, but load it if it does:

```python
import os.path
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# check if storage already exists
if not os.path.exists("./storage"):
    # load the documents and create the index
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist()
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

# either way we can now query the index
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
```

Now you can efficiently query to your heart's content! But this is just the beginning of what you can do with LlamaIndex.

```{admonition} Next Steps
* learn more about the [high-level concepts](/getting_started/concepts.md).
* tell me how to [customize things](/getting_started/customization.rst).
* curious about a specific module? check out the guides on the left 👈
```
