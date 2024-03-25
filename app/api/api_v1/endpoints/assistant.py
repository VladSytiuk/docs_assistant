from fastapi import APIRouter, UploadFile, File

from app.services.assistant import assistant
from app.schemas.assistant import Question


router = APIRouter(prefix="/assistant")


@router.post("/send-question")
async def send_question(question: Question):
    answer = await assistant.process_question(question.question)
    return {"message": answer}


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    await assistant.upload_document(file)
    return {"info": f"file '{file.filename}' saved"}
