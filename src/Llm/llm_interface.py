from openai import OpenAI


class LLMInterface:
    HISTORY_RESUME_PROMPT = "history_resume"
    CREATE_STORY_PROMPT = "create_story"

    def __init__(self):
        self._poblate_prompts()
        self.client: OpenAI = None

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

        # Request for resumes to the model
        completion = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": self.prompts[self.HISTORY_RESUME_PROMPT]},
                {"role": "user", "content": old_history_resume},
            ],
            temperature=1.0,
        )

        # Get the response from the model
        response = completion.choices[0].message.content

        return response

    def _poblate_prompts(self):
        """Populate the prompts dictionary with the prompts for each task."""

        # Todo: Add more prompts for the other tasks
        self.prompts = {
            self.HISTORY_RESUME_PROMPT: "You are a history rewriter, that helps me to keep the context of the conversation, and the important information. Your mission is to make the given user history resume smaller, without losing the context or the important information. You can even use emojis to resume ideas or words.",
            self.CREATE_STORY_PROMPT: "You are a history creator. Your best ability is, given a resume of an history, and a log that represent actions in a fantasy world between kingdoms, to create a new history that continues the previous one. Your mission is to create a story that makes sense and is coherent with the previous history. You are capable to create the history based on the log, and give some personality to the success and failure of the actions. You can even use emojis to make the story more interesting. Also, you create the story small enough with all necessary information. Be creative!",
        }

    def check_if_the_resume_is_small_enough(self, resume: str) -> bool:
        """Check if the resume is small enough to be used in the next request.

        Args:
            resume (str): The resume to be checked
        """
        max_history_resume_tokens = 1024

        return len(resume.split()) < max_history_resume_tokens

    def generate_history(self, history_resume: str, log_text: str) -> str:
        """Generate the history of the game using the history resume and the log text.

        Args:
            history_resume (str): The history resume to be used
            log_text (str): The log text to be added to the history

        Returns:
            str: The generated history
        """

        # Request for the model to generate the history
        completion = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": self.prompts[self.CREATE_STORY_PROMPT]},
                {"role": "user", "content": log_text},
            ],
            temperature=1.0,
        )
        # Todo: Revisar que el flujo del resumen de la historia
        # Get the response from the model
        response = completion.choices[0].message.content

        # Check if it is necessary to resume the history
        if not self.check_if_the_resume_is_small_enough(response):
            history_resume = self.resume_history(history_resume)

        return response, history_resume
