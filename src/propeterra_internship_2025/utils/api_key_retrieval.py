
import os

class RetrieveApiKey:
    """Class to retrieve API keys for different models."""

    def __init__(self, model:str):
        self.model = model

        self.supported_models = {"gpt-4.1":  os.environ.get("OPENAI_API_KEY_PROPETERRA"),
                                 "sonar":    os.environ.get("PERPLEXITY_API_KEY_PROPETERRA"),
                                 "sonar-pro":os.environ.get("PERPLEXITY_API_KEY_PROPETERRA"),
                                 "sonar-deep-research":os.environ.get("PERPLEXITY_API_KEY_PROPETERRA"),
                                 "ms_copilot":os.environ.get("MS_COPILOT_API_KEY"),
                                 "mistral":         os.environ.get("MISTRAL_API_KEY"),
                                 "gemini_2.5_flash":os.environ.get("GEMINI_API_KEY"),
                                 "manus":           os.environ.get("MANUS_API_KEY")}

        if model not in self.supported_models:

            raise ValueError("Selected model not in list of supported models.")
