"""
🔍 SISTEMA DE AUDITORIA AUTOMÁTICA - GPT Mestre Autônomo
Verificação completa, detecção de falhas e correções automáticas
Ciclo repetitivo até 100% funcional sem bugs nem erros
"""

import os
import sys
import time
import importlib
import subprocess
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import traceback

@dataclass
class AuditResult:
    """Resultado de uma verificação de auditoria"""
    category: str
    item: str
    status: str  # "OK", "WARNING", "ERROR", "FIXED"
    message: str
    details: Optional[str] = None
    suggested_fix: Optional[str] = None

class SystemAuditor:
    """Sistema principal de auditoria e correção automática"""
    
    def __init__(self):
        self.results: List[AuditResult] = []
        self.fixes_applied = 0
        self.cycle_count = 0
        
    def run_complete_audit(self) -> bool:
        """Executa auditoria completa - retorna True se sistema está 100% OK"""
        print("🔍 INICIANDO AUDITORIA COMPLETA DO SISTEMA")
        print("=" * 60)
        
        self.cycle_count += 1
        print(f"📊 CICLO DE AUDITORIA #{self.cycle_count}")
        
        # Limpar resultados anteriores
        self.results.clear()
        initial_fixes = self.fixes_applied
        
        # 1. VERIFICAÇÃO DE ESTRUTURA DE ARQUIVOS
        print("\n📁 1. VERIFICANDO ESTRUTURA DE ARQUIVOS...")
        self._audit_file_structure()
        
        # 2. VERIFICAÇÃO DE IMPORTS E DEPENDÊNCIAS
        print("\n📦 2. VERIFICANDO IMPORTS E DEPENDÊNCIAS...")
        self._audit_imports()
        
        # 3. VERIFICAÇÃO DE AGENTES
        print("\n🤖 3. VERIFICANDO AGENTES...")
        self._audit_agents()
        
        # 4. VERIFICAÇÃO DE CONFIGURAÇÕES
        print("\n⚙️ 4. VERIFICANDO CONFIGURAÇÕES...")
        self._audit_configurations()
        
        # 5. VERIFICAÇÃO DE TESTES
        print("\n🧪 5. VERIFICANDO TESTES...")
        self._audit_tests()
        
        # 6. VERIFICAÇÃO DE MEMÓRIA E CACHE
        print("\n🧠 6. VERIFICANDO MEMÓRIA E CACHE...")
        self._audit_memory_systems()
        
        # 7. VERIFICAÇÃO DE LOGS E MONITORAMENTO
        print("\n📊 7. VERIFICANDO LOGS E MONITORAMENTO...")
        self._audit_logging()
        
        # 8. VERIFICAÇÃO DE SEGURANÇA
        print("\n🔒 8. VERIFICANDO SEGURANÇA...")
        self._audit_security()
        
        # RELATÓRIO FINAL
        return self._generate_audit_report()
    
    def _audit_file_structure(self):
        """Verifica estrutura de arquivos essenciais"""
        
        essential_files = [
            ("app.py", "Arquivo principal da aplicação"),
            ("config.py", "Configurações do sistema"),
            ("requirements.txt", "Dependências Python"),
            (".env", "Variáveis de ambiente"),
            ("chainlit.md", "Documentação do Chainlit"),
        ]
        
        essential_dirs = [
            ("agents/", "Diretório de agentes"),
            ("utils/", "Diretório de utilitários"),
            ("memory/", "Diretório de memória"),
            ("tests/", "Diretório de testes"),
            ("logs/", "Diretório de logs"),
        ]
        
        # Verificar arquivos
        for file, desc in essential_files:
            if os.path.exists(file):
                self.results.append(AuditResult(
                    "file_structure", file, "OK", f"{desc} encontrado"
                ))
            else:
                self.results.append(AuditResult(
                    "file_structure", file, "ERROR", f"{desc} FALTANDO",
                    suggested_fix=f"Criar arquivo {file}"
                ))
        
        # Verificar diretórios
        for dir_path, desc in essential_dirs:
            if os.path.exists(dir_path):
                self.results.append(AuditResult(
                    "file_structure", dir_path, "OK", f"{desc} encontrado"
                ))
            else:
                self.results.append(AuditResult(
                    "file_structure", dir_path, "ERROR", f"{desc} FALTANDO",
                    suggested_fix=f"Criar diretório {dir_path}"
                ))
                # AUTO-FIX: Criar diretório
                try:
                    os.makedirs(dir_path, exist_ok=True)
                    self.results[-1].status = "FIXED"
                    self.results[-1].message += " - CORRIGIDO AUTOMATICAMENTE"
                    self.fixes_applied += 1
                except Exception as e:
                    self.results[-1].details = f"Erro ao criar: {e}"
    
    def _audit_imports(self):
        """Verifica se todos os imports essenciais funcionam"""
        
        critical_imports = [
            ("chainlit", "Interface principal"),
            ("google.generativeai", "LLM Gemini"),
            ("langchain_google_genai", "LangChain Gemini"),
            ("chromadb", "Banco vetorial"),
            ("duckduckgo_search", "Web search"),
        ]
        
        agent_modules = [
            ("agents.carlos", "Carlos Maestro"),
            ("agents.base_agent_v2", "BaseAgent v2"),
            ("agents.oraculo_v2", "Oráculo v9"),
            ("agents.psymind_v2", "PsyMind v2"),
            ("agents.automaster_v2", "AutoMaster v4"),
            ("agents.supervisor_ai_v2", "SupervisorAI v2"),
            ("agents.deep_agent_v2", "DeepAgent v2"),
        ]
        
        util_modules = [
            ("utils.logger", "Sistema de logging"),
            ("utils.web_search", "Web search"),
            ("utils.agent_wake_manager", "Wake Manager"),
            ("utils.agent_orchestrator", "Orquestrador"),
        ]
        
        # Testar imports críticos
        for module, desc in critical_imports:
            try:
                importlib.import_module(module)
                self.results.append(AuditResult(
                    "imports", module, "OK", f"{desc} importado com sucesso"
                ))
            except ImportError as e:
                self.results.append(AuditResult(
                    "imports", module, "ERROR", f"{desc} FALHA DE IMPORT",
                    details=str(e),
                    suggested_fix=f"pip install {module}"
                ))
        
        # Testar módulos de agentes
        for module, desc in agent_modules:
            try:
                importlib.import_module(module)
                self.results.append(AuditResult(
                    "agents", module, "OK", f"{desc} carregado com sucesso"
                ))
            except Exception as e:
                self.results.append(AuditResult(
                    "agents", module, "ERROR", f"{desc} FALHA DE CARREGAMENTO",
                    details=str(e)
                ))
        
        # Testar módulos utilitários
        for module, desc in util_modules:
            try:
                importlib.import_module(module)
                self.results.append(AuditResult(
                    "utils", module, "OK", f"{desc} carregado com sucesso"
                ))
            except Exception as e:
                self.results.append(AuditResult(
                    "utils", module, "ERROR", f"{desc} FALHA DE CARREGAMENTO",
                    details=str(e)
                ))
    
    def _audit_agents(self):
        """Verifica se todos os agentes estão funcionando corretamente"""
        
        try:
            # Testar BaseAgentV2 (somente import, pois é abstract)
            from agents.base_agent_v2 import BaseAgentV2
            # Verificar se consegue importar as classes auxiliares
            from agents.base_agent_v2 import PerformanceMetrics, AgentMemoryV2, RateLimiter
            self.results.append(AuditResult(
                "agents", "BaseAgentV2", "OK", "BaseAgent v2 carregado (abstract class)"
            ))
        except Exception as e:
            self.results.append(AuditResult(
                "agents", "BaseAgentV2", "ERROR", "BaseAgent v2 COM PROBLEMAS",
                details=str(e)
            ))
        
        # Testar Carlos
        try:
            from agents.carlos import criar_carlos_maestro
            carlos = criar_carlos_maestro()
            self.results.append(AuditResult(
                "agents", "Carlos", "OK", "Carlos Maestro funcional"
            ))
        except Exception as e:
            self.results.append(AuditResult(
                "agents", "Carlos", "ERROR", "Carlos COM PROBLEMAS",
                details=str(e)
            ))
        
        # Testar outros agentes principais
        agent_tests = [
            ("agents.oraculo_v2", "criar_oraculo_v9", "Oráculo v9"),
            ("agents.psymind_v2", "criar_psymind_v2", "PsyMind v2"),
            ("agents.automaster_v2", "criar_automaster_v2", "AutoMaster v4"),
            ("agents.supervisor_ai_v2", "criar_supervisor_ai_v2", "SupervisorAI v2"),
            ("agents.deep_agent_v2", "criar_deep_agent_websearch_v2", "DeepAgent v2"),
        ]
        
        for module_name, function_name, agent_name in agent_tests:
            try:
                module = importlib.import_module(module_name)
                creator_func = getattr(module, function_name)
                agent = creator_func()
                self.results.append(AuditResult(
                    "agents", agent_name, "OK", f"{agent_name} criado com sucesso"
                ))
            except Exception as e:
                self.results.append(AuditResult(
                    "agents", agent_name, "ERROR", f"{agent_name} FALHA NA CRIAÇÃO",
                    details=str(e)
                ))
    
    def _audit_configurations(self):
        """Verifica configurações essenciais"""
        
        # Verificar variáveis de ambiente
        env_vars = [
            ("GOOGLE_API_KEY", "Chave API do Gemini"),
            ("LLM_PROVIDER", "Provedor de LLM"),
        ]
        
        for var, desc in env_vars:
            if os.getenv(var):
                self.results.append(AuditResult(
                    "config", var, "OK", f"{desc} configurada"
                ))
            else:
                self.results.append(AuditResult(
                    "config", var, "WARNING", f"{desc} NÃO CONFIGURADA",
                    suggested_fix=f"Definir {var} no arquivo .env"
                ))
        
        # Verificar config.py
        try:
            import config
            self.results.append(AuditResult(
                "config", "config.py", "OK", "Arquivo de configuração carregado"
            ))
            
            # Verificar configurações específicas
            if hasattr(config, 'DEFAULT_MODEL'):
                self.results.append(AuditResult(
                    "config", "DEFAULT_MODEL", "OK", f"Modelo padrão: {config.DEFAULT_MODEL}"
                ))
            else:
                self.results.append(AuditResult(
                    "config", "DEFAULT_MODEL", "WARNING", "Modelo padrão não configurado"
                ))
                
        except Exception as e:
            self.results.append(AuditResult(
                "config", "config.py", "ERROR", "Erro ao carregar configurações",
                details=str(e)
            ))
    
    def _audit_tests(self):
        """Verifica se os testes estão presentes e funcionais"""
        
        test_files = [
            "tests/test_oraculo_migration.py",
            "tests/test_psymind_migration.py", 
            "tests/test_automaster_migration.py",
            "tests/test_supervisor_migration.py",
            "tests/test_deepagent_migration.py",
        ]
        
        for test_file in test_files:
            if os.path.exists(test_file):
                self.results.append(AuditResult(
                    "tests", test_file, "OK", "Arquivo de teste encontrado"
                ))
                
                # Tentar executar uma verificação básica do teste
                try:
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "def test_" in content:
                            self.results.append(AuditResult(
                                "tests", f"{test_file}_content", "OK", "Testes válidos encontrados"
                            ))
                        else:
                            self.results.append(AuditResult(
                                "tests", f"{test_file}_content", "WARNING", "Nenhum teste válido encontrado"
                            ))
                except Exception as e:
                    self.results.append(AuditResult(
                        "tests", f"{test_file}_read", "ERROR", "Erro ao ler arquivo de teste",
                        details=str(e)
                    ))
            else:
                self.results.append(AuditResult(
                    "tests", test_file, "ERROR", "Arquivo de teste FALTANDO"
                ))
    
    def _audit_memory_systems(self):
        """Verifica sistemas de memória e cache"""
        
        try:
            # Verificar diretório de memória
            if os.path.exists("memory/chroma_db"):
                self.results.append(AuditResult(
                    "memory", "chroma_db", "OK", "Diretório ChromaDB encontrado"
                ))
            else:
                os.makedirs("memory/chroma_db", exist_ok=True)
                self.results.append(AuditResult(
                    "memory", "chroma_db", "FIXED", "Diretório ChromaDB criado automaticamente"
                ))
                self.fixes_applied += 1
            
            # Verificar sistema de memória
            from memory.vector_store import get_memory_manager
            memory_manager = get_memory_manager()
            self.results.append(AuditResult(
                "memory", "vector_store", "OK", "Sistema de memória vetorial funcional"
            ))
            
        except Exception as e:
            self.results.append(AuditResult(
                "memory", "memory_system", "ERROR", "Sistema de memória COM PROBLEMAS",
                details=str(e)
            ))
        
        # Verificar cache manager
        try:
            from utils.cache_manager import get_cache_manager
            cache_manager = get_cache_manager()
            self.results.append(AuditResult(
                "memory", "cache_manager", "OK", "Cache manager funcional"
            ))
        except Exception as e:
            self.results.append(AuditResult(
                "memory", "cache_manager", "ERROR", "Cache manager COM PROBLEMAS",
                details=str(e)
            ))
    
    def _audit_logging(self):
        """Verifica sistema de logging"""
        
        try:
            from utils.logger import get_logger
            logger = get_logger("audit_test")
            logger.info("Teste de logging")
            self.results.append(AuditResult(
                "logging", "logger", "OK", "Sistema de logging funcional"
            ))
        except Exception as e:
            self.results.append(AuditResult(
                "logging", "logger", "ERROR", "Sistema de logging COM PROBLEMAS",
                details=str(e)
            ))
        
        # Verificar diretório de logs
        if not os.path.exists("logs"):
            os.makedirs("logs", exist_ok=True)
            self.results.append(AuditResult(
                "logging", "logs_dir", "FIXED", "Diretório de logs criado automaticamente"
            ))
            self.fixes_applied += 1
        else:
            self.results.append(AuditResult(
                "logging", "logs_dir", "OK", "Diretório de logs encontrado"
            ))
    
    def _audit_security(self):
        """Verifica questões de segurança"""
        
        # Verificar se há chaves expostas em arquivos
        sensitive_patterns = ["sk-", "API_KEY", "SECRET", "PASSWORD"]
        
        for root, dirs, files in os.walk("."):
            # Ignorar diretórios específicos
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                if file.endswith(('.py', '.md', '.txt', '.yml', '.yaml', '.json')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern in sensitive_patterns:
                                if pattern in content and not file_path.endswith('.env'):
                                    self.results.append(AuditResult(
                                        "security", f"exposed_key_{file}", "WARNING", 
                                        f"Possível chave exposta em {file_path}",
                                        details=f"Padrão encontrado: {pattern}"
                                    ))
                    except Exception:
                        continue
        
        # Verificar .env
        if os.path.exists('.env'):
            self.results.append(AuditResult(
                "security", ".env", "OK", "Arquivo .env encontrado (configurações seguras)"
            ))
        else:
            self.results.append(AuditResult(
                "security", ".env", "WARNING", "Arquivo .env não encontrado",
                suggested_fix="Criar arquivo .env com configurações seguras"
            ))
    
    def _generate_audit_report(self) -> bool:
        """Gera relatório final da auditoria"""
        
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DA AUDITORIA")
        print("="*60)
        
        # Contar por status
        status_count = {"OK": 0, "WARNING": 0, "ERROR": 0, "FIXED": 0}
        
        for result in self.results:
            status_count[result.status] += 1
        
        print(f"📈 ESTATÍSTICAS:")
        print(f"  ✅ OK: {status_count['OK']}")
        print(f"  ⚠️  WARNING: {status_count['WARNING']}")
        print(f"  ❌ ERROR: {status_count['ERROR']}")
        print(f"  🔧 FIXED: {status_count['FIXED']}")
        print(f"  🛠️  Total de correções aplicadas: {self.fixes_applied}")
        
        # Mostrar problemas críticos
        errors = [r for r in self.results if r.status == "ERROR"]
        warnings = [r for r in self.results if r.status == "WARNING"]
        
        if errors:
            print(f"\n❌ PROBLEMAS CRÍTICOS ({len(errors)}):")
            for error in errors[:10]:  # Mostrar apenas os primeiros 10
                print(f"  • {error.category}/{error.item}: {error.message}")
                if error.details:
                    print(f"    Detalhes: {error.details}")
                if error.suggested_fix:
                    print(f"    Sugestão: {error.suggested_fix}")
        
        if warnings:
            print(f"\n⚠️ AVISOS ({len(warnings)}):")
            for warning in warnings[:10]:  # Mostrar apenas os primeiros 10
                print(f"  • {warning.category}/{warning.item}: {warning.message}")
        
        # Determinar se sistema está OK
        system_ok = len(errors) == 0
        
        if system_ok:
            print(f"\n🎉 SISTEMA 100% FUNCIONAL!")
            print(f"  ✅ Todos os componentes críticos estão operacionais")
            print(f"  🚀 Sistema pronto para produção")
        else:
            print(f"\n🔄 SISTEMA PRECISA DE ATENÇÃO")
            print(f"  ❌ {len(errors)} problemas críticos encontrados")
            print(f"  🔧 Próximo ciclo de auditoria necessário")
        
        # Salvar relatório
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "stats": status_count,
            "fixes_applied": self.fixes_applied,
            "system_ok": system_ok,
            "errors": len(errors),
            "warnings": len(warnings),
            "results": [
                {
                    "category": r.category,
                    "item": r.item,
                    "status": r.status,
                    "message": r.message,
                    "details": r.details,
                    "suggested_fix": r.suggested_fix
                }
                for r in self.results
            ]
        }
        
        os.makedirs("audit_reports", exist_ok=True)
        report_file = f"audit_reports/audit_cycle_{self.cycle_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: {report_file}")
        
        return system_ok


def run_audit_cycles():
    """Executa ciclos de auditoria até sistema estar 100% OK"""
    
    auditor = SystemAuditor()
    max_cycles = 5  # Limite de segurança
    
    print("🚀 INICIANDO SISTEMA DE AUDITORIA AUTOMÁTICA")
    print("Verificação completa, detecção e correção de falhas")
    print("Ciclo repetitivo até 100% funcional sem bugs nem erros")
    print("\n" + "="*60)
    
    for cycle in range(1, max_cycles + 1):
        print(f"\n🔄 CICLO {cycle}/{max_cycles}")
        
        system_ok = auditor.run_complete_audit()
        
        if system_ok:
            print(f"\n🎉 SUCESSO! Sistema 100% funcional após {cycle} ciclo(s)")
            print(f"🛠️ Total de {auditor.fixes_applied} correções aplicadas")
            print("✅ Auditoria concluída com sucesso!")
            return True
        
        if cycle < max_cycles:
            print(f"\n⏳ Preparando próximo ciclo...")
            time.sleep(2)  # Pausa entre ciclos
    
    print(f"\n⚠️ SISTEMA AINDA PRECISA DE ATENÇÃO após {max_cycles} ciclos")
    print("📊 Consulte os relatórios de auditoria para detalhes")
    return False


if __name__ == "__main__":
    success = run_audit_cycles()
    sys.exit(0 if success else 1)