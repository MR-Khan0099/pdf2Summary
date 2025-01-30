# import os
# import shutil
# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import FileResponse
# from backend.utils.extract_pdf import extract_text_from_pdf
# from backend.models.huggingface_models import summarize_with_huggingface
# from backend.models.gpt import summarize_with_gpt
# from fastapi.middleware.cors import CORSMiddleware
# from backend.utils.save_pdf import save_summary_to_pdf

# # from models.deepseek import summarize_with_deepseek

# app = FastAPI()

# # CORS middleware to handle requests from different origins (for development purposes)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins (for development)
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# # Set a temporary directory for storing uploaded files
# UPLOAD_DIRECTORY = "/tmp/uploads"
# # Create the directory if it doesn't exist
# os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...), model: str = "bart"):
#     try:
#         # Save the uploaded file to a temporary location
#         file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Extract text from the PDF
#         text = extract_text_from_pdf(file_path)
        
#         # Summarize the text using the selected model
#         if model == "gpt":
#             summary = summarize_with_gpt(text)
      
#         # elif model == "deepseek":
#         #     summary = summarize_with_deepseek(text)
#         else:
#             summary = summarize_with_huggingface(model, text)

#         # Optionally delete the file after processing
#         os.remove(file_path)

#         # Save summary to PDF
#         pdf_filename = save_summary_to_pdf(summary, file.filename)

#         # Return the summary and the PDF filename (URL) for downloading
#         return {
#             "summary": summary,
#             "pdf_filename": pdf_filename
#         }

#     except Exception as e:
#         # Handle errors and provide feedback to the user
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from backend.utils.extract_pdf import extract_text_from_pdf
from backend.models.huggingface_models import summarize_with_huggingface
from backend.models.gpt import summarize_with_gpt
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.save_pdf import save_summary_to_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Set a temporary directory for storing uploaded files
UPLOAD_DIRECTORY = "/tmp/uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Store the summary temporarily in memory
summaries = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), model: str = "bart"):
    try:
        # Save the uploaded file to a temporary location
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from the PDF
        text = extract_text_from_pdf(file_path)
        
        # Summarize the text using the selected model
        if model == "gpt":
            summary = summarize_with_gpt(text)
        else:
            summary = summarize_with_huggingface(model, text)

        # Optionally delete the file after processing
        os.remove(file_path)

        # Save the summary temporarily in memory (using filename as the key)
        summaries[file.filename] = summary

        # Return the summary text to display on the frontend
        return {"summary": summary, "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/download_pdf")
async def download_pdf(summary: str, filename: str):
    # Save the summary to a PDF
    pdf_filename = save_summary_to_pdf(summary, filename)
    
    # Return the PDF file as a download
    return FileResponse(pdf_filename, media_type='application/pdf', filename=pdf_filename)
    