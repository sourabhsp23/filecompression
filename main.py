from fastapi import FastAPI, UploadFile, File, HTTPException
from compression import *
from decompression import *
import os
import json

app = FastAPI()

UPLOAD_DIR = "app/static/uploads/"
COMPRESSED_DIR = "app/static/compressed/"
DECOMPRESSED_DIR = "app/static/decompressed/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(COMPRESSED_DIR, exist_ok=True)
os.makedirs(DECOMPRESSED_DIR, exist_ok=True)

@app.post("/compress/")
async def compress_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        with open(file_path, "r") as f:
            text = f.read()

        if not text.strip():
            raise HTTPException(status_code=400, detail="Uploaded file is empty or only contains whitespace.")

        encoded_text, codes = huffman_compress(text)
        compressed_file_path = os.path.join(COMPRESSED_DIR, f"{file.filename}.huff")
        save_compressed(encoded_text, compressed_file_path)

        return {
            "message": "File compressed successfully.",
            "compressed_file_path": compressed_file_path,
            "huffman_codes": codes,
            "encoded_text_preview": encoded_text[:100] + "..."  # Preview for display
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decompress/")
async def decompress_file(
    file: UploadFile = File(...), codes: str = None
):
    try:
        # Save the compressed file to disk
        compressed_file_path = os.path.join(COMPRESSED_DIR, file.filename)
        with open(compressed_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Read the binary data
        with open(compressed_file_path, "rb") as f:
            compressed_content = f.read()

        # Convert binary data to bit string
        encoded_text = bin(int.from_bytes(compressed_content, byteorder="big"))[2:]
        
        # Pad with leading zeroes if necessary
        encoded_text = encoded_text.zfill(len(compressed_content) * 8)

        # Parse the Huffman codes
        try:
            huffman_codes = json.loads(codes)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON for Huffman codes.")

        if not encoded_text or not huffman_codes:
            raise HTTPException(status_code=400, detail="Encoded text or Huffman codes missing for decompression.")

        # Decode the compressed content
        decoded_text = decode_huffman(encoded_text, huffman_codes)

        # Save the decompressed content
        decompressed_file_path = os.path.join(DECOMPRESSED_DIR, f"{file.filename}.decompressed.txt")
        with open(decompressed_file_path, "w") as f:
            f.write(decoded_text)

        return {
            "message": "File decompressed successfully.",
            "decompressed_file_path": decompressed_file_path,
            "decoded_text_preview": decoded_text[:100] + "..."  # Preview for display
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
