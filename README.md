# 🛡️ SentinelAI

### Sistema Inteligente de Detecção de Anomalias de Acesso

O **SentinelAI** é um sistema de segurança desenvolvido para identificar comportamentos anômalos em acessos de usuários e tomar decisões preventivas com base em uma análise de risco.

O projeto foi desenvolvido como parte de uma atividade acadêmica de **Sistemas Guiados por IA**, com foco em cibersegurança, análise comportamental, banco de dados e desenvolvimento de APIs.

> **Status:** MVP funcional  
> **Versão:** 1.0.0

---

## 🎯 Sobre o projeto

Instituições de ensino podem possuir milhares de usuários acessando simultaneamente sistemas acadêmicos.

Nesse cenário, ataques de phishing, roubo de credenciais e acessos indevidos podem passar despercebidos quando a análise depende exclusivamente de monitoramento manual.

O SentinelAI foi desenvolvido para auxiliar nesse processo através da análise automática de características dos acessos.

O sistema registra os eventos, calcula uma pontuação de risco, classifica o acesso e executa uma ação de segurança.

---

## 🚨 Problema

O cenário analisado apresenta três desafios principais:

- grande quantidade de acessos simultâneos;
- dificuldade de monitoramento manual em escala;
- necessidade de identificar rapidamente comportamentos suspeitos.

Um acesso realizado fora do horário habitual, por exemplo, utilizando um dispositivo desconhecido e originado de uma localização diferente do padrão do usuário, pode representar um risco maior.

---

## 💡 Solução

O SentinelAI utiliza características do acesso para calcular uma pontuação de risco.

O fluxo principal é:

```text
LOGIN
   ↓
Coleta de informações
   ↓
Análise comportamental
   ↓
Pontuação de risco
   ↓
Classificação
   ↓
┌──────────┬──────────┬──────────┐
│  BAIXO   │  MÉDIO   │   ALTO   │
│          │          │          │
│ PERMITIR │ ALERTAR  │ BLOQUEAR │
└──────────┴──────────┴──────────┘
   ↓
Registro para auditoria
```

---

## 🧠 Análise de risco

O MVP atual utiliza um **motor de pontuação baseado em regras**.

Os fatores considerados são:

| Fator | Pontuação |
|---|---:|
| Login fora do horário habitual | +25 |
| País diferente do padrão | +35 |
| Dispositivo não reconhecido | +20 |
| IP não reconhecido | +20 |

### Classificação

| Pontuação | Nível | Ação |
|---:|---|---|
| 0–39 | 🟢 BAIXO | PERMITIR |
| 40–69 | 🟡 MÉDIO | ALERTAR |
| 70–100 | 🔴 ALTO | BLOQUEAR |

### Exemplo

Um acesso realizado:

- às 03:15;
- a partir da Alemanha;
- utilizando dispositivo desconhecido;
- utilizando IP desconhecido;

recebe:

```text
25 + 35 + 20 + 20 = 100 pontos
```

Resultado:

```text
RISCO: ALTO
AÇÃO: BLOQUEAR
```

---

## 🤖 Relação com IA

O projeto foi concebido dentro de um cenário de **defesa preditiva e análise comportamental**.

Nesta versão acadêmica, o MVP utiliza regras determinísticas para representar o funcionamento inicial do sistema.

A arquitetura foi preparada para uma evolução futura utilizando técnicas de:

- Machine Learning;
- detecção de anomalias;
- aprendizado do comportamento individual;
- análise estatística;
- modelos de classificação;
- identificação de padrões de acesso.

Portanto, o MVP atual **não afirma utilizar Machine Learning em produção**. Ele representa a primeira etapa de um sistema que pode evoluir para modelos de IA.

---

## 🏗️ Arquitetura

O projeto utiliza uma arquitetura modular:

```text
                 ┌─────────────────────┐
                 │      Streamlit      │
                 │     Frontend        │
                 └──────────┬──────────┘
                            │
                            │ HTTP / REST
                            ▼
                 ┌─────────────────────┐
                 │       FastAPI       │
                 │       Backend       │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │  Risk      │ │ Security   │ │Repository  │
      │  Analysis  │ │   Engine   │ │   Layer    │
      └────────────┘ └────────────┘ └─────┬──────┘
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │    SQLite    │
                                  └──────────────┘
```

---

## 🗄️ Banco de dados

O SentinelAI utiliza SQLite no MVP.

Principais entidades:

```text
USUARIO
   │
   ├──────────< DISPOSITIVO
   │
   ├──────────< ACESSO
   │
   └──────────< REGRA_COMPORTAMENTAL

ACESSO
   │
   └────────── ANALISE_RISCO
                    │
                    └──────────< ACAO_SEGURANCA
```

### Entidades

#### USUARIO

Armazena os usuários do sistema.

Principais campos:

- `id_usuario`
- `nome`
- `email`
- `tipo_usuario`
- `status`
- `data_cadastro`

#### DISPOSITIVO

Armazena dispositivos associados aos usuários.

#### ACESSO

Registra os eventos de login.

#### REGRA_COMPORTAMENTAL

Representa o comportamento esperado do usuário.

#### ANALISE_RISCO

Armazena a pontuação e classificação do risco.

#### ACAO_SEGURANCA

Registra a decisão tomada pelo sistema.

---

## 🖥️ Interface

O frontend foi desenvolvido utilizando Streamlit.

### Dashboard

Apresenta:

- quantidade de acessos;
- quantidade de alertas;
- bloqueios;
- eventos de alto risco;
- distribuição dos níveis de risco;
- últimos acessos;
- status dos componentes.

### Monitoramento

Permite acompanhar eventos de segurança em tempo real através dos dados registrados pela API.

A tela apresenta:

- nível de risco;
- pontuação;
- IP;
- localização;
- data e hora;
- ação executada;
- motivos da detecção.

Também é possível filtrar os eventos por nível de risco.

### Auditoria

Apresenta o histórico dos eventos e permite consultar os registros por:

- nível de risco;
- ação executada.

---

## 🛠️ Tecnologias

### Backend

- Python
- FastAPI
- Pydantic
- SQLite

### Frontend

- Streamlit
- Pandas

### Testes

- Pytest

### Desenvolvimento

- Git
- GitHub
- REST API

---

## 📂 Estrutura do projeto

```text
sentinel-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── repositories.py
│   ├── risk_analysis.py
│   └── security.py
│
├── database/
│   └── schema.sql
│
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── cards.py
│   │   └── tables.py
│   │
│   └── views/
│       ├── __init__.py
│       ├── dashboard.py
│       ├── monitoramento.py
│       └── auditoria.py
│
├── scripts/
│   └── seed_demo.py
│
├── tests/
│   ├── test_database.py
│   └── test_risk.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🚀 Instalação

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Entrar na pasta:

```bash
cd sentinel-ai
```

---

## 2. Criar ambiente virtual

### Windows

```powershell
python -m venv venv
```

Ativar:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependências

```powershell
python -m pip install -r requirements.txt
```

---

# ▶️ Execução

## Backend

Execute:

```powershell
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa da API pode ser acessada através do Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

Em outro terminal, com o ambiente virtual ativado:

```powershell
python -m streamlit run frontend/app.py
```

A interface ficará disponível em:

```text
http://localhost:8501
```

---

# 🎭 Dados de demonstração

O projeto possui um script para gerar dados demonstrativos através da própria API.

Com o backend em execução:

```powershell
python scripts/seed_demo.py
```

O script cria cenários de diferentes níveis de risco.

### Cenário 1 — Acesso normal

```text
Usuário: João
País: Brasil
Horário: 10:30
IP conhecido: sim
Dispositivo conhecido: sim

Risco: BAIXO
Pontuação: 0
Ação: PERMITIR
```

### Cenário 2 — Acesso suspeito

```text
Usuário: Maria
País: Brasil
Horário: 23:45
IP conhecido: não
Dispositivo conhecido: sim

Risco: MÉDIO
Pontuação: 45
Ação: ALERTAR
```

### Cenário 3 — Acesso de alto risco

```text
Usuário: Carlos
País: Alemanha
Horário: 03:15
IP conhecido: não
Dispositivo conhecido: não

Risco: ALTO
Pontuação: 100
Ação: BLOQUEAR
```

---

# 🧪 Testes

Os testes automatizados podem ser executados com:

```powershell
python -m pytest
```

Os testes verificam principalmente o funcionamento do motor de análise de risco e componentes do sistema.

---

# 🔐 Segurança

O projeto foi desenvolvido com foco em **detecção e resposta a acessos suspeitos**.

Entre os mecanismos implementados estão:

- validação dos dados recebidos pela API;
- classificação de risco;
- registro de eventos;
- rastreabilidade das decisões;
- separação entre análise e ação de segurança;
- armazenamento estruturado dos eventos.

O SentinelAI é um projeto acadêmico e não deve ser utilizado como mecanismo de segurança de produção sem validações, testes e controles adicionais.

---

# 🔮 Evolução futura

A arquitetura permite evoluções como:

- Machine Learning para detecção de anomalias;
- criação automática do perfil comportamental individual;
- análise de localização geográfica;
- análise de velocidade de deslocamento;
- identificação de múltiplos dispositivos;
- autenticação multifator;
- integração com sistemas de identidade;
- notificações automáticas;
- integração com SIEM;
- dashboards mais avançados;
- geração de relatórios;
- banco de dados PostgreSQL;
- execução em ambiente cloud;
- monitoramento contínuo.

---

# 👥 Equipe

Projeto desenvolvido pela equipe **Cibersegurança Acadêmica**.

### Responsabilidades técnicas

- Modelagem de dados / DER
- Desenvolvimento do backend
- Desenvolvimento do frontend
- Motor de análise de risco
- Testes
- Integração entre API e interface
- Documentação
- Versionamento com Git/GitHub

---

# 📄 Licença

Projeto desenvolvido para fins acadêmicos e educacionais.
