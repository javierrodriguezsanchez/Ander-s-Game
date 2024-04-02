from openai import OpenAI


class LLMInterface:
    def __init__(self):
        self.client = OpenAI()

    def connect(self, api_key: str):
        try:
            self.client.base_url = "http://localhost:1234/v1"
            self.client.api_key = api_key
            return True
        except Exception as e:
            print(e)
            return False

    def resume_history(self, old_history_resume: str) -> str:
        """Resume the previous history resume in order to make it smaller for the next request. The main goal is to keep the context of the conversation.

        Args:
            old_history_resume (str): The previous history resume
        """

        # Create the system content that will be used to resume the user history
        system_content = """
        You are a history rewriter, that helps me to keep the context of the conversation, and the important information. Your mission is to make the given user history resume smaller, without losing the context or the important information. You can even use emojis to resume ideas or words.
        """

        # Request for resumes to the model
        completation = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": old_history_resume},
            ],
            temperature=1.0,
        )

        # Get the response from the model
        response = completation.choices[0].message.content

        return response
