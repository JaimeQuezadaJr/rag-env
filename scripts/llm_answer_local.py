import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import subprocess
import json
from query import load_index_and_meta, query_index

SYSTEM_PROMPT = """
You are Tim Cook, CEO of Apple.
Your responses are:
- Clear
- Concise
- Inspirational
- Professional
- Focused on simplicity and user experience.
Speak in Tim Cook’s tone and mannerisms.
"""


def build_prompt(question, retrieved_chunks):
    context = ""
    for r in retrieved_chunks:
        context += f"\n[PDF: {r['pdf']} | Page {r['page']}]\n{r['text']}\n"

    return f"""
SYSTEM MESSAGE:
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{question}

Answer as Tim Cook. Use the context above to stay accurate.
If the answer isn't in the PDFs, say: 
"I'm not seeing that in the documentation."
"""


def ollama_generate(model, prompt):
    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = process.communicate(prompt)
    return out


def rag_answer(question, top_k=4, model="gemma3:4b"):
    vectorstore, _ = load_index_and_meta()
    retrieved = query_index(question, vectorstore, top_k=top_k)

    prompt = build_prompt(question, retrieved)
    answer = ollama_generate(model, prompt)

    return answer


if __name__ == "__main__":
    q = "What are the two components of the physical test battery?"
    print(rag_answer(q))
