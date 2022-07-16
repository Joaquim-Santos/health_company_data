# health_company_data

Este projeto consiste em uma API REST privada para fornecimento de informações cadastrais e financeiras de uma empresa de saúde. O Objetivo é permitir requisições que seriam feiats pelo setor financeiro da empresa, para acesso à informações de pacientes/clientes e farmácias da mesma, bem como de transações realizadas entre esses. Para tanto, o projeto foi implementado utilizando um servidor Flask, o qual disponibiliza os endpoints que são responsáveis por fornecer esses dados, ao passo em que realiza a autenticação do usuário.

# Dependências

## Instalações

Atualmente, o projeto utiliza o Python em versão 3.9.  Para executá-lo, deve-se instalar as *libs* listadas em **requirements.txt.**, recomendando-se realizar o uso de ambiente virtual.

### Ambiente pela linha de comando

Inicie o virtual env dentro da pasta app

```bash
python -m venv .venv

```

Ative seu virtualenv

```bash
.venv\\Scripts\\activate

```

Instale os requirements

```bash
pip install -r requirements.txt

```

### Ambiente pela IDE PyCharm

- Menu **FIle > Settings > project: <nome_projeto> > Python interpreter**
- Ao lado do menu de seleção do interpretador, clique na roleta de configurações e em **add**.
- Marque a opção **New enviroment**, então define o **Base interpreter** (e.g. Python 3.9).
- Basta confirmar e será criado um diretório **venv** na raíz do projeto.

Para instalar as dependências:

- Pressione Ctrl+Alt+S para abrir as configurações e selecione **Tools > Python Integrated Tools**.
- No campo **Package requirements file,** selecione o arquivo ****requirements.txt
- Ao confirmar, aparecerá uma mensagem na IDE para instalar as dependências no arquivo, basta selecionar **Install requirements**

## Variáveis de Ambiente

No momento, as variáveis de ambiente necessárias para execução do projeto são:

1. **STAGE** - Definição do ambiente de execução entre Local, Teste, Desenvolvimento ou Produção, respectivamente associados aos valores: Local, Test, Development, Production.
2. **LOGS_FOLDER** - Caminho para o diretório onde serão gerados os arquivos de Log.
3. **HOST, PORT** - Endereço do Host e sua porta para executar a aplicação (Padrão localhost:5000).
4. **ACCESS_TOKEN** - Valor a ser definido para uso na autenticação.

# Banco de Dados

Por questões de simplificação, o banco de dados foi definido como um SQLite. Desse modo, basta criar um arquivo **company_data.db**, no diretório raíz, o qual é referenciado na **SQLALCHEMY_DATABASE_URI**, na classe de configuração. Nesse banco, deverão ser cadastradas todas as informações necessárias para consumo da API.

Para comunicação com o banco e realização de CRUD via ORM, foram definidas classes que mapeiam as tabelas do banco, segundo o padrão da lib **Flask-SQLAlchemy**, as quais estão definidas no pacote **models**. Assim sendo, pode-se executar o script **manager.py** para realizar a migração e adicionar os modelos do projeto como tabelas no banco. Para tanto, esse script deve ser executado com os parâmetros, em ordem:

1. db init
2. db migrate
3. db upgrade

Isso gerará a estrutura do banco para o SQLite definido na configuração. Então, basta inserir alguns dados para consmo da API. Devido à simplicidade, basta adicionar os dados via query, em alguma IDE de banco, como **DBeaver**.

# Execução

Feitas todas as configurações, basta executar o script **application.py** para iniciar o servidor. Por padrão, o Flask o executará em **localhost:5000**, podendo ser utilizados o host e porta definidos nas variáveis de ambiente.  

A aplicação também pode ser iniciada em container, utilizando o Dockerfile do projeto. Para tanto, tendo-se o docker instalado. deve-se definir as mesmas variáveis de ambiente citadas anteriormente. Isso pode ser feito as informando em um arquivo, como um **env.list**, e então executar o comando no diretório do Dockerfile:

**docker run --env-file env.list**

Este arquivo deve usar a sintaxe **variable=value**, que define a variável para o valor fornecido.

## Swagger

Para melhor entendimento e uso da aplicação, foi construída uma documentação Swagger, com base em arquivos YALM, contidos no diretório **health_company_data_api/swagger**. Esses arquivos são utilizados com o python decorator **swag_from** da lib **flasgger**, o qual é aplicado sobre cada método que se refere a um ednpoint, a fim de construir a documentação do mesmo e disponibilizar seu uso ao acessar a página do Swagger da API. 

Para acessar a documentação Swagger, localmente: http://localhost:5000/apidocs/

Serão listados os endpoints da API, cada um com uma descrição de seu objetivo e campos para entrada de parâmetros, como dados de autenticação e filtros, de modo que é possível fazer uma chamada ao endpoint por essa página, a fim de se ter uma interface mais amigável e interativa.


## Autenticação

Visando maior segurança, a API possui uma camada de autenticação para acesso a qualquer endpoint. Para tanto, é necessário informar, no cabeçalho de cada requisição, um token de acesso, bem como usuário e senha. Então, antes de seguir para o endpoint, será chamado o método de autenticação implementado, o qual irá verificar, primeiro, se o token de acesso condiz com aquele definido na variável de ambiente (Para uso local, pode ser qualquer valor). Isso foi feito para simular o uso de uma API Key, como no caso de ambiente AWS com API Gateway. 

Caso haja equivalência, então será feita a etapa de verificação do usuário, que primeiro confirma se o usuário existe na base de dados, e caso negativo, informa que o usuário não foi encontrado. Somente se o encontrar, é que é feita a validação da senha. Caso essa passe, então é liberado o acesso ao endpoint. Vale destacar que os dados de usuário e senha devem ser enviados codificados em Base 64 (como feito na lib **base64**), como uma camada a mais de segurança. Portanto, são 3 etapas de validação:

1. Validação do token (API Key).
2. Verificação da existência do usuário.
3. Validação da senha.

Assim sendo, para acesso a qualquer endpoint, deve ser feito o cadastro do usuário na rota **/api/signup**. Para isso, o token de acesso também deve ser enviado nessa rota, assiim somente usuários que possuem essa chave de acesso à API podem se cadastrar, como seria feito em um ambiente de produção. Foi adicionada uma Constraint à tabela de usuários, para que não possam ser cadastrados usuários com o mesmo nome. Além disso, é feita uma verificação no nome de usuário antes do cadastro, de modo que esse deve seguir um padrão para ser aceito (e.g. sem caracteres especiais), e que seja sempre armazenado como **lower case**. De modo semelhante, a senha também é verificada quanto à sua força, devendo atender aos padrões (e.g conter números e caracteres especiais).

A senha é salva no banco em formato criptografado, sendo o hash gerado pelo algoritmo da lib **flask_bcrypt**, de modo que não é possível decodificá-la posteriormente, garantindo maior segurança. Assim sendo, para fazer a validação de senha no login, é feita a checagem da senha do banco com a senha enviada, utilizando um método da própria lib, que irá comparar o hash de cada senha.

Ao usar o Swagger, esses dados de autorização são automaticamente adicionados na requisição para cada rota, bastando informá-los na opção Authorize, a qual também já irá codificá-los para o envio. Essa configuração foi feita nas definições de segurança do Swagger, em seu **template.yml**.


## Rotas

Para todas as rotas foi definido um **blueprint** /api, sendo que as rotas disponíveis são:

 - **/api/patients**: Retorna a lista de pacientes cadastrados na base de dados, podendo ser filtrados por nome, sobrenome 
 e idade. Caso nenhum filtro seja passado, retorna todos os pacientes cadastrados. Para cada paciente, é retornado seu ID, nome, sobrenome e data de nascimento. Os filtros de nome e sobrenome são **case insensitive**, já o filtro de idade, pode ter um valor inicial e final, ou apenas um deles, sendo que internamente filtra as datas correspondentes ao intervalo de idade.
 - **/api/pharmacies**: Retorna a lista de farmácias cadastradas na base de dados, podendo ser filtradas por nome e cidade. Caso nenhum filtro seja passado, retorna todas as farmácias cadastradas. Para cada farmácia, é retornado seu ID, nome e cidade. Os filtros de nome e cidade são **case insensitive**.
 - **/api/transactions**: Retorna a lista de transações cadastradas na base de dados, podendo ser filtradas por valor e data. 
 Caso nenhum filtro seja passado, retorna todas as transações cadastradas. Para cada transação, é retornado seu ID, quantidade e data, bem como todos os valores de pacientes e farmácias que se relacionam com a mesma. O filtro de quantidade considera valores iguais ou maiores que o valor informado, assim como o filtro de data.
 - **/api/signup**: Registra o usuário na base de dados, após validar seu token de acesso. Deve receber o nome de usuário e senha,
 os quais serão codificados e enviados no cabeçalho, e o token deve corresponder ao valor da variável de ambiente.
 - **/api/health**: Exibe a data atual, mostrando que o sistema está funcionando.
 - **/api/logs**: Retorna a lista de arquivos de logs da aplicação, correspondentes a cada dia.
 - **/api/logs/<filename>**: Retorna um arquivo de logs da aplicação, correspondente a um dia.

## Logs

Foi implementado um módulo para geração de **Logs** da aplicaçã.o de modo que são gerados arquivos de Log correspondentes ao dia em que a aplicação é acessada. O módulo de Log é configurado para que, a cada dia, seja usado um arquivo diferente para o registro, mantendo melhor rastreabilidade. Isso foi feito pensando em como seria útil para um ambiente de produção e desenvolvimento.  

Portanto, ao acessar uma endpoint, são gravados os erros que podem ocorrer, assim como dados recebidos da requisição e enviados na resposta.

## Testes

Foram implementados testes unitários para os principais métodos, contidos no diretório de **tests**, os quais foram separados por móodulos e arquivos, buscando ter a cobertura da maior parte do código. Deve-se definir as variáveis de ambiente antes da execução:

1. STAGE: Test
2. LOGS_FOLDER: Caminho para o diretório raíz do projeto.
3. Pra conexão de banco, é definida na classe de teste, uma conexão com uma base SQLite diferente, gerada exclusivamente para os testes.
4. ACCESS_TOKEN: token_test (pode ser qualquer valor, basta corresponder ao que estiver nos casos de teste).

A estrutura dos testes é equivalente à das funcionalidades, visando:

- Implementar um módulo de teste para cada módulo desenvolvido, seguindo a mesma estrutura e hierarquia de pacotes.
- Implementar uma classe de teste correspondente a cada classe criada na aplicação.
- Implementar um ou mais métodos de teste para cada método implementado, visando cobrir todos os caminhos.

Para construção dos testes, seguir o padrão:

- Nomear os módulos, classes e métodos de testes como:
    - test_<nome_do_metodo>
    - Test<NomeDaClasse>
    - test_<nome_do_modulo>
    
A definição dos testes e sua execução são feitos com base na *lib* do **pytest**. Por assim ser, foi criado o módulo de **conftest.py**, o qual contém as configurações inicias para antes de executar os testes, tais como criação de banco de testes, e *fixtures* da própria *lib*, para população e remoção de dados de teste.

Para execução de todos os testes, basta executar o comando do *pytest* apontando para o diretório tests. Automaticamente, a *lib* reconhece todos os testes pelo padrão de nomeclatura, sendo possível executar testes apenas em diretórios específicos.

## Organização

A arquitetura da aplicação seguiu uma divisão em camadas, segundo padrão do Flask:

1. **resources**: Classes representando os Endpoints e seus métodos.
2. **services**: Fornece os serviços que solicitam acesso à banco e realizam processamentos para retorno do resultado.
3. **repositories**: Define as operações sobre a base de dados.
4. **configurations**: Define a configuração da aplicação, como rotas e ambiente.
5. **models**: Mapeamento das tabelas do banco, usadas para migração e operações com SQLAlchemy.
6. **common**: Classes Abstratas, classes para exceções e outros métodos reutilizáveis.
7. **swagger**: Documentação da aplicação,, interativa pela interface Swagger.
8. **schemas**: Classes para validação de dados de entrada, com base na lib marshmallow.

* Foram criados handlers personalizados para tratar as exceções conhecidas da API, assim como construídas classes de exceções personalizadas.
* Os dados enviados na requisição à um endpoint são validados, a fim de identificar e informar problemas em parâmetros recebidos (e.g. campos de data em formato inválido, campo com valor de string ao invés de numérico, etc.)
