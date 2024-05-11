import argparse
from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the following question based only on the above context: {question}
"""

def QA():
    '''
    When querying for relevant data, we want to find the chunks in our database that most likely
    contain the answer to the question we want to ask. We will use a LLM to generator vectors from words and then 
    calculate their relevance.
    '''
    # Set up a command line interface using Python's argparse module
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Load the Chroma DB created after running database.py
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-large")     # Use the same embedding function used to create the DB with
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the database -- results will be a list of tuples in the form (chunk, relevance score)
    results = db.similarity_search_with_relevance_scores(query_text, k=3)   # Retrieve the top 3 most relevant chunks to the query
    if len(results) == 0:    # Ensure relevant information is retrieved (threshold has been tinkered around with)
        print(f"Unable to find matching results.")
        return 
    
    context_text = "\n\n---\n\n".join([chunk.page_content for chunk, score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)  # Format the template with variables holding the query and context
    
    # Print the content for each of the k most relevant documents (chunks) identified
    # print(prompt)       


    # Call OpenAI LLM model with the prompt to obtain the answer
    model = ChatOpenAI(model="gpt-4-0125-preview")
    response_text = model.predict(prompt)

    # Provide a reference to the material sourced before printing
    sources = [doc.metadata.get("source", None) for doc, score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    

QA()










