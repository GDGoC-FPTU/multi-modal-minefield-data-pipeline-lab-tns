import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
        
    # Thay đổi model name để tránh lỗi 404 trên các phiên bản API cũ
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print(f"Uploading {file_path} to Gemini...")
    try:
        pdf_file = genai.upload_file(path=file_path)
    except Exception as e:
        print(f"Failed to upload file to Gemini: {e}")
        return None
        
    prompt = """
Analyze this document and extract a summary and the author. 
Output exactly as a JSON object matching this exact format:
{
    "document_id": "pdf-doc-001",
    "content": "Summary: [Insert your 3-sentence summary here]",
    "source_type": "PDF",
    "author": "[Insert author name here]",
    "timestamp": null,
    "source_metadata": {"original_file": "lecture_notes.pdf"}
}
"""
    
    print("Generating content from PDF using Gemini...")
    response = model.generate_content([pdf_file, prompt])
    content_text = response.text or ""
    
    # Simple cleanup if the response is wrapped in markdown json block
    if content_text.startswith("```json"):
        content_text = content_text[7:]
    if content_text.endswith("```"):
        content_text = content_text[:-3]
    if content_text.startswith("```"):
        content_text = content_text[3:]
        
    try:
        extracted_data = json.loads(content_text.strip())
    except json.JSONDecodeError:
        return {
            "document_id": "pdf-doc-001",
            "content": f"Raw Gemini response: {content_text.strip()}",
            "source_type": "PDF",
            "author": "Unknown",
            "timestamp": None,
            "source_metadata": {"original_file": os.path.basename(file_path), "parse_error": True},
        }

    extracted_data.setdefault("document_id", "pdf-doc-001")
    extracted_data.setdefault("source_type", "PDF")
    extracted_data.setdefault("author", "Unknown")
    extracted_data.setdefault("timestamp", None)
    extracted_data.setdefault("source_metadata", {"original_file": os.path.basename(file_path)})
    if isinstance(extracted_data["source_metadata"], dict):
        extracted_data["source_metadata"].setdefault("original_file", os.path.basename(file_path))
    return extracted_data
