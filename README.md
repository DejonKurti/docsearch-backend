# DocSearch Backend

This is an alternative implementation of the backend used in **6.S079 [Software Systems for Data Science]** by the DocSearch team for their final project. With the same goal of delivering a Question-Answer service that helps students locate where in their class files specific material lies (as well as answer questions on the class material itself), this implementation utilizes Chroma DB, LangChain, and OpenAI models. Ultimately, we compare this to the Weaviate backend through benchmarking to understand the system's advantages/disadvantages.

## Installation

```
pip install -r requirements.txt
```

## Usage

Create the Chroma DB Vector Store.

```
python database.py
```

Submit a query to the DB.

```
python prompt.py "<insert your question here>"
```
