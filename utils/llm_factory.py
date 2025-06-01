"""
LLM Factory - Abstração para múltiplos provedores de LLM
Suporta Google Gemini e Anthropic Claude
"""

import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

# Logger com fallback
try:
    from utils.logger import get_logger
except ImportError:
    class SimpleLogger:
        def __init__(self, name): self.name = name
        def info(self, msg): print(f"[INFO] {self.name}: {msg}")
        def warning(self, msg): print(f"[WARNING] {self.name}: {msg}")
        def error(self, msg): print(f"[ERROR] {self.name}: {msg}")
        def debug(self, msg): print(f"[DEBUG] {self.name}: {msg}")
    def get_logger(name): return SimpleLogger(name)

logger = get_logger(__name__)


class BaseLLMWrapper(ABC):
    """Classe base abstrata para wrappers de LLM"""
    
    @abstractmethod
    def invoke(self, prompt: str, **kwargs) -> Any:
        """Invoca o LLM com um prompt"""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o LLM"""
        pass


class GeminiWrapper(BaseLLMWrapper):
    """Wrapper para Google Gemini"""
    
    def __init__(self, model_name: str, api_key: str, **kwargs):
        try:
            import google.generativeai as genai
            
            # Configurar API key
            genai.configure(api_key=api_key)
            
            # Configurações de segurança
            safety_settings = kwargs.get('safety_settings', [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                }
            ])
            
            # Configurações de geração
            generation_config = {
                "temperature": kwargs.get('temperature', 0.7),
                "top_p": kwargs.get('top_p', 0.95),
                "top_k": kwargs.get('top_k', 40),
                "max_output_tokens": kwargs.get('max_tokens', 8192),
            }
            
            # Criar modelo
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            self.model_name = model_name
            self.generation_config = generation_config
            
            logger.info(f"✅ Gemini configurado: {model_name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar Gemini: {e}")
            raise
    
    def invoke(self, prompt: str, **kwargs) -> Any:
        """Invoca o Gemini com um prompt"""
        try:
            response = self.model.generate_content(prompt)
            
            # Criar objeto compatível com o formato esperado
            class GeminiResponse:
                def __init__(self, text):
                    self.content = text
            
            return GeminiResponse(response.text)
            
        except Exception as e:
            logger.error(f"❌ Erro ao invocar Gemini: {e}")
            raise
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo Gemini"""
        return {
            "provider": "gemini",
            "model": self.model_name,
            "config": self.generation_config
        }


class GeminiLangChainWrapper(BaseLLMWrapper):
    """Wrapper para Google Gemini via LangChain"""
    
    def __init__(self, model_name: str, api_key: str, **kwargs):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            # Remover o prefixo 'models/' se presente
            if model_name.startswith("models/"):
                model_name = model_name.replace("models/", "")
            
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=kwargs.get('temperature', 0.7),
                max_output_tokens=kwargs.get('max_tokens', 8192),
                top_p=kwargs.get('top_p', 0.95),
                top_k=kwargs.get('top_k', 40),
                convert_system_message_to_human=True,  # Gemini não tem mensagens de sistema nativas
            )
            
            self.model_name = model_name
            self.provider = "gemini_langchain"
            
            logger.info(f"✅ Gemini LangChain configurado: {model_name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar Gemini LangChain: {e}")
            raise
    
    def invoke(self, prompt: str, **kwargs) -> Any:
        """Invoca o Gemini via LangChain"""
        return self.llm.invoke(prompt)
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        return {
            "provider": self.provider,
            "model": self.model_name
        }


class AnthropicWrapper(BaseLLMWrapper):
    """Wrapper para Anthropic Claude via LangChain"""
    
    def __init__(self, model_name: str, api_key: str, **kwargs):
        try:
            from langchain_anthropic import ChatAnthropic
            
            self.llm = ChatAnthropic(
                model=model_name,
                anthropic_api_key=api_key,
                max_tokens=kwargs.get('max_tokens', 4096),
                temperature=kwargs.get('temperature', 0.7),
            )
            
            self.model_name = model_name
            self.provider = "anthropic_langchain"
            
            logger.info(f"✅ Anthropic configurado: {model_name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar Anthropic: {e}")
            raise
    
    def invoke(self, prompt: str, **kwargs) -> Any:
        """Invoca o Claude"""
        return self.llm.invoke(prompt)
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        return {
            "provider": self.provider,
            "model": self.model_name
        }


class LLMFactory:
    """Factory para criar instâncias de LLM baseado na configuração"""
    
    @staticmethod
    def create_llm(provider: Optional[str] = None, use_langchain: bool = True, **kwargs) -> BaseLLMWrapper:
        """
        Cria uma instância de LLM baseado no provider
        
        Args:
            provider: "gemini" ou "anthropic" (se None, usa config)
            use_langchain: Se True, usa wrapper LangChain (recomendado)
            **kwargs: Configurações adicionais do modelo
        
        Returns:
            Instância de BaseLLMWrapper
        """
        try:
            import config
            
            # Determinar provider
            if provider is None:
                provider = config.LLM_PROVIDER
            
            provider = provider.lower()
            
            if provider == "gemini":
                api_key = config.GOOGLE_API_KEY
                model_name = kwargs.get('model', config.DEFAULT_MODEL)
                
                # Configurações padrão do Gemini
                llm_kwargs = {
                    'temperature': kwargs.get('temperature', config.TEMPERATURE),
                    'max_tokens': kwargs.get('max_tokens', config.MAX_TOKENS),
                    'top_p': kwargs.get('top_p', config.TOP_P),
                    'top_k': kwargs.get('top_k', config.TOP_K),
                }
                
                if hasattr(config, 'GEMINI_SAFETY_SETTINGS'):
                    llm_kwargs['safety_settings'] = config.GEMINI_SAFETY_SETTINGS
                
                if use_langchain:
                    return GeminiLangChainWrapper(model_name, api_key, **llm_kwargs)
                else:
                    return GeminiWrapper(model_name, api_key, **llm_kwargs)
            
            elif provider == "anthropic":
                api_key = config.ANTHROPIC_API_KEY
                model_name = kwargs.get('model', config.DEFAULT_MODEL)
                
                # Configurações padrão do Anthropic
                llm_kwargs = {
                    'temperature': kwargs.get('temperature', config.TEMPERATURE),
                    'max_tokens': kwargs.get('max_tokens', config.MAX_TOKENS),
                }
                
                return AnthropicWrapper(model_name, api_key, **llm_kwargs)
            
            else:
                raise ValueError(f"Provider não suportado: {provider}")
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar LLM: {e}")
            raise
    
    @staticmethod
    def get_available_providers() -> list:
        """Retorna lista de providers disponíveis"""
        providers = []
        
        try:
            import config
            
            if hasattr(config, 'GOOGLE_API_KEY') and config.GOOGLE_API_KEY:
                providers.append("gemini")
            
            if hasattr(config, 'ANTHROPIC_API_KEY') and config.ANTHROPIC_API_KEY:
                providers.append("anthropic")
                
        except:
            pass
        
        return providers


# Função helper para facilitar migração
def create_llm(**kwargs) -> BaseLLMWrapper:
    """
    Função helper para criar LLM com configurações padrão
    
    Uso:
        llm = create_llm()  # Usa provider padrão do config
        llm = create_llm(provider="gemini")  # Força Gemini
        llm = create_llm(temperature=0.9)  # Customiza temperatura
    """
    return LLMFactory.create_llm(**kwargs)


if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando LLM Factory...")
    
    try:
        # Testar criação de LLM
        llm = create_llm()
        info = llm.get_info()
        print(f"✅ LLM criado: {info}")
        
        # Testar invocação
        response = llm.invoke("Olá! Responda em uma linha.")
        print(f"📝 Resposta: {response.content}")
        
        # Listar providers disponíveis
        providers = LLMFactory.get_available_providers()
        print(f"🤖 Providers disponíveis: {providers}")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")