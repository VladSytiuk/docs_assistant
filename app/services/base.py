from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


class BaseService:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=OpenAIEmbeddings(),
        )
