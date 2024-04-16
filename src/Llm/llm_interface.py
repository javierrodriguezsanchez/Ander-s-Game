from openai import OpenAI


class LLMInterface:
    HISTORY_RESUME_PROMPT = "history_resume"
    CREATE_STORY_PROMPT = "create_story"

    def __init__(self):
        self._poblate_prompts()
        self.client: OpenAI = None
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(
        self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio"
    ) -> bool:
        try:
            self.client = OpenAI(base_url=base_url, api_key=api_key)
            self._connected = True
            return self.connected
        except Exception as e:
            print(e)
            self._connected = False
            return self.connected

    def resume_history(self, old_history_resume: str, history_constants: str) -> str:
        """Resume the previous history resume in order to make it smaller for the next request. The main goal is to keep the context of the conversation.

        Args:
            old_history_resume (str): The previous history resume
            history_constants (str): The constants of the history
        """

        # Request for resumes to the model
        completion = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {
                    "role": "system",
                    "content": self.prompts[self.HISTORY_RESUME_PROMPT]
                    + "\nThis are constants of the history:\n"
                    + history_constants,
                },
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
            self.HISTORY_RESUME_PROMPT: """You are a history rewriter, that helps me to keep the context of the conversation, and the important information. Your mission is to make the given user history resume smaller, without losing the context or the important information. You can even use emojis to resume ideas or words.
            A valid resume can be something like:
                resume_input: "The king 1 attack the king 2"
                resume_output: "1⃣⚔️2⃣"
            The use of emojis is not for decoration, but to resume the information in a smaller way. Be creative!
            """,
            self.CREATE_STORY_PROMPT: """You are a history creator. Your best ability is, given a resume of an history, and a log that represent actions in a fantasy world between kingdoms, to create a new history that continues the previous one. Your mission is to create a story that makes sense and is coherent with the previous history. You are capable to create the history based on the log, and give some personality to the success and failure of the actions. You can even use emojis to make the story more interesting. Be creative!
            A Quick valid example of a history can be:
                resume: "1⃣⚔️2⃣"
                log: "The king 2 attack the king 1"
                history: "Searching for revenge, the king 2 prepare his tropes and after wait for the correct moment, he attack the king 1."
            It's very important the coherence of the history with the previous history and the log, and also, not generate something that will be related to a future action. A bad example can be:
                resume: "1⃣⚔️2⃣"
                log: "The king 2 attack the king 1"
                history: "The king 2 searching for revenge, prepare his tropes and after wait for the correct moment, he attack the king 1. The king 1, after the attack, prepare his troops and attack the king 2."
            the previous example is bad because the history is related to a future action, showing a second attack of the king 1 to the king 2.
            In any case, you just need to generate the history, not the log or the resume. The log and the resume are just for the context of the history. Also, will be grate if you use emojis to make the history more interesting occasionally after some words. Be creative and build a short and interesting history!
            """,
        }

    def check_if_the_resume_is_small_enough(self, resume: str) -> bool:
        """Check if the resume is small enough to be used in the next request.

        Args:
            resume (str): The resume to be checked
        """
        max_history_resume_tokens = 1024

        return len(resume.split()) < max_history_resume_tokens

    def generate_history(
        self, history_resume: str, log_text: str, history_constants
    ) -> str:
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
                {
                    "role": "system",
                    "content": self.prompts[self.CREATE_STORY_PROMPT]
                    + "RESUME OF THE HISTORY"
                    + "\n"
                    + history_constants
                    + "\n"
                    + history_resume
                    + "\nEND OF THE RESUME\n\n",
                },
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
