import os
from typing import List, Dict

def load_document(file_path: str) -> str:
    """
    Read the raw markdown document from the specified local file path.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target document not found at: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[Dict[str, str]]:
    """
    Implement a deterministic recursive character chunking strategy.
    Snaps boundaries to spaces and newlines to prevent fragmented words at chunk edges.
    """
    chunks = []
    start = 0
    text_length = len(text)
    chunk_index = 1

    while start < text_length:
        end = start + chunk_size
        
        # Snap 'end' backwards to the nearest clean break
        if end < text_length:
            for sep in ["\n\n", "\n", " "]:
                last_sep = text.rfind(sep, start, end)
                if last_sep != -1 and last_sep > start:
                    end = last_sep + len(sep)
                    break
        
        chunk_content = text[start:end].strip()
        if chunk_content:
            chunks.append({
                "chunk_id": f"chunk_{chunk_index:02d}",
                "text": chunk_content
            })
            chunk_index += 1

        # Step back for the overlap
        next_start = end - overlap
        
        # Snap 'next_start' FORWARDS to the nearest space/newline to avoid starting mid-word
        if next_start > start and next_start < text_length:
            for sep in ["\n\n", "\n", " "]:
                next_sep = text.find(sep, next_start, end)
                if next_sep != -1:
                    start = next_sep + len(sep)
                    break
            else:
                start = end # Fallback if no natural break is found
        else:
            start = end

    return chunks

if __name__ == "__main__":
    # Verify the chunking logic locally.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(base_dir, "..", "data", "company_policies.md")
    
    raw_content = load_document(source_file)
    processed_chunks = chunk_text(raw_content, chunk_size=400, overlap=50)
    
    print(f"Total chunks generated: {len(processed_chunks)}\n")
    for chunk in processed_chunks[:3]:
        print(f"[{chunk['chunk_id']}]")
        print(chunk["text"])
        print("-" * 40)