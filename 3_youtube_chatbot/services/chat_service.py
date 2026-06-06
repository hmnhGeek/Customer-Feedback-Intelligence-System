from services.environment_service import EnvironmentService
from services.prompt_service import PromptService


class ChatService:
    def __init__(self, transcript):
        self.environment = EnvironmentService()
        self.client = self.environment.get_client()
        self.model = self.environment.get_model()
        self.transcript = transcript

    def chat(self, message, history):
        messages = [{"role": "system", "content": PromptService.get_system_prompt(
            self.transcript)}] + history + [{"role": "user", "content": message}]
        stream = self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True)
        response = ""
        for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            yield response
