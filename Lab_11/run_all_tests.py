import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

from test_logger import test_logger
from test_framework import ReportGenerator
from test_performance import run_performance_test
from test_load import run_load_test
from test_stress import run_stress_test
from test_scalability import run_scalability_test
from test_security import run_security_test

def main():
    print("="*80)
    print("SUITE DE TESTES DE E-COMMERCE - BLACK FRIDAY 2025")
    print("="*80)
    print(f"Início da execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    report_gen = ReportGenerator()
    test_results = []
    
    test_logger.log_suite_start(5)
    
    tests = [
        ("Performance (P95)", run_performance_test),
        ("Carga (Throughput)", run_load_test),
        ("Estresse (Ponto de Quebra)", run_stress_test),
        ("Escalabilidade (Eficiência)", run_scalability_test),
        ("Segurança (Rate Limiting)", run_security_test)
    ]
    
    for i, (test_name, test_function) in enumerate(tests, 1):
        print(f"\n{'='*20} TESTE {i}/5: {test_name.upper()} {'='*20}")
        
        try:
            start_time = datetime.now()
            test_logger.log_progress(f"Executando {test_name}...")
            
            result = test_function()
            end_time = datetime.now()
            
            test_results.append(result)
            report_gen.add_test_result(result)
            
            duration = (end_time - start_time).total_seconds()
            print(f"\n{test_name} concluído em {duration:.1f}s")
            test_logger.log_progress(f"{test_name} concluído em {duration:.1f}s")
            
        except Exception as e:
            error_msg = str(e)
            print(f"\nErro no teste {test_name}: {error_msg}")
            test_logger.log_test_error(test_name, error_msg)
            
            error_result = {
                'test_name': test_name,
                'start_timestamp': start_time.isoformat(),
                'end_timestamp': datetime.now().isoformat(),
                'duration_seconds': 0,
                'results': {
                    'error': error_msg,
                    'status': 'FAILED'
                }
            }
            test_results.append(error_result)
            report_gen.add_test_result(error_result)
    
    print(f"\n{'='*80}")
    print("RESUMO EXECUTIVO")
    print(f"{'='*80}")
    
    total_tests = len(test_results)
    passed_tests = 0
    failed_tests = 0
    
    for result in test_results:
        test_passed = False
        for key, value in result['results'].items():
            if key.endswith('_passed') and value:
                test_passed = True
                break
        
        if test_passed:
            passed_tests += 1
        else:
            failed_tests += 1
        
        status_icon = "Passed" if test_passed else "Error"
        print(f"{status_icon} {result['test_name']}: {'APROVADO' if test_passed else 'REPROVADO'}")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    suite_summary = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'success_rate': success_rate
    }
    test_logger.log_suite_end(suite_summary)
    
    print(f"\nESTATÍSTICAS GERAIS:")
    print(f"   • Total de testes: {total_tests}")
    print(f"   • Testes aprovados: {passed_tests}")
    print(f"   • Testes reprovados: {failed_tests}")
    print(f"   • Taxa de aprovação: {success_rate:.1f}%")
    
    print(f"\nAVALIAÇÃO DE PRONTIDÃO PARA BLACK FRIDAY:")
    
    if success_rate >= 80:
        readiness = "SISTEMA PRONTO"
        recommendation = "Sistema atende aos requisitos mínimos para o evento."
    elif success_rate >= 60:
        readiness = "SISTEMA PARCIALMENTE PRONTO"
        recommendation = "Alguns ajustes necessários antes do evento."
    else:
        readiness = "SISTEMA NÃO PRONTO"
        recommendation = "Ajustes críticos necessários antes do evento."
    
    print(f"   {readiness}")
    print(f"   Recomendação: {recommendation}")
    
    report_filename = f"relatorio_testes_ecommerce_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_content = report_gen.generate_report(report_filename)
    
    print(f"\nRELATÓRIO DETALHADO:")
    print(f"   • Arquivo: {report_filename}")
    print(f"   • Localização: {os.path.abspath(report_filename)}")
    
    test_logger.log_progress(f"Relatório gerado: {report_filename}")
    test_logger.log_progress(f"Logs salvos em: logs/")
    
    print(f"\nMÉTRICAS CRÍTICAS:")
    for result in test_results:
        print(f"\n{result['test_name']}:")
        for key, value in result['results'].items():
            if any(metric in key.lower() for metric in ['p95', 'throughput', 'breakpoint', 'efficiency', 'rate_limit']):
                if isinstance(value, (int, float)):
                    print(f"   • {key}: {value:.2f}")
                else:
                    print(f"   • {key}: {value}")
    
    print(f"\n{'='*80}")
    print(f"EXECUÇÃO CONCLUÍDA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    return test_results

if __name__ == "__main__":
    main()