# 🛡️ SentinelAI

### Sistema de Análise de Risco para Acessos

O **SentinelAI** é um MVP acadêmico de cibersegurança que analisa características de acessos, calcula uma pontuação de risco e registra a classificação e a decisão de segurança associada a cada evento.

O projeto foi desenvolvido para a atividade de **Sistemas Guiados por IA**, com foco em cibersegurança, análise comportamental, banco de dados e desenvolvimento de APIs.

> **Status:** MVP funcional  
> **Versão:** 1.0.0

---

## 🎯 Sobre o projeto

Instituições de ensino utilizam sistemas acadêmicos que armazenam informações de alunos, professores e funcionários. A análise manual de muitos eventos de acesso pode dificultar a identificação de comportamentos suspeitos.

O SentinelAI busca auxiliar esse processo por meio de uma análise automatizada das características de login. No MVP, o sistema registra eventos, calcula uma pontuação de risco, classifica o acesso e registra a decisão correspondente.

## 🚨 Problema

O cenário abordado apresenta três desafios principais:

- Grande quantidade de acessos aos sistemas acadêmicos.
- Dificuldade de monitorar manualmente todos os eventos.
- Necessidade de identificar e revisar rapidamente acessos potencialmente suspeitos.

Um acesso fora do horário habitual, originado de um país diferente do padrão do usuário e realizado em um dispositivo desconhecido pode justificar uma análise mais cuidadosa. Esses sinais, isoladamente, não comprovam que houve um ataque.

## 💡 Como funciona

O fluxo conceitual do MVP é:

```text
Evento de login
      ↓
Coleta das características do acesso
      ↓
Análise baseada em regras
      ↓
Cálculo da pontuação de risco
      ↓
Classificação do risco
      ↓
Decisão registrada: PERMITIR, ALERTAR ou BLOQUEAR
      ↓
Registro para consulta e auditoria
```

**Importante:** `BLOQUEAR` representa a decisão de segurança indicada ou registrada pelo MVP. Um bloqueio efetivo do login exige integração com o sistema de autenticação ou autorização da instituição.

---

## 🧠 Motor de análise de risco

A versão atual utiliza um **motor de pontuação baseado em regras determinísticas**. Cada condição identificada adiciona pontos ao risco.

| Fator analisado | Pontuação adicionada |
|---|---:|
| Login fora do horário habitual | +25 |
| País diferente do padrão do usuário | +35 |
| Dispositivo não reconhecido | +20 |
| IP não reconhecido | +20 |

A pontuação máxima possível é de 100 pontos.

### Classificação

| Pontuação | Nível | Decisão associada |
|---:|---|---|
| 0–39 | BAIXO | PERMITIR |
| 40–69 | MÉDIO | ALERTAR |
| 70–100 | ALTO | BLOQUEAR |

Os limites e pesos são definidos no código. Eles são critérios iniciais do protótipo e precisam ser avaliados e ajustados com testes antes de qualquer uso operacional.

Um acesso fora do padrão pode ser legítimo, assim como uma pontuação baixa não garante que um acesso seja seguro.

### Exemplo de cálculo

Considere um acesso às 03:15, originado da Alemanha, com dispositivo e IP não reconhecidos:

```text
Horário fora do padrão:       +25
País diferente do padrão:     +35
Dispositivo não reconhecido:  +20
IP não reconhecido:           +20
                              ---
Pontuação total:              100
```

Resultado esperado:

```text
Nível de risco: ALTO
Decisão associada: BLOQUEAR
```

---

## 🤖 Relação com Inteligência Artificial

O projeto foi desenvolvido no contexto acadêmico de **Sistemas Guiados por IA** e aborda análise comportamental e identificação de acessos potencialmente anômalos.

**Limite da versão atual:** o motor do MVP utiliza regras determinísticas; ele não treina nem executa um modelo de Machine Learning. Portanto, não é correto afirmar que a versão atual aprende automaticamente com os acessos.

Como evolução futura, o sistema poderá ser ampliado com técnicas como:

- Machine Learning para detecção de anomalias.
- Criação e atualização de perfis comportamentais.
- Análise estatística dos eventos.
- Modelos de classificação treinados e avaliados com dados apropriados.

Essas possibilidades são propostas de evolução, não funcionalidades que esta versão afirma já possuir.

---

## 🏗️ Arquitetura

O projeto está organizado em componentes separados:

```text
┌──────────────────────────┐
│ Streamlit                │
│ Interface / Dashboard    │
└────────────┬─────────────┘
             │ HTTP / REST
             ▼
┌──────────────────────────┐
│ FastAPI                  │
│ API / Backend            │
└────────────┬─────────────┘
             │
     ┌───────┼─────────┐
     ▼       ▼         ▼
┌────────┐ ┌────────┐ ┌────────────┐
│ Análise│ │ Ações  │ │ Repositório│
│ de risco│ │segurança│ │ de dados   │
└────────┘ └────────┘ └─────┬──────┘
                            ▼
                      ┌──────────┐
                      │ SQLite   │
                      └──────────┘
```

- **Streamlit:** interface visual e páginas de acompanhamento.
- **FastAPI:** disponibiliza os endpoints da API.
- **Uvicorn:** servidor utilizado para executar a aplicação FastAPI.
- **Motor de risco:** calcula a pontuação e classifica o evento conforme as regras definidas.
- **Camada de segurança:** associa a classificação à decisão de segurança prevista no sistema.
- **Camada de repositórios:** organiza o acesso aos dados.
- **SQLite:** banco de dados utilizado no MVP.

O diagrama representa a organização lógica do projeto. O fluxo exato de cada operação depende da implementação dos respectivos módulos.

---

## 🗄️ Banco de dados

O MVP utiliza **SQLite** para armazenar os dados localmente.

### Entidades e relacionamentos

```text
USUARIO 1 ───── N DISPOSITIVO
   │
   ├─────────── N ACESSO
   │
   └─────────── N REGRA_COMPORTAMENTAL

DISPOSITIVO 1 ─ N ACESSO

ACESSO 1 ─────── 1 ANALISE_RISCO

ANALISE_RISCO 1 ─ N ACAO_SEGURANCA
```

### Entidades principais

| Entidade | Finalidade |
|---|---|
| `USUARIO` | Armazena os dados dos usuários. |
| `DISPOSITIVO` | Registra dispositivos associados aos usuários. |
| `ACESSO` | Registra eventos de login. |
| `REGRA_COMPORTAMENTAL` | Armazena referências do comportamento esperado. |
| `ANALISE_RISCO` | Guarda a pontuação, o nível e os motivos da análise. |
| `ACAO_SEGURANCA` | Registra a decisão ou ação associada à análise. |

As chaves primárias identificam registros, enquanto as chaves estrangeiras relacionam registros entre tabelas. As cardinalidades indicadas representam o modelo lógico esperado; as restrições efetivamente garantidas dependem das definições no banco de dados e das validações da aplicação.

---

## 🖥️ Interface

O frontend foi desenvolvido utilizando Streamlit.

### Dashboard

A página reúne indicadores e informações resumidas, como quantidade de acessos, alertas, eventos de risco e últimos registros, conforme os dados disponíveis na API.

### Monitoramento

Apresenta informações dos eventos registrados, como:

- Nível de risco.
- Pontuação.
- IP de origem.
- Localização.
- Data e hora.
- Decisão associada.
- Motivos identificados.

A atualização dos dados depende do mecanismo de consulta e atualização implementado na interface. Por isso, esta documentação não presume atualização contínua em tempo real.

### Auditoria

Permite consultar registros históricos e filtrar eventos por critérios disponibilizados pela interface, como nível de risco ou decisão associada.

---

## 🛠️ Tecnologias

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLite

### Frontend

- Streamlit
- Requests
- Pandas

### Testes e desenvolvimento

- Pytest
- Git
- GitHub
- API HTTP/REST

---

## 📂 Estrutura do projeto

```text
sentinel-ai/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── repositories.py
│   ├── risk_analysis.py
│   └── security.py
├── database/
│   └── schema.sql
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── cards.py
│   │   └── tables.py
│   └── views/
│       ├── __init__.py
│       ├── dashboard.py
│       ├── monitoramento.py
│       └── auditoria.py
├── scripts/
│   └── seed_demo.py
├── tests/
│   ├── test_database.py
│   └── test_risk.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 Instalação

### 1. Clonar o repositório

Substitua `<URL_DO_REPOSITORIO>` pela URL real do repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd sentinel-ai
```

### 2. Criar e ativar o ambiente virtual

**Windows — PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Se o PowerShell impedir a execução do script de ativação, consulte as configurações de execução do Python/PowerShell do seu ambiente. Como alternativa, no Prompt de Comando (CMD), use:

```bat
venv\Scripts\activate.bat
```

### 3. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
python -m pip install -r requirements.txt
```

---

## ▶️ Executar o projeto

Abra dois terminais na pasta do projeto e ative o ambiente virtual em ambos.

### Backend

No primeiro terminal:

```powershell
python -m uvicorn app.main:app --reload
```

A API ficará disponível localmente em:

- **API:** `http://127.0.0.1:8000`
- **Documentação interativa (Swagger):** `http://127.0.0.1:8000/docs`

### Frontend

No segundo terminal:

```powershell
python -m streamlit run frontend/app.py
```

A interface ficará disponível em:

`http://localhost:8501`

---

## 🎭 Dados de demonstração

Com o backend em execução, rode o script de demonstração em outro terminal, com o ambiente virtual ativado:

```powershell
python scripts/seed_demo.py
```

O script foi criado para enviar cenários demonstrativos à API. Os resultados abaixo ilustram o comportamento esperado das regras descritas; confirme-os executando o projeto.

### Cenário 1 — Acesso dentro do padrão

```text
Usuário: João
País: Brasil
Horário: 10:30
IP conhecido: sim
Dispositivo conhecido: sim

Risco esperado: BAIXO
Pontuação esperada: 0
Decisão associada: PERMITIR
```

### Cenário 2 — Acesso suspeito

```text
Usuário: Maria
País: Brasil
Horário: 23:45
IP conhecido: não
Dispositivo conhecido: sim

Risco esperado: MÉDIO
Pontuação esperada: 45
Decisão associada: ALERTAR
```

### Cenário 3 — Acesso de alto risco

```text
Usuário: Carlos
País: Alemanha
Horário: 03:15
IP conhecido: não
Dispositivo conhecido: não

Risco esperado: ALTO
Pontuação esperada: 100
Decisão associada: BLOQUEAR
```

---

## 🧪 Testes

Para executar os testes automatizados:

```powershell
python -m pytest
```

Os testes existentes podem verificar comportamentos do motor de risco e do banco de dados. A cobertura real depende dos casos implementados nos arquivos da pasta `tests/`.

---

## 🔐 Segurança e limitações

O SentinelAI é um **protótipo acadêmico**, não uma solução pronta para proteger sistemas em produção.

O MVP contempla análise baseada em regras, classificação de risco e registro de eventos e decisões. Antes de uma utilização real, seriam necessários, entre outros pontos:

- Integração validada com o sistema de autenticação para aplicar bloqueios efetivos.
- Testes de segurança e desempenho.
- Autenticação e autorização da própria API.
- Proteção de credenciais e dados sensíveis.
- Validação dos pesos e limites com dados representativos.
- Monitoramento, tratamento de falhas e auditoria operacional.

A pontuação indica o grau de risco segundo as regras atuais; não confirma, por si só, que um acesso é malicioso.

---

## 🔮 Evolução futura

Possíveis melhorias incluem:

- Machine Learning para detecção de anomalias.
- Criação e atualização de perfis comportamentais.
- Análise geográfica e de padrões de deslocamento.
- Integração com autenticação multifator.
- Integração com sistemas de identidade.
- Notificações automáticas.
- Integração com SIEM.
- Relatórios e dashboards mais avançados.
- Migração do SQLite para PostgreSQL.
- Implantação em ambiente cloud.
- Monitoramento contínuo.

Esses itens representam possibilidades de evolução e não devem ser interpretados como funcionalidades já entregues no MVP.

---

## 👥 Equipe

Projeto desenvolvido pela equipe **Cibersegurança Acadêmica**.

### Áreas de trabalho

- Modelagem de dados e DER.
- Desenvolvimento do backend e da API.
- Desenvolvimento da interface.
- Motor de análise de risco.
- Testes.
- Integração entre API e interface.
- Documentação.
- Versionamento com Git/GitHub.

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e educacionais. Nenhuma licença de software específica é declarada nesta documentação.

