import openai
import os
from aisuite.provider import Provider, LLMError

from aisuite.providers import NORM_KWARGS_OPENAI


class OpenaiProvider(Provider):
    def __init__(self, **config):
        """
        Initialize the OpenAI provider with the given configuration.
        Pass the entire configuration dictionary to the OpenAI client constructor.
        """
        # Ensure API key is provided either in config or via environment variable
        config.setdefault("api_key", os.getenv("OPENAI_API_KEY"))
        if not config["api_key"]:
            raise ValueError(
                "OpenAI API key is missing. Please provide it in the config or set the OPENAI_API_KEY environment variable."
            )

        # NOTE: We could choose to remove above lines for api_key since OpenAI will automatically
        # infer certain values from the environment variables.
        # Eg: OPENAI_API_KEY, OPENAI_ORG_ID, OPENAI_PROJECT_ID, OPENAI_BASE_URL, etc.

        # Pass the entire config to the OpenAI client constructor
        config ={
            NORM_KWARGS_OPENAI.get(norm_key, norm_key): value
            for norm_key, value in config.items()
        }
        self.client = openai.OpenAI(**config)

    def response_stream_generator(self, response):
        with response as stream:
            for text in stream:
                yield text.choices[0].delta.content

    def chat_completions_create(self, model, messages, **kwargs):
        # Any exception raised by OpenAI will be returned to the caller.
        # Maybe we should catch them and raise a custom LLMError.
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs  # Pass any additional arguments to the OpenAI API
        )

        if kwargs.get("stream", False):
            return self.response_stream_generator(response)
        return response
            
            
        
    

   
