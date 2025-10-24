# Exercício 1: Testes de Login com Selenium

## **Site de Teste**
**URL**: [https://practicetestautomation.com/practice-test-login/](https://practicetestautomation.com/practice-test-login/)

### **Credenciais Válidas**
- **Username**: `student`
- **Password**: `Password123`

---

## **Testes Implementados**

### ** Resumo**
- **Total**: 15 casos de teste
- **Cenários válidos**: 3 testes
- **Cenários inválidos**: 8 testes
- **Testes de validação**: 4 testes

### ** Casos de Teste Válidos**
1. `test_login_sucesso` - Login com credenciais corretas
2. `test_logout_apos_login` - Logout após login bem-sucedido
3. `test_multiplos_logins` - Múltiplos logins consecutivos

### ** Casos de Teste Inválidos**
1. `test_login_username_invalido` - Username incorreto
2. `test_login_senha_incorreta` - Password incorreta
3. `test_login_campos_vazios` - Campos vazios
4. `test_login_apenas_username` - Só username preenchido
5. `test_login_apenas_password` - Só password preenchido
6. `test_login_username_vazio` - Username vazio
7. `test_login_password_vazia` - Password vazio
8. `test_login_credenciais_especiais` - Caracteres especiais

### ** Testes de Validação**
1. `test_verificar_elementos_pagina` - Elementos presentes
2. `test_titulo_pagina` - Título correto
3. `test_url_redirecionamento` - Redirecionamento pós-login
4. `test_mensagens_erro` - Validação de mensagens de erro

---