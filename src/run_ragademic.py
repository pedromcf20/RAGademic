import logging
import os

from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

from utils.arxiv_utils import fetch_arxiv_papers
from utils.chain_utils import invoke_rag_chain, setup_rag_chain
from utils.db_utils import initialize_chroma
from utils.llm_utils import initialize_chat_model
from utils.logging_utils import setup_logging
from utils.preprocessing_utils import load_documents, split_documents

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_academic_rag_chain(arxiv_search_query: str):
    """
    Processes an academic search query returns Retrieval Augmented Generation chain.

    This function executes several steps:
    1. Loads the OpenAI API key from environment variables.
    2. Initializes OpenAI embeddings with the API key.
    3. Fetches academic papers from arXiv based on the provided search query.
    4. Loads these papers as documents and splits them into smaller chunks.
    5. Initializes a GPT-3.5 turbo model and a Chroma vector store with the document splits.
    6. Sets up a Retrieval Augmented Generation (RAG) chain using the configured Chroma vector store.

    Parameters:
    arxiv_search_query (str): The search query for fetching academic papers from arXiv.

    Returns:
    rag_chain: The answer generated by the RAG chain.

    Raises:
    ValueError: If the OpenAI API key is not found in the environment variables.
    """

    # Load environment variables, specifically the OpenAI API key
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")

    # Initialize OpenAI embeddings using the API key
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Fetch academic papers from arXiv using a specified search query
    downloaded_papers = fetch_arxiv_papers(arxiv_search_query)

    # Load the downloaded papers as documents
    docs = load_documents(downloaded_papers)

    # Split the loaded documents into smaller text chunks for processing
    splits = split_documents(docs)

    # Initialze LLM - gpt-3.5 turbo
    llm = initialize_chat_model(api_key, "gpt-3.5-turbo", 0)

    # Initialize a Chroma vector store using the document splits
    vectordb = initialize_chroma(splits, embeddings)
    retriever = vectordb.as_retriever()

    # Set up a Retrieval Augmented Generation (RAG) chain using the configured Chroma vector store
    rag_prompt_custom = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum and keep the answer as concise as possible. 
        Always say "thanks for asking!" at the end of the answer. 
        {context}
        Question: {question}
        Helpful Answer:"""
    
    # Initialize rag chain
    rag_chain = setup_rag_chain(llm, retriever, rag_prompt_custom)

    return rag_chain


def perform_retrieval_augmented_generation(rag_chain, question: str) -> str:
    """
    Invokes a pre-initialized Retrieval Augmented Generation (RAG) chain with a specified question 
    and returns the generated answer.

    This function takes a RAG chain object, which is expected to be already configured with necessary
    components like a language model and a document retriever. It then uses this RAG chain to process
    the provided question and generate an answer.

    Parameters:
    rag_chain: The pre-initialized RAG chain object used for generating answers.
               The exact type of this parameter depends on how the RAG chain is implemented.
    question (str): The question to be answered by the RAG chain.

    Returns:
    str: The answer generated by the RAG chain for the given question.
    """
    
    # Invoke the RAG chain with the question
    answer = invoke_rag_chain(rag_chain, question)

    return answer


def main()->None:
    """
    Main function to handle the user interaction for continuous question-answering using a RAG chain.

    This function performs the following steps:
    1. Prompts the user to input an arXiv search query.
    2. Initializes a RAG chain with the provided search query.
    3. Enters an interactive loop where the user can ask questions.
    4. Uses the initialized RAG chain to generate answers to the user's questions.
    5. Allows the user to exit the loop and the program by typing 'exit' or 'quit'.

    The function does not accept any parameters and does not return any value.
    """

    setup_logging()
    logging.info("Starting the RAG application.")

    # User inputs the arXiv search query once
    arxiv_search_query = input("Enter the arXiv search query: ")

    # Initialize the RAG chain with the given search query
    rag_chain = initialize_academic_rag_chain(arxiv_search_query)

    print("Enter your questions to the model. Type 'exit' to quit.")

    while True:
        # User inputs their question
        question = input("Enter your question: ")

        # Check for exit condition
        if question.lower() in ['exit', 'quit']:
            break

        # Get the answer from the RAG chain
        answer = perform_retrieval_augmented_generation(rag_chain, question)

        # Display the answer
        print("Answer:", answer)
    
    logging.info("Exiting the RAG application.")

if __name__ == "__main__":
    main()