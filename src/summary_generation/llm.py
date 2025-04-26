from langchain_google_genai import ChatGoogleGenerativeAI
import logging
from config import get_settings
import os

class GoogleGenerativeLLM:
    """Provider for Google Generative AI (Gemini/PaLM models).
    Example:
        >>> provider = GoogleGenerativeAIProvider(api_key, model)
    """
    def __init__(self):
        # settings = get_settings()

        self.logger = logging.getLogger(__name__)
        try:
            self.client = ChatGoogleGenerativeAI(
                api_key= os.getenv("GOOGLE_API_KEY") ,# or settings.GOOGLE_API_KEY,
                model= os.getenv("GOOGLE_GENERATIVE_MODEL"), # or settings.GOOGLE_GENERATIVE_MODEL,
                max_tokens= int(os.getenv("MAX_TOKENS")), # or settings.MAX_TOKENS,
                temperature= float(os.getenv("TEMPERATURE")) # or settings.TEMPERATURE,
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize ChatGoogleGenerativeAI client: {e}")
            self.client = None
    
    def generate_response(self, messages: list):
        """Generates a response from the model given a list of messages."""
        if not self.client:
            self.logger.error("Client is not initialized.")
            return None
        
        try:
            response = self.client.invoke(messages)
            return response.content if response else None
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return None