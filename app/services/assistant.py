import shutil

from fastapi import File
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.errors.app_errors import UnsupportedFileExtensionError
from app.services.base import BaseService
from app.services.prompts import ASSISTANT_PROMPT


class AssistantService(BaseService):
    QA_CHAIN_PROMPT = PromptTemplate.from_template(ASSISTANT_PROMPT)

    async def process_question(self, question: str) -> str:
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 1}),
            chain_type_kwargs={"prompt": self.QA_CHAIN_PROMPT},
        )
        answer = qa_chain({"query": question})
        return answer["result"]

    async def upload_document(self, file: File) -> None:
        if not self._is_pdf(file):
            raise UnsupportedFileExtensionError()

        file_path = f"app/documents/{file.filename}"

        with open(file_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        row_document = PyPDFium2Loader(file_path).load()
        chunks = await self._split_document(row_document)
        await self._store_documents(chunks)

    @staticmethod
    async def _split_document(raw_document: list) -> list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=20
        )
        chunks = text_splitter.split_documents(raw_document)
        return chunks

    @staticmethod
    async def _store_documents(chunked_documents: list) -> None:
        Chroma.from_documents(
            chunked_documents,
            OpenAIEmbeddings(),
            persist_directory="./chroma_db",
        )

    @staticmethod
    def _is_pdf(file: File) -> bool:
        extension = file.filename.split(".")[-1].lower()
        return extension == "pdf"


assistant = AssistantService()
