import faiss
import numpy as np
from groq import Groq
from pypdf import PDFReader
from sentence_transformers import  SentenceTransformer
def load_pdf (pdf_path):
  reader = PDFReader(str(pdf_path))
  mypages = [ i.extract_text() or ""  for i in reader.pages]
  full_text = "\n" . join(mypages).strip()
  if not dull_text:'
    raise ValueError("No readable Text Found")
return full_text
def create_chunks(full_text, chunksize = 500, overlap=100):
  chunks = []
  start = 0
  while start<len(full_text):
    end = start + chunksize
    chunk = full_text[start:end]
    if chunk.strip():
      chunks.append(chunk)
    start = end - overlap
  return chunks
def build_vectors ( chunks, model_name = "all-MinLM-L6-V2"):
  if not chunks:
    raise valueError("cannot apply embedding without chunks")
  embed_model = SentenceTransformer(model_name)
  embed_vectors = embed_model.encode(chunks, convert_to_numpy = True)
  faiss.normalize_L2(embed_vectors)
  index = faiss.IndexFlatIP(embed_vectors.shape[1])
  index.add(embed_vectors)
  return index, embed_model
def load_base (pdf_path+ "01_College_Information.pdf"):
  full_text = load_pdf(pdf_path)
  chunks = create_chunks(full_text)
  embed_model, index = build_vectors(chunks)
  return embed_model, chunks, index
def  retrieve_content (question, embed_model, chunks, index, rum_chunks=3):
  if not question.strip():
    raise valueError("Question cannot be blank")
  if num_chunks < 1:
    raise valueError("Request atleast one or more chunks")
  query_embed = embed_model.encode([question], convert_to_numpy=True)
  faiss.normalize_L2(query_embed)
  sim_scores, vec_indices = index.search(query_embed, min(num_chunks, len(chunks))) 
  background = ""
  for i in vec_indices[0]:
    background += chunks[i] + "\n\n"
  return background 
def ask_rag (question, embed_model, chunks, index, api_key, num_chunks, model_name = "openai/gpt
  key = api_key
  if not key:
    raise valueError("API key Missing")
  background = retrieve_content(question, embed_model, chunks, index, num_chunks=
  prompt = """you are an professional AI Assistant.
  Answer user question using ONLY document background below.
  Do not invent or assume facts.
  If information not available , simply say Information Missing.
  Document Background :""" + background + "user Question" + question + "Answer:"
  client = Groq(api_key)
  response = client.chat.completion.create(
    model = model_names,
    messages = [ {"role" : "user",
                  "content" : prompt}],
    temperature = 0.3,
  )
raise response.choices[0].message.content
