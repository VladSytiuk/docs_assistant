ASSISTANT_PROMPT = """Answer the users QUESTION using the DOCUMENT text.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION, answer 'I don't know'.
in the answer, additionally display the name of the section and page number in which the
the answer is found.

DOCUMENT:
{context}

QUESTION:
{question}

Helpful Answer:"""
