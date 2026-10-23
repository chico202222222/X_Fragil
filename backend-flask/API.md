Documentação da API
Sistema de Triagem da Síndrome do X Frágil
1. Apresentação
Este documento reúne os endpoints desenvolvidos para o backend do Sistema de Triagem da Síndrome do X Frágil, projeto da disciplina de Experiência Criativa.

A API foi construída em Python com Flask. Ela recebe as informações enviadas pelas telas do sistema, valida os dados e realiza consultas ou alterações no banco MySQL.

O documento também serve de referência para a integração com o frontend, desenvolvido em HTML, CSS e JavaScript por outro integrante da equipe.
2. Tecnologias utilizadas
- Python e Flask: desenvolvimento do backend e das rotas HTTP.
- Flask-SQLAlchemy: acesso ao banco de dados por meio de modelos Python.
- MySQL: armazenamento de pacientes, avaliações, sintomas e respostas.
- Flask-Migrate: gerenciamento de alterações na estrutura do banco.
- JSON: formato utilizado na comunicação entre frontend e backend.
Endereço de desenvolvimento: http://127.0.0.1:5000
3. Endpoints disponíveis
3.1. Consultar sintomas
Método: GET
Endpoints:
- /api/sintomas?sexo=masculino
- /api/sintomas?sexo=feminino
Retorna os sintomas utilizados no checklist, conforme o sexo informado na requisição. Atualmente, o checklist masculino tem 12 sintomas, e o feminino, 11.
3.2. Cadastrar paciente
Método: POST
Endpoint: /api/pacientes

Cadastra um paciente no sistema.

Exemplo de corpo da requisição:
{
  "nome": "Paciente Teste",
  "data_nascimento": "2015-05-20",
  "sexo": "masculino"
}
Quando o cadastro é realizado, a API retorna HTTP 201 e os dados do paciente, incluindo seu ID.
3.3. Listar pacientes
Método: GET
Endpoint: /api/pacientes

Retorna a lista de pacientes cadastrados no banco.
3.4. Consultar paciente por ID
Método: GET
Endpoint: /api/pacientes/1

Consulta os dados de um paciente específico. Se o ID não existir, retorna HTTP 404.
3.5. Atualizar paciente
Método: PATCH
Endpoint: /api/pacientes/1

Atualiza apenas os campos informados, sem exigir o envio de todos os dados do paciente.

Exemplo:
{
  "nome": "Paciente Teste Atualizado"
}
Os campos permitidos são nome, data_nascimento e sexo. A atualização bem-sucedida retorna HTTP 200.
3.6. Excluir paciente
Método: DELETE
Endpoint: /api/pacientes/2

Exclui um paciente sem avaliações vinculadas. Caso haja avaliações relacionadas, a operação é bloqueada e retorna HTTP 409. A exclusão foi testada com um cadastro fictício criado especificamente para essa finalidade.
3.7. Criar avaliação
Método: POST
Endpoint: /api/avaliacoes

Cria uma avaliação vinculada a um paciente existente.
{
  "paciente_id": 1
}
Após o cadastro, a avaliação recebe um ID próprio, usado para registrar as respostas do checklist.
3.8. Registrar respostas de uma avaliação
Método: POST
Endpoint: /api/avaliacoes/1/respostas

Recebe as respostas para os sintomas de determinada avaliação.

Exemplo simplificado:
{
  "respostas": [
    {"sintoma_id": 1, "presente": true},
    {"sintoma_id": 2, "presente": false}
  ]
}
O campo presente indica se o sintoma foi marcado como presente (true) ou ausente (false). O exemplo contém apenas duas respostas para mostrar o formato: na requisição real de teste, é necessário enviar todos os sintomas aplicáveis ao checklist do paciente.

A API verifica IDs inválidos, respostas duplicadas e tentativas de preencher uma avaliação que já possui respostas. Nesse último caso, retorna HTTP 409.
3.9. Consultar respostas de uma avaliação
Método: GET
Endpoint: /api/avaliacoes/1/respostas

Recupera as respostas salvas, incluindo o ID e a descrição de cada sintoma e a indicação de presença ou ausência. Essas informações poderão ser utilizadas pelo frontend para apresentar um checklist já preenchido.
3.10. Consultar resumo da avaliação
Método: GET
Endpoint: /api/avaliacoes/1/resumo

Retorna um resumo descritivo com:
- Total de sintomas respondidos.
- Quantidade de sintomas marcados como presentes.
- Quantidade de sintomas marcados como ausentes.
Nos testes com dados fictícios, uma avaliação apresentou 12 sintomas respondidos: 5 presentes e 7 ausentes.

Atenção: esse resumo não representa diagnóstico nem classificação clínica de risco. Os critérios de pontuação clínica ainda precisam ser definidos e validados.
4. Códigos de resposta HTTP
Código	Significado
200	Requisição realizada com sucesso
201	Registro criado com sucesso
400	Dados enviados incorretamente
404	Registro não encontrado
409	Conflito com uma regra da operação
500	Erro interno durante o processamento


Esses códigos ajudam o frontend a identificar resultados e apresentar mensagens adequadas ao usuário.
5. Integração com o frontend
O frontend será desenvolvido em HTML, CSS e JavaScript e se comunicará com o Flask por meio de requisições HTTP. Nas requisições com corpo JSON, deve ser utilizado o cabeçalho:

Content-Type: application/json

O fluxo previsto para uma avaliação é:
1. Cadastrar ou selecionar um paciente.
2. Consultar os sintomas correspondentes ao checklist.
3. Criar uma avaliação vinculada ao paciente.
4. Enviar as respostas selecionadas.
5. Consultar as respostas e o resumo da avaliação.
As telas ficarão responsáveis pela interação com o usuário; o backend, pelas validações, pelo processamento e pelo acesso ao banco. A integração completa entre frontend e backend ainda está pendente.
6. Segurança e cuidados com os dados
Como o sistema lida com informações relacionadas à saúde, a proteção dos dados dos pacientes exige atenção especial.

Já existem validações de entrada e verificações em operações no banco, como o bloqueio da exclusão de pacientes com avaliações cadastradas. Entretanto, a API ainda não possui autenticação e autorização de usuários.

Por isso, os testes devem continuar restritos ao ambiente local e a dados fictícios. Antes de utilizar dados reais ou disponibilizar a aplicação, será necessário implementar controle de acesso e revisar o tratamento das informações pessoais, considerando as exigências aplicáveis da LGPD.
7. Funcionalidades pendentes
- Implementar cadastro de usuários e autenticação.
- Definir permissões de acesso aos dados dos pacientes.
- Validar as regras clínicas de pontuação e classificação.
- Integrar o backend às telas desenvolvidas pela equipe.
- Realizar testes automatizados e de segurança.
- Revisar o fluxo completo do sistema antes da entrega.
8. Considerações finais
A estrutura atual do backend permite cadastrar, consultar, atualizar e excluir pacientes, além de criar avaliações, registrar respostas e consultar seus resumos.

Essas operações foram testadas localmente com Flask, SQLAlchemy e MySQL. As próximas atividades serão voltadas à integração com o frontend, à implementação de mecanismos de segurança e às funcionalidades necessárias para a conclusão do projeto.