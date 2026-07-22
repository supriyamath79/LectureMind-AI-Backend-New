print("LLM SERVICE IMPORTED")

import ollama


def generate_answer(question, retrieved_chunks):
    # Use only the top 2 retrieved chunks
    context = "\n\n".join(retrieved_chunks[:2])

    # Debug: Print retrieved chunks
    print("\n========== RETRIEVED CHUNKS ==========\n")

    for i, chunk in enumerate(retrieved_chunks[:2], start=1):
        print(f"\nChunk {i}:\n")
        print(chunk)
        print("-" * 60)

    # Prompt
    prompt = f"""
    You are LectureMind AI.

    You are a Retrieval-Augmented Generation (RAG) assistant.

    STRICT RULES:

    - Answer ONLY from the Lecture Context.
    - Never use your own knowledge.
    - Never guess.
    - Never add examples that are not present in the lecture.
    - Never explain concepts beyond the lecture.
    - If the answer is missing, reply exactly:
    "I could not find the answer in the lecture."
    - Give a complete answer if it exists.
    - Finish every sentence.
    - Use simple paragraphs.

    Lecture Context:
    {context}

    Question:
    {question}

    Answer:
    """

    # Generate answer using Gemma
    response = ollama.chat(
        model="gemma2:2b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
        "temperature":0,
        "num_predict":512,
        "top_p":0.9,
        "top_k":40
    }
    )

    answer = response["message"]["content"]

    # Debug: Print answer
    print("\n========== GENERATED ANSWER ==========\n")
    print(answer)
    print("\n======================================\n")

    return answer