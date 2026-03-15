from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from database.vector_store import load_vector_store


def ingest():

    loader = DirectoryLoader(
        "data/trusted_sources",
        glob="**/*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    vectordb = load_vector_store()

    vectordb.add_documents(docs)

    vectordb.persist()

    print("Documents ingested successfully")


if __name__ == "__main__":
    ingest()