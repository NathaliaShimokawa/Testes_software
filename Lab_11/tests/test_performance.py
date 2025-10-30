"""
Teste de Performance - Tempo de Resposta P95
Meta: < 500ms para 95% das requisições
"""
import requests
import time
import statistics
from test_framework import TestMetrics, TEST_CONFIG

def run_performance_test():
    metrics = TestMetrics()
    metrics.start_test("Teste de Performance - P95")
    
    url = f"{TEST_CONFIG['base_url']}/delay/0.1"  
    num_requests = 100
    response_times = []
    successful_requests = 0
    
    print(f"Iniciando teste de performance com {num_requests} requisições...")
    
    for i in range(num_requests):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=TEST_CONFIG['timeout'])
            response_time_ms = (time.time() - start_time) * 1000
            
            response_times.append(response_time_ms)
            
            if response.status_code == 200:
                successful_requests += 1
                
            if (i + 1) % 20 == 0:
                print(f"Progresso: {i + 1}/{num_requests} requisições")
                
        except Exception as e:
            print(f"Erro na requisição {i + 1}: {e}")
            response_times.append(5000)
    
    if response_times:
        response_times.sort()
        p50 = statistics.median(response_times)
        p90 = response_times[int(0.90 * len(response_times))]
        p95 = response_times[int(0.95 * len(response_times))]
        p99 = response_times[int(0.99 * len(response_times))]
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
    else:
        p50 = p90 = p95 = p99 = avg_time = min_time = max_time = 0
    
    success_rate = (successful_requests / num_requests) * 100
    
    metrics.add_metric('total_requests', num_requests)
    metrics.add_metric('successful_requests', successful_requests)
    metrics.add_metric('success_rate_pct', success_rate)
    metrics.add_metric('response_time_p50_ms', p50)
    metrics.add_metric('response_time_p90_ms', p90)
    metrics.add_metric('response_time_p95_ms', p95)
    metrics.add_metric('response_time_p99_ms', p99)
    metrics.add_metric('response_time_avg_ms', avg_time)
    metrics.add_metric('response_time_min_ms', min_time)
    metrics.add_metric('response_time_max_ms', max_time)
    
    target_p95 = TEST_CONFIG['targets']['performance_p95_ms']
    passed = metrics.evaluate_target(p95, target_p95, 'less_than', 'performance_p95_ms')
    
    metrics.finish_test()
    

    print("\n" + "="*60)
    print("RESULTADOS DO TESTE DE PERFORMANCE")
    print("="*60)
    print(f"Total de requisições: {num_requests}")
    print(f"Requisições bem-sucedidas: {successful_requests}")
    print(f"Taxa de sucesso: {success_rate:.1f}%")
    print(f"Tempo de resposta P50: {p50:.2f}ms")
    print(f"Tempo de resposta P90: {p90:.2f}ms")
    print(f"Tempo de resposta P95: {p95:.2f}ms")
    print(f"Tempo de resposta P99: {p99:.2f}ms")
    print(f"Tempo médio: {avg_time:.2f}ms")
    print(f"Tempo mínimo: {min_time:.2f}ms")
    print(f"Tempo máximo: {max_time:.2f}ms")
    print(f"\nMETA P95 < {target_p95}ms: {'APROVADO' if passed else 'REPROVADO'}")
    
    return metrics.get_results()

if __name__ == "__main__":
    run_performance_test()
