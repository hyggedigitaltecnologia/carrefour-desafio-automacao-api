# Automacao de Testes de API - ServeRest

Projeto de automacao de testes para a API [ServeRest](https://serverest.dev), uma API REST gratuita que simula operacoes de e-commerce. O projeto cobre endpoints de **usuarios**, **login**, **produtos** e **carrinhos** com validacoes funcionais, de contrato e seguranca.

## Stack Tecnologica

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem principal |
| Pytest | Framework de testes com fixtures e markers |
| Requests | Cliente HTTP para chamadas a API |
| Pydantic | Validacao de contrato (schema) das respostas |
| Faker | Geracao de dados dinamicos para testes |
| pytest-html | Relatorios HTML dos resultados |
| Allure | Relatorios detalhados com historico |
| GitHub Actions | Pipeline de CI/CD |

## Arquitetura do Projeto

```
├── src/
│   ├── config.py                  # Configuracoes (URL base, timeout)
│   ├── helpers/
│   │   └── data_generator.py      # Geracao de dados aleatorios com Faker
│   ├── models/                    # Modelos Pydantic para validacao de contrato
│   │   ├── carrinho_model.py
│   │   ├── login_model.py
│   │   ├── produto_model.py
│   │   └── usuario_model.py
│   └── services/                  # Camada de servicos (chamadas HTTP)
│       ├── base_service.py
│       ├── carrinho_service.py
│       ├── login_service.py
│       ├── produto_service.py
│       └── usuario_service.py
├── tests/
│   ├── carrinhos/
│   │   └── test_carrinhos.py      # Testes de criacao, conclusao e cancelamento
│   ├── e2e/
│   │   └── test_fluxo_completo.py # Fluxos end-to-end de negocio
│   ├── login/
│   │   └── test_login.py          # Autenticacao, validacao e seguranca
│   ├── produtos/
│   │   └── test_produtos.py       # CRUD completo de produtos
│   └── usuarios/
│       ├── test_buscar_usuario.py  # GET /usuarios/{id}
│       ├── test_cadastrar_usuario.py # POST /usuarios
│       ├── test_editar_usuario.py  # PUT /usuarios/{id}
│       ├── test_excluir_usuario.py # DELETE /usuarios/{id}
│       └── test_listar_usuarios.py # GET /usuarios
├── conftest.py                    # Fixtures globais (services, auth, dados)
├── pytest.ini                     # Configuracao do Pytest e markers
├── requirements.txt               # Dependencias do projeto
└── .github/workflows/api-tests.yml # Pipeline CI
```

## Pre-requisitos

- Python 3.10+
- pip (gerenciador de pacotes)
- Git

## Instalacao e Configuracao

```bash
# Clonar o repositorio
git clone <url-do-repositorio>
cd carrefour-desafio-automacao-api

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Executando os Testes

```bash
# Executar todos os testes
pytest

# Executar somente testes de smoke (sanidade rapida)
pytest -m smoke

# Executar testes de contrato
pytest -m contract

# Executar testes de regressao
pytest -m regression

# Executar testes de seguranca
pytest -m security

# Executar testes end-to-end
pytest -m e2e

# Executar testes de um modulo especifico
pytest tests/login/
pytest tests/usuarios/
pytest tests/produtos/
pytest tests/carrinhos/

# Gerar relatorio HTML
pytest --html=reports/report.html --self-contained-html

# Gerar resultados para Allure
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Configuracao de Ambiente

Por padrao a API utiliza `https://serverest.dev`. Para apontar para outra instancia:

```bash
# Via variavel de ambiente
export BASE_URL=http://localhost:3000

# Ou editando o arquivo .env
BASE_URL=http://localhost:3000
```

## Estrategia de Testes

### Niveis de Teste (Piramide)

| Nivel | Marker | Descricao |
|---|---|---|
| Smoke | `smoke` | Validacoes rapidas dos fluxos criticos |
| Contrato | `contract` | Validacao da estrutura das respostas via Pydantic |
| Regressao | `regression` | Cobertura completa incluindo cenarios negativos |
| Seguranca | `security` | Validacao contra injecao SQL, XSS e entradas maliciosas |
| End-to-End | `e2e` | Fluxos de negocio completos simulando uso real |

### Tecnicas de Teste Aplicadas

| Tecnica | Aplicacao |
|---|---|
| Analise de valor limite | Formatos de email, campos obrigatorios |
| Particao de equivalencia | Usuarios admin vs nao-admin |
| Testes parametrizados | Emails invalidos com `@pytest.mark.parametrize` |
| Validacao de contrato | Modelos Pydantic com `extra="forbid"` |
| Isolamento de dados | Fixtures com setup/teardown automatico |
| Dados dinamicos | Faker com locale pt_BR para dados realistas |

## Matriz de Cobertura

| Endpoint | Smoke | Contrato | Regressao | Seguranca | E2E |
|---|---|---|---|---|---|
| POST /login | X | X | X | X | X |
| GET /usuarios | X | X | X | | |
| GET /usuarios/{id} | X | X | X | | X |
| POST /usuarios | X | X | X | | X |
| PUT /usuarios/{id} | X | | X | | X |
| DELETE /usuarios/{id} | X | | X | | X |
| GET /produtos | X | X | X | | |
| GET /produtos/{id} | | X | X | | X |
| POST /produtos | X | X | X | | X |
| PUT /produtos/{id} | | | X | | X |
| DELETE /produtos/{id} | | | X | | X |
| GET /carrinhos | X | X | | | |
| POST /carrinhos | X | X | X | | X |
| DELETE /carrinhos/concluir | | | X | | X |
| DELETE /carrinhos/cancelar | | | X | | X |

## Pipeline CI/CD

O projeto utiliza **GitHub Actions** com duas etapas:

1. **Smoke Tests** - Execucao rapida dos cenarios criticos (gate de qualidade)
2. **Regression Tests** - Suite completa executada apos sucesso dos smoke tests

Os relatorios HTML e resultados Allure sao disponibilizados como artefatos na pipeline.

## Decisoes Tecnicas

| Decisao | Justificativa |
|---|---|
| Python + Pytest | Sintaxe limpa, fixtures poderosas, ecossistema rico de plugins |
| Requests | Biblioteca HTTP madura e amplamente utilizada |
| Pydantic para contratos | Validacao tipada em tempo de execucao, mais expressiva que JSON Schema |
| Fixtures com teardown | Garantia de limpeza de dados independente do resultado do teste |
| Service Layer pattern | Encapsulamento das chamadas HTTP, facilita manutencao |
| Faker com locale pt_BR | Dados realistas e unicos a cada execucao |
| Markers do Pytest | Organizacao flexivel por nivel de teste |
