import os
import logging
from typing import Optional, Any
from langchain.llms import OpenAI
from langchain.llms import Anthropic

class FallbackHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.llm_options = {
            'llama': self._setup_llama,
            'openai': self._setup_openai,
            'anthropic': self._setup_anthropic
        }

    def get_fallback_llm(self, primary_llm: str) -> Optional[Any]:
        """Get fallback LLM if primary fails"""
        self.logger.info(f"Primary LLM {primary_llm} failed, attempting fallback...")
        
        # Try each LLM option in order
        for llm_name, setup_func in self.llm_options.items():
            if llm_name != primary_llm:
                try:
                    llm = setup_func()
                    if llm:
                        self.logger.info(f"Successfully set up fallback LLM: {llm_name}")
                        return llm
                except Exception as e:
                    self.logger.warning(f"Failed to set up {llm_name}: {str(e)}")

        self.logger.error("All fallback options failed")
        return None

    def _setup_llama(self):
        """Set up Llama model"""
        try:
            from langchain.llms import LlamaCpp
            model_path = os.getenv('LLAMA_MODEL_PATH', 'models/llama-2-7b-chat.gguf')
            
            if not os.path.exists(model_path):
                self.logger.error(f"Llama model not found at {model_path}")
                return None

            return LlamaCpp(
                model_path=model_path,
                temperature=0.7,
                max_tokens=2000
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Llama: {str(e)}")
            return None

    def _setup_openai(self):
        """Set up OpenAI model"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.logger.error("OpenAI API key not found")
            return None

        try:
            return OpenAI(
                openai_api_key=api_key,
                temperature=0.7
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI: {str(e)}")
            return None

    def _setup_anthropic(self):
        """Set up Anthropic/Claude model"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            self.logger.error("Anthropic API key not found")
            return None

        try:
            return Anthropic(
                anthropic_api_key=api_key,
                temperature=0.7
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Anthropic: {str(e)}")
            return None