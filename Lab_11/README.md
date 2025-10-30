# Plano de Teste - E-commerce Black Friday 2025

## Requisitos do Sistema

- **10.000 usuários simultâneos** esperados na Black Friday
- **Tempo de resposta < 500ms** padurante o evento
- **Proteção contra ataques** e vazamento de dados
ra 95% das requisições
- **Disponibilidade de 99.9%** 
## Tipos de Teste e Metas

| Tipo de Teste | Métrica Obrigatória | Meta Definida |
|---------------|-------------------|---------------|
| **Desempenho** | Tempo de resposta P95 | < 500ms |
| **Carga** | Throughput sustentado | > 2000 req/s |
| **Estresse** | Ponto de quebra | > 15.000 usuários |
| **Escalabilidade** | Eficiência horizontal | > 80% |
| **Segurança** | Rate limiting | 100 req/min/IP |
  
