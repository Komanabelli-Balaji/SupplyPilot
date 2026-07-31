import time

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

from config.settings import FALLBACK_MODEL, MODEL


class Provider:

    def __init__(
        self,
        system_prompt,
        tools,
        response_format,
        retry_delay=60,
    ):

        self.retry_delay = retry_delay
        self.system_prompt = system_prompt
        self.tools = tools
        self.response_format = response_format

        self.primary_model = init_chat_model(MODEL)
        self.fallback_model = init_chat_model(FALLBACK_MODEL)

    def _build_agent(self, model, response_format):
        return create_agent(
            model=model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            response_format=response_format,
        )

    def invoke(self, messages):
        return self.invoke_with_schema(
            messages=messages,
            response_format=self.response_format,
        )

    def invoke_with_schema(
        self,
        messages,
        response_format
    ):
        primary_agent = self._build_agent(self.primary_model, response_format)
        fallback_agent = self._build_agent(self.fallback_model, response_format)

        while True:

            # ---------- PRIMARY ----------

            try:
                print(f"\nUsing {MODEL}")

                response = primary_agent.invoke(
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
                    raise

            # ---------- FALLBACK ----------

            try:
                print(f"\nUsing {FALLBACK_MODEL}")

                response = fallback_agent.invoke(
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
                    raise

                time.sleep(self.retry_delay)