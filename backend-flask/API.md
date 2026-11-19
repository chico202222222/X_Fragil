# Documentação da API
## Sistema de Triagem da Síndrome do X Frágil

### 1. Apresentação

Este documento apresenta os endpoints desenvolvidos para o backend do Sistema de Triagem da Síndrome do X Frágil, projeto da disciplina de Experiência Criativa da PUCPR.

A API foi desenvolvida em Python com Flask. Sua função é receber as informações enviadas pelo frontend, validar os dados, aplicar as regras do sistema e realizar operações no banco MySQL.

O frontend é desenvolvido em HTML, CSS e JavaScript por outro integrante da equipe.

O sistema tem finalidade acadêmica e utiliza uma pontuação experimental. Seus resultados não representam diagnóstico médico.

### 2. Tecnologias utilizadas

- **Python e Flask:** desenvolvimento do backend e dos endpoints HTTP.
- **Flask-SQLAlchemy:** comunicação com o banco por meio de modelos Python.
- **MySQL:** armazenamento dos usuários, pacientes, sintomas, avaliações e respostas.
- **Flask-Migrate e Alembic:** controle das alterações na estrutura do banco.
- **JSON:** comunicação entre frontend e backend.
- **bcrypt:** armazenamento seguro de senhas por meio de hash.
- **Sessões Flask:** identificação dos usuários autenticados.
- **Proteção CSRF:** validação de tokens nas requisições que modificam dados.
- **Flask-Limiter:** limitação de requisições, incluindo tentativas de login.
- **pytest:** execução dos testes automatizados.

Endereço local de desenvolvimento: `http://127.0.0.1:5000`

### 3. Endpoints disponíveis

#### 3.1. Autenticação de usuário

**Método:** POST

**Endpoint:** `/api/login`

Recebe as credenciais do usuário e verifica se o acesso é permitido.

Exemplo:

```json
{
  "email": "usuario@exemplo.com",
  "senha": "SenhaExemplo123"
}
```

Se as credenciais forem válidas, o sistema cria uma sessão autenticada.

**Outros endpoints de autenticação:**

- `POST /api/logout` — encerra a sessão.
- `GET /api/sessao` — consulta informações da sessão atual.
- `GET /api/csrf-token` — obtém um token de proteção CSRF.

O login e o logout exigem um token CSRF válido.

#### 3.2. Cadastrar usuário

**Método:** POST

**Endpoint:** `/api/usuarios`

Permite cadastrar usuários mediante autorização de administrador.

As senhas são armazenadas utilizando hash bcrypt. O sistema também oferece compatibilidade com hashes Werkzeug existentes.

#### 3.3. Consultar sintomas

**Método:** GET

**Endpoints:**

- `/api/sintomas?sexo=masculino`
- `/api/sintomas?sexo=feminino`

Retorna os sintomas aplicáveis ao checklist conforme o sexo informado.

Na configuração de sintomas utilizada durante os testes, o checklist masculino possui 12 sintomas e o feminino, 11. Esses totais dependem dos registros ativos no banco.

#### 3.4. Cadastrar paciente

**Método:** POST

**Endpoint:** `/api/pacientes`

Cadastra um paciente vinculado ao usuário autenticado.

Exemplo:

```json
{
  "nome": "Paciente Teste",
  "data_nascimento": "2015-05-20",
  "sexo": "masculino"
}
```

Quando o cadastro é realizado com sucesso, o servidor retorna HTTP 201.

#### 3.5. Listar pacientes

**Método:** GET

**Endpoint:** `/api/pacientes`

Permite consultar os pacientes associados ao usuário autenticado.

#### 3.6. Consultar paciente por ID

**Método:** GET

**Endpoint:** `/api/pacientes/1`

Consulta os dados de um paciente específico, respeitando as regras de acesso.

Quando o paciente não existe ou não está acessível ao usuário, a API pode retornar HTTP 404.

#### 3.7. Atualizar paciente

**Método:** PATCH

**Endpoint:** `/api/pacientes/1`

Atualiza os campos permitidos de um paciente.

Exemplo:

```json
{
  "nome": "Paciente Teste Atualizado"
}
```

Os campos documentados são nome, data de nascimento e sexo.

#### 3.8. Excluir paciente

**Método:** DELETE

**Endpoint:** `/api/pacientes/2`

Permite excluir um paciente conforme as regras do sistema.

A exclusão de pacientes com avaliações vinculadas é bloqueada, retornando HTTP 409.

#### 3.9. Criar avaliação

**Método:** POST

**Endpoint:** `/api/avaliacoes`

Cria uma avaliação vinculada a um paciente pertencente ao usuário autenticado.

```json
{
  "paciente_id": 1
}
```

A avaliação recebe um identificador próprio para registrar as respostas.

#### 3.10. Registrar respostas

**Método:** POST

**Endpoint:** `/api/avaliacoes/1/respostas`

Recebe as respostas dos sintomas vinculados à avaliação.

Exemplo simplificado de formato:

```json
{
  "respostas": [
    {
      "sintoma_id": 1,
      "presente": true
    },
    {
      "sintoma_id": 2,
      "presente": false
    }
  ]
}
```

**Atenção:** o exemplo mostra somente o formato. O backend exige uma resposta para cada sintoma aplicável ao paciente.

O endpoint verifica:

- Ausência de autenticação.
- JSON inválido.
- Checklist incompleto.
- Sintomas inválidos.
- Identificadores duplicados.
- Valores de presença diferentes de verdadeiro ou falso.
- Avaliações que já possuem respostas.

Uma avaliação já respondida retorna HTTP 409.

Quando todas as validações são atendidas, o sistema salva as respostas e calcula uma pontuação ponderada experimental, que é armazenada na avaliação.

Essa pontuação não possui finalidade diagnóstica.

#### 3.11. Consultar respostas

**Método:** GET

**Endpoint:** `/api/avaliacoes/1/respostas`

Retorna as respostas registradas, incluindo identificador do sintoma, descrição e indicação de presença ou ausência.

O acesso é restrito às avaliações dos pacientes associados ao usuário autenticado.

#### 3.12. Consultar resumo

**Método:** GET

**Endpoint:** `/api/avaliacoes/1/resumo`

Retorna o resumo descritivo da avaliação, com a quantidade de sintomas respondidos, presentes e ausentes.

Uma avaliação sem respostas retorna HTTP 409.

O resumo serve para apresentar os resultados registrados, não constituindo um diagnóstico clínico.

#### 3.13. Consultar histórico de avaliações

**Método:** GET

**Endpoint:** `/api/pacientes/1/avaliacoes`

Retorna as avaliações cadastradas para determinado paciente, respeitando as permissões do usuário.

O histórico permite identificar avaliações pendentes e concluídas.

### 4. Códigos de resposta HTTP

| Código | Significado |
|---|---|
| 200 | Requisição realizada com sucesso |
| 201 | Registro criado com sucesso |
| 400 | Dados incorretos ou inválidos |
| 401 | Usuário não autenticado |
| 403 | Acesso negado ou token CSRF inválido |
| 404 | Registro não encontrado ou indisponível ao usuário |
| 409 | Conflito com uma regra da operação |
| 429 | Limite de requisições excedido |
| 500 | Erro interno durante o processamento |

Esses códigos ajudam o frontend a apresentar mensagens adequadas para o usuário.

### 5. Integração com o frontend

A interface utiliza HTML, CSS e JavaScript para enviar requisições à API Flask.

Nas operações que enviam JSON, deve ser utilizado o cabeçalho:

`Content-Type: application/json`

Para operações protegidas, o frontend também deve enviar o token CSRF no cabeçalho:

`X-CSRF-Token: <token>`

O navegador deve manter o cookie de sessão nas chamadas autenticadas.

O fluxo previsto é:

1. Solicitar um token CSRF.
2. Efetuar login.
3. Solicitar um novo token CSRF após a autenticação.
4. Cadastrar ou selecionar um paciente.
5. Consultar os sintomas correspondentes ao checklist.
6. Criar uma avaliação.
7. Registrar as respostas.
8. Consultar o resumo e o histórico.

A integração completa com as telas permanece como etapa de validação.

### 6. Segurança e proteção dos dados

O backend possui mecanismos de segurança implementados para reduzir riscos de acesso indevido e requisições inválidas.

Entre eles:

- Autenticação de usuários.
- Sessões de acesso.
- Diferenciação entre administrador e profissional.
- Verificação de propriedade dos pacientes.
- Hash de senhas.
- Proteção CSRF.
- Limitação de tentativas de login.
- Validação dos dados enviados.
- Configuração de credenciais por variáveis de ambiente.

Como o sistema trata informações relacionadas à saúde, essas medidas não dispensam uma revisão de segurança e privacidade.

A utilização de dados reais exige uma análise adicional de conformidade com a LGPD, medidas de proteção adequadas e avaliação dos requisitos aplicáveis.

### 7. Testes realizados

O projeto utiliza pytest para automatizar verificações do backend.

Entre os cenários testados estão:

- Acesso sem autenticação.
- Restrições de acesso entre usuários.
- Permissões de administrador.
- Verificação de senhas.
- Validação de dados de avaliações.
- Validação e consulta das respostas.
- Cálculos de pontuação.
- Tratamento de avaliações incompletas ou já respondidas.
- Rejeição de login sem token CSRF.

A última execução completa registrada apresentou 38 testes aprovados. Um teste adicional de proteção CSRF foi aprovado individualmente, totalizando 39 cenários aprovados até o momento.

### 8. Funcionalidades pendentes

- Concluir a integração com o frontend.
- Validar o fluxo completo de autenticação, cadastro, avaliação e resumo.
- Confirmar o funcionamento de cookies e tokens CSRF no navegador.
- Verificar o comportamento das gravações e operações de rollback em testes isolados.
- Revisar a documentação e preparar a demonstração final.
- Submeter qualquer uso clínico da pontuação a validação especializada.

### 9. Considerações finais

O backend do Sistema de Triagem da Síndrome do X Frágil já possui recursos de autenticação, controle de permissões, gerenciamento de pacientes, avaliações, respostas, cálculo de pontuação experimental e consulta de históricos.

A aplicação foi organizada em módulos para facilitar seu desenvolvimento e manutenção.

Os testes automatizados apresentam resultados positivos, mas ainda será necessária a verificação completa da integração entre frontend, backend e banco de dados.

O projeto tem finalidade acadêmica e seus resultados não devem ser interpretados como diagnóstico médico.