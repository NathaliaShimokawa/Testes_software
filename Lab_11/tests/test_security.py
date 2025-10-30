"""
Teste de Segurança - Rate Limiting
Meta: 100 req/min por IP
"""
import requests
import time
from test_framework import TestMetrics, TEST_CONFIG

def run_security_test():
    metrics = TestMetrics()
    metrics.start_test("Teste de Segurança - Rate Limiting")
    
    url = f"{TEST_CONFIG['base_url']}/status/429"
    test_ip = "192.168.1.100"
    target_limit = TEST_CONFIG['targets']['security_rate_limit_rpm']
    
    print("Iniciando teste de segurança - Rate Limiting...")
    print(f"URL: {url}")
    print(f"IP simulado: {test_ip}")
    print(f"Limite esperado: {target_limit} req/min")
    
    print(f"\n--- Teste 1: Taxa normal de requisições ---")
    normal_requests = 50  
    headers = {'X-Forwarded-For': test_ip}
    
    successful_normal = 0
    blocked_normal = 0
    
    start_time = time.time()
    for i in range(normal_requests):
        try:
            response = requests.get(f"{TEST_CONFIG['base_url']}/status/200", 
                                  headers=headers, 
                                  timeout=TEST_CONFIG['timeout'])
            
            if response.status_code == 200:
                successful_normal += 1
            elif response.status_code == 429:
                blocked_normal += 1
                
        except Exception as e:
            blocked_normal += 1
        
        time.sleep(0.05)
    
    normal_duration = time.time() - start_time
    normal_rate = successful_normal / (normal_duration / 60) 
    
    print(f"  Requisições bem-sucedidas: {successful_normal}")
    print(f"  Requisições bloqueadas: {blocked_normal}")
    print(f"  Taxa: {normal_rate:.1f} req/min")
    
    print(f"\n--- Teste 2: Taxa excessiva de requisições ---")
    excessive_requests = 150  
    
    successful_excessive = 0
    blocked_excessive = 0
    
    start_time = time.time()
    for i in range(excessive_requests):
        try:
            response = requests.get(f"{TEST_CONFIG['base_url']}/status/200", 
                                  headers=headers, 
                                  timeout=TEST_CONFIG['timeout'])
            
            if response.status_code == 200:
                successful_excessive += 1
            elif response.status_code == 429:
                blocked_excessive += 1
                
        except Exception as e:
            blocked_excessive += 1
        
        if i == target_limit:
            print(f"  Atingiu {target_limit} requisições...")
    
    excessive_duration = time.time() - start_time
    excessive_rate = (successful_excessive + blocked_excessive) / (excessive_duration / 60)
    
    print(f"  Requisições bem-sucedidas: {successful_excessive}")
    print(f"  Requisições bloqueadas: {blocked_excessive}")
    print(f"  Taxa total: {excessive_rate:.1f} req/min")
    
    print(f"\n--- Teste 3: IP diferente (controle) ---")
    different_ip = "192.168.1.101"
    control_headers = {'X-Forwarded-For': different_ip}
    control_requests = 30
    
    successful_control = 0
    blocked_control = 0
    
    for i in range(control_requests):
        try:
            response = requests.get(f"{TEST_CONFIG['base_url']}/status/200", 
                                  headers=control_headers, 
                                  timeout=TEST_CONFIG['timeout'])
            
            if response.status_code == 200:
                successful_control += 1
            elif response.status_code == 429:
                blocked_control += 1
                
        except Exception as e:
            blocked_control += 1
        
        time.sleep(0.05)
    
    print(f"  Requisições bem-sucedidas: {successful_control}")
    print(f"  Requisições bloqueadas: {blocked_control}")
  
    normal_success_rate = (successful_normal / normal_requests) * 100
    excessive_block_rate = (blocked_excessive / excessive_requests) * 100
    control_success_rate = (successful_control / control_requests) * 100

    rate_limiting_working = (
        normal_success_rate > 80 and  
        excessive_block_rate > 20 and  
        control_success_rate > 80 
    )
    
    metrics.add_metric('target_rate_limit_rpm', target_limit)
    metrics.add_metric('normal_requests_sent', normal_requests)
    metrics.add_metric('normal_requests_successful', successful_normal)
    metrics.add_metric('normal_success_rate_pct', normal_success_rate)
    metrics.add_metric('excessive_requests_sent', excessive_requests)
    metrics.add_metric('excessive_requests_blocked', blocked_excessive)
    metrics.add_metric('excessive_block_rate_pct', excessive_block_rate)
    metrics.add_metric('control_requests_sent', control_requests)
    metrics.add_metric('control_requests_successful', successful_control)
    metrics.add_metric('control_success_rate_pct', control_success_rate)
    metrics.add_metric('rate_limiting_detected', rate_limiting_working)
    
    passed = metrics.evaluate_target(1 if rate_limiting_working else 0, 1, 'equals', 'security_rate_limit_rpm')
    
    metrics.finish_test()
    
    print("\n" + "="*60)
    print("RESULTADOS DO TESTE DE SEGURANÇA")
    print("="*60)
    print(f"Limite configurado: {target_limit} req/min por IP")
    print(f"\nTeste de taxa normal:")
    print(f"  - Taxa de sucesso: {normal_success_rate:.1f}%")
    print(f"  - Requisições/min: {normal_rate:.1f}")
    print(f"\nTeste de taxa excessiva:")
    print(f"  - Taxa de bloqueio: {excessive_block_rate:.1f}%")
    print(f"  - Requisições/min: {excessive_rate:.1f}")
    print(f"\nTeste de controle (IP diferente):")
    print(f"  - Taxa de sucesso: {control_success_rate:.1f}%")
    
    print(f"\nRate limiting detectado: {'Sim' if rate_limiting_working else 'Não'}")
    print(f"META RATE LIMITING FUNCIONAL: {'APROVADO' if passed else 'REPROVADO'}")
    
    print(f"\nRECOMENDAÇÕES DE SEGURANÇA:")
    print(f"   • Implemente rate limiting por IP")
    print(f"   • Configure alertas para tentativas de abuso")
    print(f"   • Use CAPTCHA após múltiplas tentativas")
    print(f"   • Monitore padrões de tráfego suspeito")
    print(f"   • Implemente blacklist/whitelist dinâmica")
    
    return metrics.get_results()

if __name__ == "__main__":
    run_security_test()
