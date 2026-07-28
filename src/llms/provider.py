import time

from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from config.settings import MODEL, FALLBACK_MODEL


class Provider:

    def __init__(
        self,
        system_prompt,
        tools,
        response_format,
        retry_delay=60,
    ):

        self.retry_delay = retry_delay
        self.response_format = response_format

        self.primary_model = init_chat_model(MODEL)
        self.fallback_model = init_chat_model(FALLBACK_MODEL)

        self.primary_agent = create_agent(
            model=self.primary_model,
            tools=tools,
            system_prompt=system_prompt,
            response_format=response_format
        )

        self.fallback_agent = create_agent(
            model=self.fallback_model,
            tools=tools,
            system_prompt=system_prompt,
            response_format=response_format
        )

    def invoke(self, messages):

        while True:

            # ---------- PRIMARY ----------

            try:
                print(f"\nUsing {MODEL}")

                response = self.primary_agent.invoke(
                    {"messages": messages}
                )
                return response["structured_response"]

            except ChatGoogleGenerativeAIError as e:
                if "RESOURCE_EXHAUSTED" in str(e):
                    print("=" * 60)
                    print(f"{MODEL} failed.")
                    print(type(e).__name__)
                    print(f"Switching to {FALLBACK_MODEL}")
                    print("=" * 60)

                else:
                    raise e

            # ---------- FALLBACK ----------

            try:
                print(f"\nUsing {FALLBACK_MODEL}")

                response = self.fallback_agent.invoke(
                    {"messages": messages}
                )
                return response["structured_response"]

            except ChatGoogleGenerativeAIError as e:
                if "RESOURCE_EXHAUSTED" in str(e):
                    print("=" * 60)
                    print(f"{FALLBACK_MODEL} failed.")
                    print(type(e).__name__)
                    print(f"Retrying in {self.retry_delay} seconds...")
                    print("=" * 60)
                else:
                    raise e

                time.sleep(self.retry_delay)