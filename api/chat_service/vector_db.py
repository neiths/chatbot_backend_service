from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import TextLoader
import psycopg2
from dotenv import load_dotenv
load_dotenv()

""" 
1. load document
there are many ways to load a document
2. text split
3. load embeddings model
4. connect to vector database
5. store vector to db
6. query vector from db by retrieve (sematic) nearest neighbors
"""

loader = PyPDFLoader("sample.pdf")
pages = loader.load_and_split()

# connect database
CONNECTION_STRING = "postgresql+psycopg2://postgres:thien@localhost:5432/pg_langchain"
COLLECTION_NAME = "sample_collection"

# embedding model
#embeddings_model = AnyscaleEmbeddings()
embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")


vector_store = PGVector(
    connection=CONNECTION_STRING,
    embeddings=embeddings_model,
    collection_name=COLLECTION_NAME
)

def store_data_to_db(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    docs_only_text = [pages[8].page_content, pages[9].page_content, pages[10].page_content, pages[11].page_content]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.create_documents(docs_only_text)
    # print(docs)
    vector_store.add_documents(texts, id=[idx for idx in range(len(texts))])


retriever = vector_store.as_retriever(search_kwargs={"k": 1})
