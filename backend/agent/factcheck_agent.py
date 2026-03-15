import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.tools.news_search_tool import search_news
from backend.tools.rag_tool import retrieve_documents
from backend.prompts.factcheck_prompt import FACTCHECK_PROMPT

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)


def extract_text(response):
    """
    Extract clean text from Gemini response.
    """
    if hasattr(response, "content"):

        if isinstance(response.content, str):
            return response.content

        if isinstance(response.content, list):
            text_parts = []
            for item in response.content:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
            return "\n".join(text_parts)

    return str(response)


def factcheck_claim(claim):

    news_results = search_news(claim)

    rag_results = retrieve_documents(claim)

    prompt = FACTCHECK_PROMPT.format(
        claim=claim,
        search_results=news_results,
        rag_results=rag_results
    )

    response = llm.invoke(prompt)

    clean_text = extract_text(response)

    return clean_text