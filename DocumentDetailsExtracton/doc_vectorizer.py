import os
import base64
from io import BytesIO
import filetype
from pdf2image import convert_from_path

from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from .prompts import image_prompt  # Make sure this exists

# --- Utility Functions ---

def get_filename(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def file_router(file):
    kind = filetype.guess(file)
    if kind is None:
        return "Unknown"

    file_type = kind.mime

    if file_type.startswith("image/"):
        return 'imagesingle'

    loader = PyPDFLoader(file)
    docs = loader.load()

    if not len(docs[0].page_content):
        return 'imagepdf'
    else:
        return 'pdf'

def encode_image(image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# --- LLM Setup ---

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

def image_summarize(model, base64_image: str, prompt: str) -> str:
    msg = model.invoke([
        HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
            ]
        )
    ])
    return msg.content

# --- Image Handlers ---

def image_handler(image):
    base64_img = encode_image(image)
    summary = image_summarize(model, base64_img, prompt=image_prompt)
    with open('example.txt', 'w') as f:
        f.write(summary)
    return summary

def image_handler_append(image):
    base64_img = encode_image(image)
    summary = image_summarize(model, base64_img, prompt=image_prompt)
    with open('example.txt', 'a') as f:
        f.write(summary + '\n')
    return summary

# --- Vectorization Functions ---

def vectorize_text(text: str, company_name: str, filename: str = "text_input"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    docs = splitter.split_text(text)
    persist_directory = os.path.join("chroma_store", company_name, filename)

    vectorstore = Chroma.from_texts(
        docs,
        embedding=HuggingFaceEmbeddings(),
        persist_directory=persist_directory
    )
    # Remove persist() call - Chroma auto-persists when persist_directory is specified
    return vectorstore

def vectorize_single_image(image, company_name: str):
    summary = image_handler(image)
    filename = "image_single"
    return vectorize_text(summary, company_name, filename)

def vectorize_multiple_images(image_path: str, company_name: str):
    images = convert_from_path(image_path)
    filename = get_filename(image_path)
    summary = ''

    for i, image in enumerate(images):
        if i == 0:
            summary = image_handler(image)
        else:
            summary += image_handler_append(image)

    return vectorize_text(summary, company_name, filename)

def vectorize_docs(filepath: str, company_name: str):
    loader = PyPDFLoader(filepath)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = splitter.split_documents(docs)
    filename = get_filename(filepath)
    persist_directory = os.path.join("chroma_store", company_name, filename)

    vectorstore = Chroma.from_documents(
        chunks,
        HuggingFaceEmbeddings(),
        persist_directory=persist_directory
    )
    # Remove persist() call - Chroma auto-persists when persist_directory is specified
    return vectorstore

# --- Entry Point for Routing ---

def vectorize(filepath: str, company_name: str):
    file_type = file_router(filepath)
    print(f"Detected file type: {file_type}")

    if file_type == 'imagesingle':
        return vectorize_single_image(filepath, company_name)
    elif file_type == 'imagepdf':
        return vectorize_multiple_images(filepath, company_name)
    else:
        return vectorize_docs(filepath, company_name)


