from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import shutil

DATA_PATH = "data/6.006"
CHROMA_PATH = "chroma"

def generate_vector_store():
    documents = load_documents()
    chunks = chunk_text(documents)
    save_to_chroma(chunks)


def load_documents():
    '''
    This function load each markdown file and turn it into a "document"
    containing all the content (text) in the file and metadata (e.g the name
    of the source file where the text originally came from).

    A loaded document can be very long though, so split it up into smaller "chunks"
    where each one will be more focused and relevant to what we're querying. 
    '''
    loader = DirectoryLoader(DATA_PATH)
    documents = loader.load()
    return documents


def chunk_text(documents: list[Document]):
    '''
    A loaded document can be very long though, so split it up into smaller "chunks"
    where each one will be more focused and relevant to what we're querying. 
    '''
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,    # Set size to number of characters [controlled for chunk size -- same size as implemented in the Weaviate backend]
        chunk_overlap=1000,  # Size of the overlap between each chunk
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    #random_document = chunks[15]
    #print(random_document.page_content)
    #print(random_document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    '''
    Create a Chroma database from the chunks. Will use the OpenAI embeddings function to generate the vector 
    embeddings for each chunk.
    '''
    # Clear any previous version of the database
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create new DB
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-large")
    db = Chroma.from_documents(
        chunks, embedding_function, persist_directory=CHROMA_PATH   # Save it to disk
    )
    # DB should save automatically, but this persist method will manually ensure it does if error occurs
    # db.persist()    
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


generate_vector_store()