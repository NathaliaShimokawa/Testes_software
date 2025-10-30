import requests
import threading
import time
from threading import Lock
from test_framework import TestMetrics, TEST_CONFIG

def run_load_test():
    metrics = TestMetrics()
    metrics.start_test("Teste de Carga - Throughput")
    
    url = f"{TEST_CONFIG['base_url']}/delay/0.05" 
    num_threads = 50
    requests_per_thread = 40
    total_requests = num_threads * requests_per_thread
    
    results = {
        'successful_requests': 0,
        'failed_requests': 0,
        'response_times': [],
        'error_details': []
    }
    results_lock = Lock()
    
    print(f"Iniciando teste de carga...")
    print(f"Threads: {num_threads}")
    print(f"Requisições por thread: {requests_per_thread}")
    print(f"Total de requisições: {total_requests}")
    
    def worker(thread_id):
        local_success = 0
        local_failed = 0
        local_times = []
        local_errors = []
        
        for req_num in range(requests_per_thread):
            try:
                start_time = time.time()
                response = requests.get(url, timeout=TEST_CONFIG['timeout'])
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    local_success += 1
                    local_times.append(response_time * 1000) 
                else:
                    local_failed += 1
                    local_errors.append(f"HTTP {response.status_code}")
                    
            except Exception as e:
                local_failed += 1
                local_errors.append(str(e))

        with results_lock:
            results['successful_requests'] += local_success
            results['failed_requests'] += local_failed
            results['response_times'].extend(local_times)
            results['error_details'].extend(local_errors)
    
    start_time = time.time()
    threads = []
    
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    while any(t.is_alive() for t in threads):
        time.sleep(1)
        with results_lock:
            completed = results['successful_requests'] + results['failed_requests']
            if completed > 0:
                print(f"Progresso: {completed}/{total_requests} requisições completadas")
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    total_completed = results['successful_requests'] + results['failed_requests']
    success_rate = (results['successful_requests'] / total_completed) * 100 if total_completed > 0 else 0
    throughput = results['successful_requests'] / total_duration
    
    avg_response_time = sum(results['response_times']) / len(results['response_times']) if results['response_times'] else 0
    
    metrics.add_metric('total_requests', total_requests)
    metrics.add_metric('successful_requests', results['successful_requests'])
    metrics.add_metric('failed_requests', results['failed_requests'])
    metrics.add_metric('success_rate_pct', success_rate)
    metrics.add_metric('test_duration_seconds', total_duration)
    metrics.add_metric('throughput_rps', throughput)
    metrics.add_metric('avg_response_time_ms', avg_response_time)
    metrics.add_metric('concurrent_threads', num_threads)
    
    target_throughput = TEST_CONFIG['targets']['load_throughput_rps']
    passed = metrics.evaluate_target(throughput, target_throughput, 'greater_than', 'load_throughput_rps')
    
    metrics.finish_test()
    
    print("\n" + "="*60)
    print("RESULTADOS DO TESTE DE CARGA")
    print("="*60)
    print(f"Duração total: {total_duration:.2f}s")
    print(f"Total de requisições: {total_requests}")
    print(f"Requisições bem-sucedidas: {results['successful_requests']}")
    print(f"Requisições falhadas: {results['failed_requests']}")
    print(f"Taxa de sucesso: {success_rate:.1f}%")
    print(f"Throughput: {throughput:.2f} req/s")
    print(f"Tempo médio de resposta: {avg_response_time:.2f}ms")
    print(f"Threads concorrentes: {num_threads}")
    
    if results['error_details']:
        error_summary = {}
        for error in results['error_details']:
            error_summary[error] = error_summary.get(error, 0) + 1
        print(f"\nErros encontrados:")
        for error, count in error_summary.items():
            print(f"  - {error}: {count} ocorrências")
    
    print(f"\nMETA THROUGHPUT > {target_throughput} req/s: {'APROVADO' if passed else 'REPROVADO'}")
    
    return metrics.get_results()

if __name__ == "__main__":
    run_load_test()
