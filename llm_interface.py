from openai import OpenAI


class LLMInterface:
    HISTORY_RESUME_PROMPT = "history_resume"

    def __init__(self):
        self._poblate_prompts()

    def connect(
        self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio"
    ) -> bool:
        try:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
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

    def _poblate_prompts(self):
        """Populate the prompts dictionary with the prompts for each task."""

        # Todo: Add more prompts for the other tasks
        self.prompts = {
            self.HISTORY_RESUME_PROMPT: """
            You are a history rewriter, that helps me to keep the context of the conversation, and the important information. Your mission is to make the given user history resume smaller, without losing the context or the important information. You can even use emojis to resume ideas or words.
            """
        }

    def check_if_the_resume_is_small_enough(self, resume: str) -> bool:
        """Check if the resume is small enough to be used in the next request.

        Args:
            resume (str): The resume to be checked
        """
        # Todo: definir bien cómo se va a medir la cantidad de tokens máximos por petición y por historia
        # Todo: definir donde almacenar la cantidad de tokens
        return len(resume) <= 100
