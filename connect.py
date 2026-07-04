class LLM:
    def ask(self, provider, prompt):
        if provider == "openai":
            client = OpenAI(
                api_key=OPENAI_KEY
            )

            model = "gpt-5"

        elif provider == "deepseek":
            client = OpenAI(
                api_key=DEEPSEEK_KEY,
                base_url="https://api.deepseek.com"
            )

            model = "deepseek-v4-flash"

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
