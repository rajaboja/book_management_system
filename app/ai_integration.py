import groq

class LlamaIntegration:
    def __init__(self):
        self.client = groq.Client()

    async def generate_summary(self, book_content: str) -> str:
        prompt = f"Summarize the following book content:\n\n{book_content}\n\nSummary:"
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes books."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

llama_integration = LlamaIntegration()