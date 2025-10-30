import logging
import json
import os
from datetime import datetime
from typing import Dict, Any

class TestLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._ensure_log_directory()
        self._setup_loggers()
    
    def _ensure_log_directory(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _setup_loggers(self):
        self.main_logger = logging.getLogger('ecommerce_tests')
        self.main_logger.setLevel(logging.INFO)
        
        self.metrics_logger = logging.getLogger('test_metrics')
        self.metrics_logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        main_handler = logging.FileHandler(
            f'{self.log_dir}/execucao_testes_{timestamp}.log',
            encoding='utf-8'
        )
        main_handler.setFormatter(formatter)
        
        metrics_handler = logging.FileHandler(
            f'{self.log_dir}/metricas_testes_{timestamp}.log',
            encoding='utf-8'
        )
        metrics_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.main_logger.addHandler(main_handler)
        self.main_logger.addHandler(console_handler)
        
        self.metrics_logger.addHandler(metrics_handler)
        self.metrics_logger.addHandler(console_handler)
    
    def log_test_start(self, test_name: str, config: Dict[str, Any] = None):
        self.main_logger.info(f"INICIANDO: {test_name}")
        if config:
            self.main_logger.info(f"Configuração: {json.dumps(config, indent=2)}")
    
    def log_test_end(self, test_name: str, results: Dict[str, Any]):
        self.main_logger.info(f"CONCLUÍDO: {test_name}")
        self.main_logger.info(f"Duração: {results.get('duration_seconds', 'N/A')}s")
        
        self.metrics_logger.info(f"MÉTRICAS - {test_name}:")
        self.metrics_logger.info(json.dumps(results, indent=2, ensure_ascii=False))
    
    def log_test_error(self, test_name: str, error: str):
        self.main_logger.error(f"ERRO em {test_name}: {error}")
    
    def log_suite_start(self, total_tests: int):
        self.main_logger.info("="*80)
        self.main_logger.info("INICIANDO SUITE DE TESTES DE E-COMMERCE")
        self.main_logger.info(f"Total de testes: {total_tests}")
        self.main_logger.info(f"Timestamp: {datetime.now().isoformat()}")
        self.main_logger.info("="*80)
    
    def log_suite_end(self, summary: Dict[str, Any]):
        self.main_logger.info("="*80)
        self.main_logger.info("🏁 SUITE DE TESTES CONCLUÍDA")
        self.main_logger.info(f"Total executados: {summary.get('total_tests', 0)}")
        self.main_logger.info(f"Aprovados: {summary.get('passed_tests', 0)}")
        self.main_logger.info(f"Reprovados: {summary.get('failed_tests', 0)}")
        self.main_logger.info(f"Taxa de sucesso: {summary.get('success_rate', 0):.1f}%")
        self.main_logger.info(f"Timestamp fim: {datetime.now().isoformat()}")
        self.main_logger.info("="*80)
    
    def log_progress(self, message: str):
        self.main_logger.info(f"{message}")
    
    def log_metric(self, test_name: str, metric_name: str, value: Any, target: Any = None, passed: bool = None):
        status = ""
        if passed is not None:
            status = "PASSOU" if passed else "FALHOU"
        
        if target is not None:
            self.metrics_logger.info(f"{test_name} | {metric_name}: {value} (Meta: {target}) {status}")
        else:
            self.metrics_logger.info(f"{test_name} | {metric_name}: {value}")

test_logger = TestLogger()