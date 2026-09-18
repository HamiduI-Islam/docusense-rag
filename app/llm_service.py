import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client pointed at Groq's free compatibility endpoint
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_grounded_response(query: str, context_chunks: list[str]) -> tuple[str, int]:
    """
    Synthesize an answer using only the provided context chunks.
    Enforce a strict anti-hallucination guardrail if the context is insufficient.
    Return the answer string and the total token count.
    """
    combined_context = "\n\n---\n\n".join(context_chunks)
    
    system_prompt = (
        "You are a strict, factual technical assistant. You must answer the user's question "
        "using ONLY the provided context documentation.\n\n"
        "CRITICAL GUARDRAIL: If the provided documentation does not contain the exact answer, "
        "you must not attempt to guess or use outside knowledge. Instead, you must output exactly "
        "this exact phrase and nothing else: "
        "'The provided documentation does not contain sufficient information to answer this question.'"
    )
    
    user_prompt = f"Context Documentation:\n{combined_context}\n\nUser Question: {query}"
    
    # Execute the LLM call using a fast, free open-source model
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0
    )
    
    answer = response.choices[0].message.content.strip()
    tokens_used = response.usage.total_tokens
    
    return answer, tokens_used