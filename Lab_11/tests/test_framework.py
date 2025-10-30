import time
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from test_logger import test_logger

class TestMetrics:
    def __init__(self):
        self.metrics = {}
        self.start_time = None
        self.end_time = None
    
    def start_test(self, test_name: str):
        self.test_name = test_name
        self.start_time = time.time()
        self.metrics = {
            'test_name': test_name,
            'start_timestamp': datetime.now().isoformat(),
            'results': {}
        }
        # Log início do teste
        test_logger.log_test_start(test_name, TEST_CONFIG)
    
    def add_metric(self, key: str, value: Any):
        self.metrics['results'][key] = value
        # Log da métrica
        test_logger.log_metric(self.test_name, key, value)
    
    def finish_test(self):
        self.end_time = time.time()
        self.metrics['end_timestamp'] = datetime.now().isoformat()
        self.metrics['duration_seconds'] = self.end_time - self.start_time
        # Log fim do teste
        test_logger.log_test_end(self.test_name, self.metrics)
    
    def evaluate_target(self, actual_value: float, target_value: float, 
                       comparison: str = 'less_than', metric_name: str = ''):
        if comparison == 'less_than':
            passed = actual_value < target_value
        elif comparison == 'greater_than':
            passed = actual_value > target_value
        else:
            passed = actual_value == target_value
        
        self.metrics['results'][f'{metric_name}_target'] = target_value
        self.metrics['results'][f'{metric_name}_actual'] = actual_value
        self.metrics['results'][f'{metric_name}_passed'] = passed

        test_logger.log_metric(self.test_name, f"{metric_name}_avaliacao", 
                              actual_value, target_value, passed)
        
        return passed
    
    def get_results(self):
        return self.metrics

class ReportGenerator:
    def __init__(self):
        self.test_results = []
    
    def add_test_result(self, metrics: Dict):
        self.test_results.append(metrics)
    
    def generate_report(self, output_file: str = 'test_report.md'):
        report_content = self._generate_markdown_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_content
    
    def _generate_markdown_report(self):
        report = "# Relatório de Testes de E-commerce - Black Friday\n\n"
        report += f"**Data do Relatório:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
        report += "## Resumo Executivo\n\n"
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results 
                          if any(k.endswith('_passed') and v for k, v in test['results'].items()))
        
        report += f"- **Total de testes:** {total_tests}\n"
        report += f"- **Testes aprovados:** {passed_tests}\n"
        report += f"- **Taxa de aprovação:** {(passed_tests/total_tests)*100:.1f}%\n\n"
    
        report += "## Detalhes dos Testes\n\n"
        
        for test in self.test_results:
            report += f"### {test['test_name']}\n\n"
            report += f"- **Duração:** {test['duration_seconds']:.2f}s\n"
            report += f"- **Início:** {test['start_timestamp']}\n"
            report += f"- **Fim:** {test['end_timestamp']}\n\n"
            
            report += "**Métricas Coletadas:**\n\n"
            for key, value in test['results'].items():
                if not key.endswith('_passed'):
                    if isinstance(value, float):
                        report += f"- {key}: {value:.2f}\n"
                    else:
                        report += f"- {key}: {value}\n"
            
            report += "\n**Avaliação das Metas:**\n\n"
            for key, value in test['results'].items():
                if key.endswith('_passed'):
                    metric_name = key.replace('_passed', '')
                    status = "✅ APROVADO" if value else "❌ REPROVADO"
                    actual = test['results'].get(f'{metric_name}_actual', 'N/A')
                    target = test['results'].get(f'{metric_name}_target', 'N/A')
                    report += f"- {metric_name}: {status} (Valor: {actual}, Meta: {target})\n"
            
            report += "\n---\n\n"
        
        return report

TEST_CONFIG = {
    'base_url': 'https://httpbin.org', 
    'timeout': 5,
    'targets': {
        'performance_p95_ms': 500,
        'load_throughput_rps': 2000,
        'stress_breakpoint_users': 15000,
        'scalability_efficiency_pct': 80,
        'security_rate_limit_rpm': 100
    }
}