from database.vector_store import load_vector_store


def retrieve_documents(query):

    vectordb = load_vector_store()

    retriever = vectordb.as_retriever()

    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    return context