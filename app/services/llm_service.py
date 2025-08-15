import os
import time
from typing import Optional
import google.generativeai as genai
from app.models.schemas import LLMRequest, LLMResponse, LLMQueryRequest, LLMQueryResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
        genai.configure(api_key=self.api_key)
        self.default_model = "gemini-1.5-flash"
        
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generate response using Gemini LLM"""
        try:
            logger.info(f"Generating LLM response for: {request.text[:50]}...")
            
            # Initialize model
            model = genai.GenerativeModel(request.model or self.default_model)
            
            # Generate response
            response = model.generate_content(request.text)
            
            # Extract response text
            response_text = response.text if response.text else "No response generated"
            
            result = LLMResponse(
                success=True,
                message="Response generated successfully",
                response_text=response_text,
                model_used=request.model or self.default_model
            )
            
            logger.info(f"LLM response generated successfully using {result.model_used}")
            return result
            
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            return LLMResponse(
                success=False,
                message=f"Error generating response: {str(e)}"
            )
    
    async def query_llm(self, request: LLMQueryRequest) -> LLMQueryResponse:
        """Query LLM with advanced parameters"""
        try:
            logger.info(f"Querying LLM with parameters: model={request.model}, max_tokens={request.max_tokens}")
            
            # Initialize model with parameters
            model = genai.GenerativeModel(
                model_name=request.model or self.default_model,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=request.max_tokens,
                    temperature=request.temperature
                )
            )
            
            # Generate response
            response = model.generate_content(request.text)
            
            # Extract response
            response_text = response.text if response.text else "No response generated"
            
            result = LLMQueryResponse(
                success=True,
                message="Query processed successfully",
                query=request.text,
                response=response_text,
                model_used=request.model or self.default_model,
                tokens_used=len(response_text.split())  # Approximate token count
            )
            
            logger.info(f"LLM query successful: {result.tokens_used} tokens used")
            return result
            
        except Exception as e:
            logger.error(f"LLM query error: {str(e)}")
            return LLMQueryResponse(
                success=False,
                message=f"Error processing query: {str(e)}",
                query=request.text
            )
    
    def get_available_models(self) -> list:
        """Get list of available Gemini models"""
        try:
            models = genai.list_models()
            gemini_models = [model.name for model in models if 'gemini' in model.name.lower()]
            return gemini_models
        except Exception as e:
            logger.error(f"Error getting models: {str(e)}")
            return [self.default_model]
