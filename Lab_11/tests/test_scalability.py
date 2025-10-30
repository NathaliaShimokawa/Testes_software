import requests
import threading
import time
import statistics
from test_framework import TestMetrics, TEST_CONFIG

def run_scalability_test():
    metrics = TestMetrics()
    metrics.start_test("Teste de Escalabilidade - Eficiência Horizontal")
    
    url = f"{TEST_CONFIG['base_url']}/delay/0.1"
    base_load = 100 
    max_instances = 10
    
    print("Iniciando teste de escalabilidade...")
    print(f"Carga base: {base_load} requisições por instância")
    print(f"Máximo de instâncias: {max_instances}")
    
    baseline_throughput = None
    efficiency_data = []
    
    for instances in range(1, max_instances + 1):
        print(f"\n--- Testando {instances} instância(s) ---")
        
        total_requests = base_load * instances
        threads = []
        results = {
            'successful_requests': 0,
            'response_times': []
        }
        results_lock = threading.Lock()
        
        def worker():
            try:
                start_time = time.time()
                response = requests.get(url, timeout=TEST_CONFIG['timeout'])
                response_time = time.time() - start_time
                
                with results_lock:
                    results['response_times'].append(response_time)
                    if response.status_code == 200:
                        results['successful_requests'] += 1
            except Exception:
                pass
        
        test_start = time.time()
        
        for _ in range(total_requests):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        test_duration = time.time() - test_start
        
        throughput = results['successful_requests'] / test_duration
        avg_response_time = statistics.mean(results['response_times']) if results['response_times'] else 0
        success_rate = (results['successful_requests'] / total_requests) * 100
        
        if instances == 1:
            baseline_throughput = throughput
            efficiency = 100.0
        else:
            theoretical_throughput = baseline_throughput * instances
            efficiency = (throughput / theoretical_throughput) * 100 if theoretical_throughput > 0 else 0
        
        efficiency_data.append({
            'instances': instances,
            'throughput': throughput,
            'efficiency': efficiency,
            'response_time': avg_response_time * 1000,  # ms
            'success_rate': success_rate
        })
        
        print(f"  Throughput: {throughput:.2f} req/s")
        print(f"  Eficiência: {efficiency:.1f}%")
        print(f"  Tempo médio: {avg_response_time*1000:.2f}ms")
        print(f"  Taxa de sucesso: {success_rate:.1f}%")
        

        target_efficiency = TEST_CONFIG['targets']['scalability_efficiency_pct']
        if efficiency < target_efficiency:
            print(f"Eficiência abaixo do alvo ({target_efficiency}%)")
    
    min_efficiency = min(data['efficiency'] for data in efficiency_data)
    avg_efficiency = statistics.mean(data['efficiency'] for data in efficiency_data)
    final_efficiency = efficiency_data[-1]['efficiency']  
    
    metrics.add_metric('baseline_throughput_rps', baseline_throughput)
    metrics.add_metric('max_instances_tested', max_instances)
    metrics.add_metric('min_efficiency_pct', min_efficiency)
    metrics.add_metric('avg_efficiency_pct', avg_efficiency)
    metrics.add_metric('final_efficiency_pct', final_efficiency)
    metrics.add_metric('efficiency_data', efficiency_data)
    
    target_efficiency = TEST_CONFIG['targets']['scalability_efficiency_pct']
    passed = metrics.evaluate_target(min_efficiency, target_efficiency, 'greater_than', 'scalability_efficiency_pct')
    
    metrics.finish_test()
    
    print("\n" + "="*60)
    print("RESULTADOS DO TESTE DE ESCALABILIDADE")
    print("="*60)
    print(f"Throughput baseline (1 instância): {baseline_throughput:.2f} req/s")
    print(f"Eficiência mínima: {min_efficiency:.1f}%")
    print(f"Eficiência média: {avg_efficiency:.1f}%")
    print(f"Eficiência final ({max_instances} instâncias): {final_efficiency:.1f}%")
    
    print(f"\nDetalhamento por número de instâncias:")
    for data in efficiency_data:
        print(f"  {data['instances']} instância(s): {data['throughput']:.1f} req/s, "
              f"{data['efficiency']:.1f}% eficiência")
    
    print(f"\nMETA EFICIÊNCIA > {target_efficiency}%: {'APROVADO' if passed else 'REPROVADO'}")
    
    return metrics.get_results()

if __name__ == "__main__":
    run_scalability_test()
