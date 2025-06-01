#!/usr/bin/env python3
"""
GPT MESTRE AUTÔNOMO - Interface Terminal com Monitoramento
🤖 Carlos com Dashboard de Custos e Tokens
"""

import os
import sys
from datetime import datetime
import time

# Adicionar o diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports do sistema
try:
    from agents.carlos import criar_carlos_maestro
    from utils.logger import get_logger
    from utils.dashboard_display import show_dashboard, get_dashboard_summary
    from utils.token_monitor import get_token_monitor
    
    logger = get_logger("terminal_app")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    exit(1)


def print_header():
    """Imprime o header do sistema"""
    print("\n" + "="*60)
    print("🧠 GPT MESTRE AUTÔNOMO v5.0 - Terminal com Monitoramento")
    print("="*60)
    print("Digite sua mensagem ou comando:")
    print("  /status    - Exibe dashboard de monitoramento")
    print("  /resumo    - Exibe resumo compacto de custos")
    print("  /help      - Lista todos os comandos")
    print("  /sair      - Encerra o sistema")
    print("="*60 + "\n")


def print_help():
    """Imprime ajuda detalhada"""
    print("\n📚 COMANDOS DISPONÍVEIS:")
    print("-" * 40)
    print("/status    - Dashboard completo com custos e métricas")
    print("/resumo    - Linha única com resumo de custos")
    print("/reset     - Reinicia o ciclo de monitoramento")
    print("/alertas   - Mostra alertas ativos")
    print("/agentes   - Lista consumo por agente")
    print("/help      - Esta mensagem de ajuda")
    print("/sair      - Encerra o sistema")
    print("-" * 40)
    print("\n💡 DICAS:")
    print("- O monitoramento rastreia tokens e custos em tempo real")
    print("- Alertas automáticos quando se aproxima dos limites")
    print("- Cache inteligente economiza tokens automaticamente")
    print("- Use /status periodicamente para acompanhar gastos")
    print()


def show_agents_usage():
    """Mostra uso detalhado por agente"""
    monitor = get_token_monitor()
    usage = monitor.get_current_usage()
    
    print("\n📊 CONSUMO POR AGENTE:")
    print("-" * 50)
    print(f"{'Agente':<20} {'Tokens':>10} {'Custo':>10} {'%':>5}")
    print("-" * 50)
    
    # Ordenar por consumo
    agents_sorted = sorted(
        usage['agent_usage_data'].items(),
        key=lambda x: x[1]['total_tokens'],
        reverse=True
    )
    
    for agent, data in agents_sorted:
        if data['total_tokens'] > 0:
            print(f"{agent[:20]:<20} {data['total_tokens']:>10,} "
                  f"R$ {data['cost_brl']:>7.2f} {data['percentage']:>4.1f}%")
    
    print("-" * 50)
    print(f"{'TOTAL':<20} {usage['total_tokens']:>10,} "
          f"R$ {usage['estimated_cost_brl']:>7.2f} 100.0%")
    print()


def show_alerts():
    """Mostra alertas ativos"""
    monitor = get_token_monitor()
    usage = monitor.get_current_usage()
    
    alerts = usage.get('alerts', [])
    
    if not alerts:
        print("\n✅ Nenhum alerta ativo no momento!")
        return
    
    print(f"\n⚠️  ALERTAS ATIVOS ({len(alerts)}):")
    print("-" * 60)
    
    for alert in alerts:
        timestamp = alert['timestamp'].strftime("%H:%M:%S")
        level_icon = "🔴" if alert['level'] == "CRITICAL" else "🟡"
        print(f"{level_icon} [{timestamp}] {alert['message']}")
    
    print("-" * 60)
    print()


def main():
    """Loop principal do terminal"""
    carlos = None
    
    print_header()
    
    # Inicializar Carlos
    print("🚀 Inicializando Carlos...")
    try:
        carlos = criar_carlos_maestro(
            supervisor_ativo=True,
            reflexor_ativo=True,
            deepagent_ativo=True,
            oraculo_ativo=True,
            automaster_ativo=True,
            taskbreaker_ativo=True,
            psymind_ativo=True,
            promptcrafter_ativo=True,
            memoria_ativa=True,
            modo_proativo=True,
            inovacoes_ativas=True
        )
        print("✅ Carlos inicializado com sucesso!")
        print(f"\n💡 {get_dashboard_summary()}\n")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar Carlos: {e}")
        return
    
    # Loop principal
    while True:
        try:
            # Prompt
            user_input = input("Você: ").strip()
            
            if not user_input:
                continue
            
            # Processar comandos
            if user_input.lower() == "/sair":
                print("\n👋 Até logo!")
                break
                
            elif user_input.lower() == "/status":
                show_dashboard()
                continue
                
            elif user_input.lower() == "/resumo":
                print(f"\n{get_dashboard_summary()}\n")
                continue
                
            elif user_input.lower() == "/help":
                print_help()
                continue
                
            elif user_input.lower() == "/agentes":
                show_agents_usage()
                continue
                
            elif user_input.lower() == "/alertas":
                show_alerts()
                continue
                
            elif user_input.lower() == "/reset":
                monitor = get_token_monitor()
                monitor.reset_cycle()
                print("\n🔄 Ciclo de monitoramento resetado!\n")
                continue
            
            # Processar mensagem normal
            print("\n🤔 Processando...", end='', flush=True)
            
            start_time = time.time()
            response = carlos.processar(user_input, {})
            elapsed = time.time() - start_time
            
            # Limpar linha de "Processando"
            print("\r" + " " * 20 + "\r", end='')
            
            # Mostrar resposta
            print(f"Carlos: {response}")
            
            # Mostrar métricas inline
            monitor = get_token_monitor()
            usage = monitor.get_current_usage()
            last_cost = usage['cost_per_request']
            
            print(f"\n⏱️  {elapsed:.1f}s | 💰 R$ {last_cost:.2f} | "
                  f"📊 {usage['total_tokens']:,} tokens | "
                  f"🎯 {usage['quota_percentage']:.1f}% da cota\n")
            
            # Verificar se há alertas novos
            if usage.get('alerts'):
                latest_alert = usage['alerts'][-1]
                # Se o alerta foi nos últimos 30 segundos
                if (datetime.now() - latest_alert['timestamp']).seconds < 30:
                    level_icon = "🔴" if latest_alert['level'] == "CRITICAL" else "🟡"
                    print(f"{level_icon} ALERTA: {latest_alert['message']}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
            
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")
            logger.error(f"Erro no processamento: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        logger.error(f"Erro fatal: {e}", exc_info=True)