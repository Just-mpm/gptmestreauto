"""
Dashboard ASCII Art para Monitoramento de Tokens
GPT Mestre Autônomo - Interface Visual
"""

import os
import sys
from datetime import timedelta
from typing import Dict, List
from colorama import init, Fore, Back, Style

# Inicializar colorama para cores no terminal (funciona em Windows também)
try:
    init(autoreset=True)
    COLORS_ENABLED = True
except:
    COLORS_ENABLED = False

from utils.token_monitor import get_token_monitor


class DashboardDisplay:
    """Classe para exibir dashboard ASCII no terminal"""
    
    def __init__(self):
        self.monitor = get_token_monitor()
        self.width = 65  # Largura do dashboard
    
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_time(self, td: timedelta) -> str:
        """Formata timedelta para HH:MM:SS"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def format_currency(self, value: float) -> str:
        """Formata valor em reais"""
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def color_text(self, text: str, color: str) -> str:
        """Adiciona cor ao texto se disponível"""
        if not COLORS_ENABLED:
            return text
        
        color_map = {
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'red': Fore.RED,
            'blue': Fore.BLUE,
            'cyan': Fore.CYAN,
            'magenta': Fore.MAGENTA,
            'white': Fore.WHITE
        }
        
        return f"{color_map.get(color, '')}{text}{Style.RESET_ALL}"
    
    def create_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Cria uma barra de progresso ASCII"""
        filled = int(width * percentage / 100)
        empty = width - filled
        
        if percentage >= 95:
            color = 'red'
        elif percentage >= 70:
            color = 'yellow'
        else:
            color = 'green'
        
        bar = '█' * filled + '░' * empty
        return self.color_text(f"[{bar}]", color)
    
    def display(self, clear: bool = True):
        """Exibe o dashboard completo"""
        if clear:
            self.clear_screen()
        
        # Obter dados
        data = self.monitor.get_dashboard_data()
        usage = data['usage']
        prediction = data['prediction']
        status = data['status']
        status_color_map = {'OK': 'green', 'ALERTA': 'yellow', 'CRÍTICO': 'red'}
        
        # Construir dashboard
        lines = []
        
        # Header
        lines.append("+" + "-" * (self.width - 2) + "+")
        lines.append("|" + self.color_text("        🚀 GPT Mestre Autônomo - Monitoramento Max 5x       ", 'cyan').center(self.width + 10) + "|")
        lines.append("+" + "-" * (self.width - 2) + "+")
        
        # Tempo do ciclo
        remaining = self.format_time(usage['remaining_time'])
        lines.append(f"| Ciclo Atual: {self.color_text(remaining, 'blue')} Restantes (HH:MM:SS)" + " " * 18 + "|")
        lines.append("|" + " " * (self.width - 2) + "|")
        
        # Métricas principais
        cost_color = 'red' if usage['estimated_cost_brl'] > 10 else 'yellow' if usage['estimated_cost_brl'] > 5 else 'green'
        lines.append(f"|   ⚡ Custo Total (Ciclo): {self.color_text(self.format_currency(usage['estimated_cost_brl']), cost_color)}" + " " * 26 + "|")
        lines.append(f"|   📊 Tokens Total (Ciclo): {self.color_text(f'{usage["total_tokens"]:,}', 'cyan')}" + " " * 23 + "|")
        
        # Barra de progresso da cota
        quota_bar = self.create_progress_bar(usage['quota_percentage'])
        lines.append(f"|   🎯 % Cota Usada: {usage['quota_percentage']:5.1f}% {quota_bar}" + " " * 11 + "|")
        lines.append("|" + " " * (self.width - 2) + "|")
        
        # Velocidade e custo médio
        velocity_color = 'red' if usage['tokens_per_minute'] > 200 else 'yellow' if usage['tokens_per_minute'] > 100 else 'green'
        lines.append(f"|   📈 Velocidade de Consumo: {self.color_text(f'{usage["tokens_per_minute"]:.0f}', velocity_color)} T/min" + " " * 17 + "|")
        lines.append(f"|   💰 Custo Médio/Req: {self.format_currency(usage['cost_per_request'])}" + " " * 27 + "|")
        lines.append("|" + " " * (self.width - 2) + "|")
        
        # Top consumidores
        lines.append(f"|   🔥 {self.color_text('Agentes Top Consumidores:', 'yellow')}" + " " * 31 + "|")
        
        for agent, data in usage['top_consumers'][:3]:
            agent_line = f"     - {agent[:15]:15}: {data['total_tokens']:6,} T / {self.format_currency(data['cost_brl'])}"
            # Ajustar espaçamento
            padding = self.width - len(agent_line) - 3
            lines.append(f"|{agent_line}" + " " * padding + "|")
        
        lines.append("|" + " " * (self.width - 2) + "|")
        
        # Status do sistema
        status_text = f"{data['status_color']} Status: {self.color_text(status, status_color_map.get(status, 'white'))}"
        
        # Adicionar mensagem de alerta se houver
        if usage.get('alerts'):
            latest_alert = usage['alerts'][-1]
            alert_msg = latest_alert['message'][:40] + "..."
            status_text += f" - {alert_msg}"
        
        lines.append(f"|   {status_text}" + " " * (self.width - len(status_text) - 7) + "|")
        lines.append("|" + " " * (self.width - 2) + "|")
        
        # Footer
        lines.append("+" + "-" * (self.width - 2) + "+")
        lines.append("| Digite '/status' para atualizar ou '/help' para comandos.   |")
        lines.append("+" + "-" * (self.width - 2) + "+")
        
        # Previsão mensal
        lines.append("")
        lines.append(self.color_text("📊 PREVISÃO DE CUSTOS:", 'cyan'))
        lines.append(f"   Diário: {self.format_currency(prediction['daily_cost_brl'])} ({prediction['daily_tokens']:,} tokens)")
        
        monthly_color = 'red' if prediction['monthly_cost_brl'] > 100 else 'yellow' if prediction['monthly_cost_brl'] > 50 else 'green'
        lines.append(f"   Mensal: {self.color_text(self.format_currency(prediction['monthly_cost_brl']), monthly_color)} ({prediction['monthly_tokens']:,} tokens)")
        
        # Sugestões de otimização
        suggestions = self.monitor.get_optimization_suggestions()
        if suggestions:
            lines.append("")
            lines.append(self.color_text("💡 SUGESTÕES DE OTIMIZAÇÃO:", 'yellow'))
            for suggestion in suggestions[:3]:
                lines.append(f"   {suggestion}")
        
        # Imprimir tudo
        print("\n".join(lines))
    
    def display_compact(self) -> str:
        """Retorna versão compacta do dashboard para logs"""
        data = self.monitor.get_dashboard_data()
        usage = data['usage']
        
        return (
            f"📊 Tokens: {usage['total_tokens']:,} | "
            f"💰 Custo: {self.format_currency(usage['estimated_cost_brl'])} | "
            f"🎯 Cota: {usage['quota_percentage']:.1f}% | "
            f"📈 Vel: {usage['tokens_per_minute']:.0f} T/min"
        )


def show_dashboard(clear: bool = True):
    """Função helper para mostrar o dashboard"""
    dashboard = DashboardDisplay()
    dashboard.display(clear)


def get_dashboard_summary() -> str:
    """Retorna resumo compacto do dashboard"""
    dashboard = DashboardDisplay()
    return dashboard.display_compact()


if __name__ == "__main__":
    # Teste do dashboard
    monitor = get_token_monitor()
    
    # Simular alguns dados
    monitor.log_tokens("CarlosMaestroV5", 500, 250)
    monitor.log_tokens("OraculoV9", 300, 150)
    monitor.log_tokens("CreativeMindV1", 200, 100)
    monitor.log_tokens("DeepAgent", 150, 75)
    monitor.log_tokens("Reflexor", 100, 50)
    
    # Mostrar dashboard
    show_dashboard()