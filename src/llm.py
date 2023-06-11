from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
import os
from getpass import getpass

###### GLOBALS
docsDir = ''
qa = ''

####### FUNCTIONS
def setOpenApiKey(openApiKey):
    print("setOpenApiKey")
    try:
        OPENAI_API_KEY = openApiKey
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    except:
        print("Invalid key. Please try again.")
    init()
    return True

def pdfLoader(path):
    print("Startng pdfLoader")
    from langchain.document_loaders import PyPDFLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    loader = PyPDFLoader(path)
    documents = loader.load_and_split()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":2})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
    return qa

def directoryLoader(path):
    print("directoryLoader")
    # Documentation : https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/directory_loader.html
    loader = DirectoryLoader(path)
    documents = loader.load()
    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    from langchain.embeddings import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings()
    from langchain.vectorstores import Chroma
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
    return qa

def init():
    print("init")
    global docsDir
    docsDir = 'docs/'
    global qa
    qa = directoryLoader(docsDir)
    #qa = pdfLoader("pdf/test.pdf")

def askQuestion(query):
    # TXT
    returnString = qa.run(query)
    # PDF
    # output = qa({"query": query})
    # returnString = str(output['result'])
    return returnString