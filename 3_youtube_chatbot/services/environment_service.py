import os
from dotenv import load_dotenv
from openai import OpenAI


class EnvironmentService:
    def __init__(self):
        load_dotenv(override=True)

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("AI_MODEL")
        self.base_url = os.getenv("BASE_URL")
        self.proxy_user = os.getenv("PROXY_USER")
        self.proxy_pwd = os.getenv("PROXY_PWD")

        self.openai_client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def get_client(self):
        return self.openai_client

    def get_model(self):
        return self.model

    def get_base_url(self):
        return self.base_url

    def get_proxy_details(self):
        return {"user": self.proxy_user, "pwd": self.proxy_pwd}
