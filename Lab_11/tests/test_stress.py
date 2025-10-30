import requests
import threading
import time
from threading import Lock
from test_framework import TestMetrics, TEST_CONFIG

def run_stress_test():
    metrics = TestMetrics()
    metrics.start_test("Teste de Estresse - Ponto de Quebra")
    
    url = f"{TEST_CONFIG['base_url']}/delay/0.1"
    max_users = 20000
    step = 1000
    target_response_time = 2.0  
    target_success_rate = 90.0 
    
    print("Iniciando teste de estresse...")
    print(f"URL: {url}")
    print(f"Incremento: {step} usuários por teste")
    print(f"Máximo: {max_users} usuários")
    
    breakpoint_found = False
    breakpoint_users = 0
    
    for users in range(step, max_users + step, step):
        print(f"\n--- Testando {users} usuários simultâneos ---")
        
        threads = []
        results = {
            'success': 0,
            'failures': 0,
            'response_times': [],
            'errors': []
        }
        lock = Lock()
        
        def worker():
            try:
                start_time = time.time()
                response = requests.get(url, timeout=TEST_CONFIG['timeout'])
                response_time = time.time() - start_time
                
                with lock:
                    results['response_times'].append(response_time)
                    if response.status_code == 200 and response_time <= target_response_time:
                        results['success'] += 1
                    else:
                        results['failures'] += 1
                        if response_time > target_response_time:
                            results['errors'].append('timeout')
                        else:
                            results['errors'].append(f'http_{response.status_code}')
            except Exception as e:
                with lock:
                    results['failures'] += 1
                    results['errors'].append(str(type(e).__name__))
        
        test_start = time.time()
        
        for _ in range(users):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        test_duration = time.time() - test_start
        
        total_requests = results['success'] + results['failures']
        success_rate = (results['success'] / total_requests) * 100 if total_requests > 0 else 0
        avg_response_time = sum(results['response_times']) / len(results['response_times']) if results['response_times'] else 0
        
        print(f"  Duração: {test_duration:.2f}s")
        print(f"  Taxa de sucesso: {success_rate:.1f}%")
        print(f"  Tempo médio: {avg_response_time:.2f}s")
        print(f"  Sucessos: {results['success']}")
        print(f"  Falhas: {results['failures']}")
        
        if success_rate < target_success_rate or avg_response_time > target_response_time:
            breakpoint_found = True
            breakpoint_users = users
            
            print(f"PONTO DE QUEBRA IDENTIFICADO!")
            print(f"   - Usuários simultâneos: {users}")
            print(f"   - Taxa de sucesso: {success_rate:.1f}% (mínimo: {target_success_rate}%)")
            print(f"   - Tempo médio: {avg_response_time:.2f}s (máximo: {target_response_time}s)")
            
            if results['errors']:
                error_summary = {}
                for error in results['errors']:
                    error_summary[error] = error_summary.get(error, 0) + 1
                print(f"   - Tipos de erro:")
                for error_type, count in error_summary.items():
                    print(f"     * {error_type}: {count}")
            
            break
        else:
            print(f"Sistema suportou {users} usuários")
    
    # Add final metrics
    if breakpoint_found:
        metrics.add_metric('breakpoint_users', breakpoint_users)
        metrics.add_metric('breakpoint_found', True)
    else:
        metrics.add_metric('breakpoint_users', max_users)
        metrics.add_metric('breakpoint_found', False)
        print(f"Sistema suportou todos os {max_users} usuários testados")
    
    metrics.add_metric('max_tested_users', max_users)
    metrics.add_metric('test_increment', step)
    metrics.add_metric('target_success_rate', target_success_rate)
    metrics.add_metric('target_response_time', target_response_time)
    
    target_breakpoint = TEST_CONFIG['targets']['stress_breakpoint_users']
    final_breakpoint = breakpoint_users if breakpoint_found else max_users
    passed = metrics.evaluate_target(final_breakpoint, target_breakpoint, 'greater_than', 'stress_breakpoint_users')
    
    metrics.finish_test()
    
    print("\n" + "="*60)
    print("RESULTADOS DO TESTE DE ESTRESSE")
    print("="*60)
    print(f"Ponto de quebra: {final_breakpoint} usuários")
    print(f"Sistema quebrou: {'Sim' if breakpoint_found else 'Não'}")
    print(f"Máximo testado: {max_users} usuários")
    print(f"Incremento usado: {step} usuários")
    print(f"META > {target_breakpoint} usuários: {'APROVADO' if passed else 'REPROVADO'}")
    
    return metrics.get_results()

if __name__ == "__main__":
    run_stress_test()