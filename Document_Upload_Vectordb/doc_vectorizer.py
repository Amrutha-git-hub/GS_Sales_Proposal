import os
import base64
from io import BytesIO
import filetype
from pdf2image import convert_from_path
from datetime import datetime
import hashlib

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

def get_file_hash(file_path):
    """Generate SHA-256 hash of file for duplicate detection"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return None

def create_base_metadata(file_path, company_name, file_type):
    """Create base metadata common to all file types"""
    timestamp = datetime.now().isoformat()
    
    metadata = {
        'company_name': company_name,
        'file_type': file_type,
        'filename': os.path.basename(file_path) if isinstance(file_path, str) else 'uploaded_image',
        'file_path': file_path if isinstance(file_path, str) else None,
        'processed_timestamp': timestamp,
        'processing_date': datetime.now().strftime('%Y-%m-%d'),
        'processing_time': datetime.now().strftime('%H:%M:%S'),
        'chunk_strategy': 'recursive_character_text_splitter',
        'embedding_model': 'huggingface_default'
    }
    
    # Add file-specific metadata if it's a file path
    if isinstance(file_path, str) and os.path.exists(file_path):
        metadata.update({
            'file_hash': get_file_hash(file_path),
            'file_size_bytes': get_file_size(file_path),
            'file_extension': os.path.splitext(file_path)[1].lower()
        })
    
    return metadata

def file_router(file):
    try:
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
    except Exception as e:
        print(f"Error in file_router: {e}")
        return 'pdf'  # Default fallback

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

# --- Enhanced Vectorization Functions ---

def vectorize_text(text: str, company_name: str, filename: str = "text_input", base_metadata: dict = None):
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
        docs = splitter.split_text(text)
        
        # Create persist directory
        persist_directory = os.path.join("chroma_store", company_name, filename)
        os.makedirs(persist_directory, exist_ok=True)
        
        # Create collection name (sanitize company name)
        collection_name = f"{company_name}_{filename}".replace(" ", "_").replace("-", "_").lower()
        
        # Create metadata for each chunk
        metadatas = []
        for i, chunk in enumerate(docs):
            chunk_metadata = base_metadata.copy() if base_metadata else {}
            chunk_metadata.update({
                'chunk_index': i,
                'chunk_size': len(chunk),
                'total_chunks': len(docs),
                'content_type': 'text',
                'source_document': filename
            })
            metadatas.append(chunk_metadata)
        
        vectorstore = Chroma.from_texts(
            texts=docs,
            embedding=HuggingFaceEmbeddings(),
            metadatas=metadatas,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        return vectorstore
        
    except Exception as e:
        print(f"Error in vectorize_text: {e}")
        # Fallback to in-memory store
        metadatas = [{'error': str(e), 'fallback': True} for _ in docs]
        vectorstore = Chroma.from_texts(
            texts=docs,
            embedding=HuggingFaceEmbeddings(),
            metadatas=metadatas,
            collection_name=f"fallback_{collection_name}"
        )
        return vectorstore

def vectorize_single_image(image, company_name: str):
    try:
        # Create base metadata for image
        base_metadata = create_base_metadata(image, company_name, 'single_image')
        base_metadata.update({
            'content_source': 'ai_image_summary',
            'ai_model_used': 'gemini-2.0-flash',
            'processing_method': 'image_to_text_summary'
        })
        
        summary = image_handler(image)
        filename = "image_single"
        return vectorize_text(summary, company_name, filename, base_metadata)
    except Exception as e:
        print(f"Error in vectorize_single_image: {e}")
        error_metadata = {'error': str(e), 'file_type': 'single_image'}
        return vectorize_text("Error processing image", company_name, "error_image", error_metadata)

def vectorize_multiple_images(image_path: str, company_name: str):
    try:
        images = convert_from_path(image_path)
        filename = get_filename(image_path)
        
        # Create base metadata
        base_metadata = create_base_metadata(image_path, company_name, 'pdf_images')
        base_metadata.update({
            'total_pages': len(images),
            'content_source': 'ai_image_summary',
            'ai_model_used': 'gemini-2.0-flash',
            'processing_method': 'pdf_to_images_to_text',
            'conversion_tool': 'pdf2image'
        })
        
        summary = ''
        for i, image in enumerate(images):
            if i == 0:
                summary = image_handler(image)
            else:
                summary += image_handler_append(image)

        return vectorize_text(summary, company_name, filename, base_metadata)
    except Exception as e:
        print(f"Error in vectorize_multiple_images: {e}")
        error_metadata = {'error': str(e), 'file_type': 'pdf_images'}
        return vectorize_text("Error processing PDF images", company_name, "error_pdf_images", error_metadata)

def vectorize_docs(filepath: str, company_name: str):
    try:
        loader = PyPDFLoader(filepath)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
        chunks = splitter.split_documents(docs)
        filename = get_filename(filepath)
        
        # Create base metadata
        base_metadata = create_base_metadata(filepath, company_name, 'pdf_document')
        base_metadata.update({
            'total_pages': len(docs),
            'total_chunks_created': len(chunks),
            'chunk_size': 600,
            'chunk_overlap': 80,
            'content_source': 'direct_pdf_text',
            'loader_used': 'PyPDFLoader'
        })
        
        # Create persist directory
        persist_directory = os.path.join("chroma_store", company_name, filename)
        os.makedirs(persist_directory, exist_ok=True)
        
        # Create collection name (sanitize)
        collection_name = f"{company_name}_{filename}".replace(" ", "_").replace("-", "_").lower()
        
        # Add metadata to each chunk
        for i, chunk in enumerate(chunks):
            chunk.metadata.update(base_metadata)
            chunk.metadata.update({
                'chunk_index': i,
                'page_number': chunk.metadata.get('page', 'unknown'),
                'chunk_char_count': len(chunk.page_content)
            })
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=HuggingFaceEmbeddings(),
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        return vectorstore
        
    except Exception as e:
        print(f"Error in vectorize_docs: {e}")
        # Fallback to in-memory store
        try:
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
            chunks = splitter.split_documents(docs)
            
            # Add error metadata to fallback
            error_metadata = {'error': str(e), 'fallback': True, 'file_type': 'pdf_document'}
            for chunk in chunks:
                chunk.metadata.update(error_metadata)
            
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=HuggingFaceEmbeddings(),
                collection_name=f"fallback_{company_name}_{filename}".replace(" ", "_").lower()
            )
            return vectorstore
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            # Return minimal vectorstore
            return Chroma.from_texts(
                texts=["Error loading document"],
                embedding=HuggingFaceEmbeddings(),
                metadatas=[{'error': str(fallback_error), 'critical_failure': True}],
                collection_name="error_fallback"
            )

# --- Entry Point for Routing ---

def vectorize(filepath: str, company_name: str):
    try:
        file_type = file_router(filepath)
        print(f"Detected file type: {file_type}")

        if file_type == 'imagesingle':
            return vectorize_single_image(filepath, company_name)
        elif file_type == 'imagepdf':
            return vectorize_multiple_images(filepath, company_name)
        else:
            return vectorize_docs(filepath, company_name)
            
    except Exception as e:
        print(f"Error in vectorize main function: {e}")
        # Ultimate fallback with comprehensive error metadata
        error_metadata = {
            'error': str(e),
            'critical_failure': True,
            'processed_timestamp': datetime.now().isoformat(),
            'company_name': company_name,
            'attempted_file': filepath
        }
        return Chroma.from_texts(
            texts=[f"Error processing file: {str(e)}"],
            embedding=HuggingFaceEmbeddings(),
            metadatas=[error_metadata],
            collection_name="ultimate_fallback"
        )

# --- Utility Functions for Metadata Queries ---

def search_by_metadata(vectorstore, metadata_filter: dict, query: str = None, k: int = 5):
    """Search documents using metadata filters"""
    try:
        if query:
            # Similarity search with metadata filter
            results = vectorstore.similarity_search(
                query=query, 
                k=k, 
                filter=metadata_filter
            )
        else:
            # Get all documents matching metadata filter
            results = vectorstore.get(where=metadata_filter, limit=k)
        return results
    except Exception as e:
        print(f"Error in metadata search: {e}")
        return []

def get_document_metadata_summary(vectorstore):
    """Get a summary of all metadata in the vectorstore"""
    try:
        # This would need to be implemented based on your specific Chroma setup
        # You might need to query the underlying collection directly
        collection = vectorstore._collection
        all_data = collection.get()
        
        if all_data and 'metadatas' in all_data:
            return {
                'total_documents': len(all_data['metadatas']),
                'unique_companies': set(meta.get('company_name') for meta in all_data['metadatas'] if meta.get('company_name')),
                'file_types': set(meta.get('file_type') for meta in all_data['metadatas'] if meta.get('file_type')),
                'processing_dates': set(meta.get('processing_date') for meta in all_data['metadatas'] if meta.get('processing_date'))
            }
    except Exception as e:
        print(f"Error getting metadata summary: {e}")
        return None