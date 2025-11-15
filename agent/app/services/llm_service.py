"""
LLM Service - handles interactions with language models (OpenAI, Anthropic, Google Gemini).
"""
from typing import Optional, Dict, Any
from app.core.config import settings
import logging
import openai
import anthropic
import google.generativeai as genai
import json

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with Large Language Models.

    Supports:
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude)
    - Google (Gemini Pro, Gemini Flash)
    """

    def __init__(self):
        """Initialize LLM service with configured provider."""
        self.provider = settings.LLM_PROVIDER
        self.default_model = settings.DEFAULT_MODEL

        if self.provider == "openai":
            self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider == "anthropic":
            self.anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        elif self.provider == "gemini":
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(self.default_model)
        else:
            logger.warning(f"Unknown LLM provider: {self.provider}. Defaulting to Gemini.")
            self.provider = "gemini"
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(self.default_model or "gemini-pro")

    async def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
        response_format: Optional[str] = None
    ) -> str:
        """
        Generate a completion from the LLM.

        Args:
            system_prompt: System instructions
            user_prompt: User message
            temperature: Creativity (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            model: Model to use (overrides default)
            response_format: "json" or None

        Returns:
            Generated text
        """
        model = model or self.default_model
        max_tokens = max_tokens or settings.LLM_MAX_TOKENS

        try:
            if self.provider == "openai":
                return await self._generate_openai(
                    system_prompt,
                    user_prompt,
                    temperature,
                    max_tokens,
                    model,
                    response_format
                )
            elif self.provider == "anthropic":
                return await self._generate_anthropic(
                    system_prompt,
                    user_prompt,
                    temperature,
                    max_tokens,
                    model
                )
            elif self.provider == "gemini":
                return await self._generate_gemini(
                    system_prompt,
                    user_prompt,
                    temperature,
                    max_tokens,
                    model,
                    response_format
                )
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

        except Exception as e:
            logger.error(f"LLM generation failed: {e}", exc_info=e)
            raise

    async def _generate_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        model: str,
        response_format: Optional[str] = None
    ) -> str:
        """Generate completion using OpenAI."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Add JSON mode if requested
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}

        response = await self.openai_client.chat.completions.create(**kwargs)

        return response.choices[0].message.content

    async def _generate_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        model: str
    ) -> str:
        """Generate completion using Anthropic Claude."""
        response = await self.anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        return response.content[0].text

    async def _generate_gemini(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        model: str,
        response_format: Optional[str] = None
    ) -> str:
        """Generate completion using Google Gemini."""
        # Combine system and user prompts for Gemini
        combined_prompt = f"{system_prompt}\n\n{user_prompt}"

        # Add JSON instruction to prompt if needed (SDK version 0.3.2 doesn't support response_mime_type)
        if response_format == "json":
            combined_prompt += "\n\nIMPORTANT: Respond ONLY with valid JSON. No other text."

        # Configure generation
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        # Create model if different from default
        if model and model != self.default_model:
            model_instance = genai.GenerativeModel(model)
        else:
            model_instance = self.gemini_model

        # Generate content
        response = await model_instance.generate_content_async(
            combined_prompt,
            generation_config=generation_config
        )

        return response.text

    async def generate_with_examples(
        self,
        system_prompt: str,
        examples: list,
        user_prompt: str,
        temperature: float = 0.7,
        model: Optional[str] = None
    ) -> str:
        """
        Generate completion with few-shot examples.

        Args:
            system_prompt: System instructions
            examples: List of {"user": "...", "assistant": "..."} examples
            user_prompt: Current user prompt
            temperature: Creativity
            model: Model to use

        Returns:
            Generated text
        """
        messages = [{"role": "system", "content": system_prompt}]

        # Add examples
        for example in examples:
            messages.append({"role": "user", "content": example["user"]})
            messages.append({"role": "assistant", "content": example["assistant"]})

        # Add current prompt
        messages.append({"role": "user", "content": user_prompt})

        model = model or self.default_model

        if self.provider == "openai":
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            return response.choices[0].message.content

        elif self.provider == "anthropic":
            # Anthropic requires different message format
            anthropic_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in messages if msg["role"] != "system"
            ]

            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=settings.LLM_MAX_TOKENS,
                temperature=temperature,
                system=system_prompt,
                messages=anthropic_messages
            )
            return response.content[0].text

        elif self.provider == "gemini":
            # Gemini uses a simpler format
            conversation = []
            for msg in messages[1:]:  # Skip system message
                if msg["role"] == "user":
                    conversation.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    conversation.append({"role": "model", "parts": [msg["content"]]})

            model_instance = genai.GenerativeModel(model, system_instruction=system_prompt)

            response = await model_instance.generate_content_async(
                conversation,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": settings.LLM_MAX_TOKENS,
                }
            )
            return response.text

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
