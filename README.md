# Desafio Técnico – Intuitive Care

Este repositório contém a solução **Full Stack** desenvolvida para o desafio técnico da Intuitive Care, abrangendo:

* Pipeline de Dados (ETL)
* Modelagem de Banco de Dados
* API RESTful
* Interface Web

---

## Arquitetura da Solução

O projeto foi estruturado seguindo princípios de **Separação de Responsabilidades (SoC)**, visando manutenibilidade, clareza e escalabilidade:

* **ETL (Python / Pandas)**
  Extração, normalização, limpeza e enriquecimento dos dados da ANS.

* **Database (SQL)**
  Modelagem relacional normalizada para garantir integridade dos dados e boa performance em consultas analíticas.

* **Backend (FastAPI)**
  API RESTful de alta performance, com tipagem estática e documentação automática (Swagger).

* **Frontend (Vue.js via CDN)**
  Interface reativa para visualização de dados e métricas, sem necessidade de build ou dependências locais.

---

## Como Executar o Projeto

### Pré-requisitos

* Python 3.8 ou superior
* Git

---

### Passo 1: Configuração e ETL

1. Clone este repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute o pipeline de dados para gerar os arquivos processados na pasta `data/`:

```bash
python src/etl_pipeline.py
```

**Nota:**
Este script simula o download dos dados da ANS, realiza limpeza, normalização, validação de CNPJs e gera os arquivos `.csv` consolidados e agregados necessários para consumo da API.

---

### Passo 2: API Backend

Inicie o servidor da aplicação:

```bash
uvicorn src.api:app --reload
```

* API disponível em:
  [http://127.0.0.1:8000](http://127.0.0.1:8000)

* Documentação interativa (Swagger):
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Passo 3: Frontend

1. Acesse a pasta `frontend`
2. Abra o arquivo `index.html` em qualquer navegador moderno (Chrome, Edge ou Firefox)

> Optei por uma abordagem via **CDN**, seguindo o princípio **KISS (Keep It Simple, Stupid)**, eliminando a necessidade de `npm install` ou processos de build para facilitar a avaliação.

---

## Decisões Arquiteturais e Trade-offs

Conforme solicitado no desafio, seguem as justificativas técnicas para as principais escolhas adotadas:

---

### 1. Processamento de Dados (ETL)

**Decisão:** Processamento em memória com Pandas

**Trade-off (Memória vs. Incremental):**
Embora o processamento incremental (chunksize) seja mais adequado para cenários de Big Data (>10 GB), o volume amostral do desafio permitiu processamento em memória, priorizando simplicidade e velocidade de desenvolvimento.

**Resiliência:**
O pipeline foi estruturado de forma modular, permitindo fácil refatoração para processamento em streaming caso o volume de dados exceda a RAM disponível.

---

### 2. Qualidade de Dados (Validação de CNPJ)

**Decisão:** Flagging (marcar) registros inválidos em vez de excluí-los

**Justificativa:**
Em sistemas financeiros e de saúde, a integridade histórica é fundamental. A exclusão de registros com CNPJ inválido poderia distorcer os totais financeiros.
A estratégia adotada foi manter o registro, marcando-o como inválido para fins de auditoria e análise posterior.

---

### 3. Banco de Dados

**Decisão:** Modelo Relacional Normalizado (Opção B)

**Justificativa:**
Entre uma tabela única desnormalizada e a separação em tabelas relacionais, optei pela normalização, separando:

* **Operadoras** (Dimensão)
* **Despesas** (Fato)

**Vantagens:**

* Evita redundância de dados textuais (razão social, UF)
* Reduz armazenamento
* Facilita manutenção cadastral

**Tipagem:**
Valores monetários foram definidos como `DECIMAL(15,2)`, evitando erros de precisão associados ao uso de `FLOAT` em cálculos financeiros.

---

### 4. Backend API

**Decisão:** FastAPI (Opção B)

**Justificativa:**
Escolhido em detrimento do Flask por oferecer:

* Suporte nativo a `async/await`
* Melhor performance para operações de I/O
* Validação automática de dados com Pydantic
* Documentação Swagger gerada automaticamente

---

### 5. Paginação e Busca

**Decisão:**

* Paginação **Offset-based**
* Busca **Server-side**

**Justificativa:**

* **Busca no servidor:** evita o envio do dataset completo ao cliente, melhorando a experiência do usuário (especialmente em redes móveis)
* **Paginação Offset:** mais intuitiva para interfaces administrativas e suficiente para o volume de dados atual, em comparação ao modelo por cursor
