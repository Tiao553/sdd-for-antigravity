# BRAINSTORM: PBI Multi-Agent PBIP Generator

> Exploratory session to clarify intent and approach before requirements capture

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | PBI_MULTI_AGENT |
| **Date** | 2026-04-23 |
| **Author** | brainstorm-agent |
| **Status** | Ready for Define |

---

## Initial Idea

**Raw Input:** Construir um sistema multi-agent para geração de PBIT/PBIP — o formato que a IA consegue manipular nativamente.

**Context Gathered:**
- O formato **PBIP** (Power BI Project) é text-based (TMDL + PBIR/JSON), ideal para manipulação por IA
- O formato **PBIT** é um ZIP binário — mais difícil de manipular programaticamente
- O ecossistema Microsoft Fabric já suporta PBIP nativamente com Git integration
- AgentSpec serve como **harness de desenvolvimento** (SDD workflow), não como runtime do sistema
- O produto final é uma **aplicação standalone Python** com orquestração multi-agent

**Technical Context Observed (for Define):**

| Aspect | Observation | Implication |
|--------|-------------|-------------|
| Likely Location | Novo repositório standalone | Projeto independente do AgentSpec |
| Relevant KB Domains | microsoft-fabric, data-modeling, genai | Patterns de Fabric, modelagem, e IA |
| IaC Patterns | N/A (aplicação local/CLI) | Sem infraestrutura cloud no MVP |
| Output Format | PBIP (TMDL + PBIR) | Text-based, Git-friendly, AI-native |

---

## Discovery Questions & Answers

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | Qual cenário principal de uso? | Gerar relatórios Power BI **do zero** a partir de requisitos em linguagem natural | Define o pipeline como end-to-end: prompt → PBIP |
| 2 | Qual o input do sistema? | O agente interno terá informações e schemas para alocar os dados certos | Sistema precisa de um **catálogo interno de schemas** como knowledge base |
| 3 | Qual a stack de execução? | Standalone com **CrewAI ou LangGraph**. AgentSpec é só o harness para construir | Produto final é app Python independente, não integrado ao AgentSpec |
| 4 | Preferência de framework multi-agent? | Sem preferência — quer recomendação | Avaliação comparativa CrewAI vs LangGraph necessária |
| 5 | Tem samples/ground truth? | Nenhum por enquanto — construir do zero | Primeira tarefa do projeto: criar exemplos de referência PBIP válidos |
| 6 | Qual LLM provider? | **OpenRouter** | Flexibilidade total de modelo via API unificada; otimização de custo por agente |

---

## Sample Data Inventory

> Samples improve LLM accuracy through in-context learning and few-shot prompting.

| Type | Location | Count | Notes |
|------|----------|-------|-------|
| Input files | N/A | 0 | Precisam ser criados — exemplos de prompts de requisitos |
| Output examples | N/A | 0 | Precisam ser criados — projetos PBIP de referência válidos |
| Ground truth | N/A | 0 | Criar PBIPs manualmente no PBI Desktop e salvar como referência |
| Related code | N/A | 0 | Sem código existente — projeto greenfield |

**How samples will be used:**

- Few-shot examples em prompts dos agentes (estrutura TMDL válida)
- Templates de PBIR JSON para o Layout Designer clonar e adaptar
- Schemas YAML de referência para o Schema Mapper
- Test fixtures para validação do PBIP Assembler

**Ação necessária:** Criar 2-3 projetos PBIP de referência manualmente no Power BI Desktop (vendas, RH, financeiro) antes de codificar os agentes.

---

## Approaches Explored

### Approach A: LangGraph — Pipeline com Nós Especializados ⭐ Recommended

**Description:** Cada agente é um nó em um grafo LangGraph com estado compartilhado (`TypedDict`). O fluxo é um pipeline com gates de validação e loops de retry automáticos.

```text
[User Prompt]
    → [Requirement Analyst] — interpreta pedido, extrai entidades/métricas
    → [Schema Mapper] — mapeia requisitos para schemas internos
    → [TMDL Builder] — gera modelo semântico (tabelas, relações, medidas)
    → [TMDL Validator] — valida sintaxe e consistência
        ↺ retry loop se inválido (max 3 tentativas)
    → [Layout Designer] — gera PBIR (páginas, visuais, filtros)
    → [PBIP Assembler] — monta estrutura de pastas final
    → [Quality Gate] — validação final do pacote completo
```

**Pros:**
- Controle granular do fluxo (conditional edges, cycles, retries)
- Estado tipado e compartilhado entre agentes (`TypedDict`)
- Suporte nativo a checkpointing (pausar/retomar geração)
- Integração natural com OpenRouter via `ChatOpenAI(base_url=...)`
- Melhor para outputs determinísticos (arquivos, não chat)
- Ecossistema LangChain para tools, parsers, e prompts

**Cons:**
- Mais boilerplate que CrewAI
- Curva de aprendizado um pouco maior

**Why Recommended:** Gerar PBIP é essencialmente um **compilador** — precisa de validação em múltiplas etapas, retry quando DAX está errado, e state management preciso. LangGraph foi feito exatamente para pipelines com fluxo condicional e estado compartilhado.

---

### Approach B: CrewAI — Crew Sequencial com Agentes Roleplaying

**Description:** Cada agente tem role/goal/backstory. Tasks executam sequencialmente. Output de um agente vira input do próximo.

**Pros:**
- Setup mais simples e intuitivo
- Abstração de alto nível (menos código)
- Bom para prototipagem rápida

**Cons:**
- Menos controle sobre fluxo condicional
- Difícil implementar retry loops granulares (quando TMDL Validator encontra erro, precisa voltar apenas ao TMDL Builder com feedback específico — CrewAI não faz isso nativamente)
- State management menos robusto
- Mais difícil debugar erros na geração de TMDL

---

### Approach C: Híbrido — LangGraph + Tool-Calling Agents

**Description:** LangGraph para orquestração macro, cada nó usa agente com tools (funções Python que geram/validam TMDL e PBIR).

**Pros:**
- Máxima flexibilidade e extensibilidade
- Agentes podem chamar ferramentas de validação diretamente
- Melhor para escalar no futuro

**Cons:**
- Complexidade alta demais para MVP
- Over-engineering para a primeira versão
- Pode evoluir para isso a partir do Approach A

---

## Selected Approach

| Attribute | Value |
|-----------|-------|
| **Chosen** | Approach A — LangGraph Pipeline com Nós Especializados |
| **User Confirmation** | 2026-04-23 20:34 |
| **Reasoning** | Melhor controle de fluxo, retry loops nativos, estado tipado, e ideal para pipeline de geração de arquivos determinísticos. OpenRouter integra nativamente via LangChain. |

---

## Key Decisions Made

| # | Decision | Rationale | Alternative Rejected |
|---|----------|-----------|----------------------|
| 1 | **LangGraph** como framework de orquestração | Retry loops, conditional edges, estado tipado — essencial para pipeline de compilação TMDL | CrewAI (menos controle de fluxo) |
| 2 | **PBIP** como formato de saída (não PBIT) | Text-based (TMDL + PBIR JSON), AI-native, Git-friendly | PBIT (ZIP binário, difícil de manipular) |
| 3 | **OpenRouter** como LLM provider | Flexibilidade de modelo, otimização de custo por agente | Provider único (lock-in) |
| 4 | **Catálogo de schemas em YAML** como knowledge base | Simples, versionável, fácil de estender | Banco de dados (over-engineering para v1) |
| 5 | **6 agentes especializados** | Separação clara de responsabilidades, testabilidade | Agente monolítico (impossível de debugar) |
| 6 | **AgentSpec como harness de dev** (não runtime) | SDD workflow para planejar/construir; produto final é standalone | Integrar agentes no AgentSpec (mistura responsabilidades) |

---

## Features Removed (YAGNI)

| Feature Suggested | Reason Removed | Can Add Later? |
|-------------------|----------------|----------------|
| Visuais avançados (mapas, scatter, treemap) | Complexidade alta de layout JSON; tabela + bar + KPI card resolve MVP | Yes |
| Interface web/chat interativa | CLI é suficiente para validar o conceito | Yes |
| Conexão direta a bancos de dados | Schema manual via YAML primeiro | Yes |
| Temas customizados / branding | Layout padrão do PBI funciona | Yes |
| Multi-página automática | Uma página resolve 80% dos casos MVP | Yes |
| Deploy no Fabric Service via API | Foco em gerar arquivo local primeiro | Yes |
| Streaming / real-time refresh | Batch é suficiente para v1 | Yes |

---

## Agent Architecture

### Agentes do Sistema

| # | Agent | Responsibility | Input | Output |
|---|-------|---------------|-------|--------|
| 1 | **Requirement Analyst** | Interpreta prompt do usuário, extrai entidades, métricas, filtros, tipo de visual desejado | Prompt em linguagem natural | JSON estruturado com requisitos |
| 2 | **Schema Mapper** | Mapeia requisitos para tabelas/colunas do catálogo interno de schemas | Requisitos JSON + Catálogo YAML | Mapeamento entidade→tabela→coluna |
| 3 | **TMDL Builder** | Gera arquivos TMDL (tables, relationships, measures) | Mapeamento de schema | Arquivos `.tmdl` do semantic model |
| 4 | **DAX Specialist** | Gera/otimiza medidas DAX complexas (YoY, Running Total, etc.) | Requisitos de métricas + contexto do modelo | Blocos de medidas DAX válidas |
| 5 | **Layout Designer** | Gera estrutura PBIR (páginas, visuais, posicionamento, filtros) | Requisitos + modelo TMDL gerado | Arquivos JSON do report (PBIR) |
| 6 | **PBIP Assembler** | Monta estrutura de pastas PBIP final, valida completude | Todos os outputs anteriores | Pasta PBIP pronta para PBI Desktop |

### Estado Compartilhado (LangGraph State)

```python
class PBIPState(TypedDict):
    user_prompt: str
    requirements: dict           # Output do Requirement Analyst
    schema_mapping: dict         # Output do Schema Mapper
    tmdl_files: dict[str, str]   # filename → content
    tmdl_valid: bool             # Gate de validação
    tmdl_errors: list[str]       # Erros para retry
    retry_count: int             # Contador de retries (max 3)
    dax_measures: list[dict]     # Output do DAX Specialist
    pbir_files: dict[str, str]   # filename → content
    output_path: str             # Caminho da pasta PBIP final
    status: str                  # success | failed | retrying
```

### Estrutura de Saída PBIP

```text
output/MeuRelatorio/
├── MeuRelatorio.pbip                    # Pointer file
├── MeuRelatorio.SemanticModel/
│   ├── definition/
│   │   ├── model.tmdl                   # Model metadata
│   │   ├── tables/
│   │   │   ├── Vendas.tmdl              # Table definition
│   │   │   └── Produtos.tmdl
│   │   ├── relationships.tmdl           # Relationships
│   │   └── expressions.tmdl             # DAX measures
│   └── .platform                        # Platform config
├── MeuRelatorio.Report/
│   ├── definition/
│   │   ├── pages/
│   │   │   └── page1/
│   │   │       ├── page.json            # Page config
│   │   │       └── visuals/
│   │   │           ├── visual1.json     # Bar chart
│   │   │           ├── visual2.json     # Table
│   │   │           └── visual3.json     # KPI card
│   │   └── report.json                  # Report config
│   └── .platform
└── .gitignore
```

---

## Incremental Validations

| Section | Presented | User Feedback | Adjusted? |
|---------|-----------|---------------|-----------|
| Composição dos 6 agentes | ✅ | "faz sentido" | No |
| Escopo MVP vs YAGNI | ✅ | "concordo" | No |

---

## Suggested Requirements for /define

Based on this brainstorm session, the following should be captured in the DEFINE phase:

### Problem Statement (Draft)
Equipes de BI precisam criar relatórios Power BI repetitivos e padronizados manualmente, consumindo horas em tarefas que poderiam ser automatizadas. Um sistema multi-agent pode gerar projetos PBIP completos e válidos a partir de requisitos em linguagem natural, acelerando drasticamente o ciclo de desenvolvimento de relatórios.

### Target Users (Draft)
| User | Pain Point |
|------|------------|
| Analista de BI | Gasta horas montando relatórios padrão que seguem templates similares |
| Engenheiro de Dados | Precisa criar modelos semânticos repetitivos para diferentes domínios |
| Gestor / Stakeholder | Quer relatórios rápidos sem esperar sprint de BI |

### Success Criteria (Draft)
- [ ] Sistema gera PBIP válido que abre no Power BI Desktop sem erros
- [ ] TMDL gerado passa validação de sintaxe
- [ ] Relatório gerado contém pelo menos 3 visuais funcionais (tabela, gráfico, KPI)
- [ ] Pipeline completo executa em menos de 60 segundos
- [ ] Medidas DAX geradas são sintaticamente corretas

### Constraints Identified
- Power BI Desktop necessário para validação visual (não há preview headless)
- Formato PBIP ainda em evolução — Microsoft pode alterar schema
- DAX gerado por LLM precisa de validação rigorosa (alucinações comuns)
- Sem API oficial da Microsoft para gerar PBIP programaticamente

### Out of Scope (Confirmed)
- Visuais avançados (mapas, scatter, treemap)
- Interface web/chat interativa
- Conexão direta a bancos de dados
- Temas customizados / branding
- Multi-página automática
- Deploy no Fabric Service via API
- Streaming / real-time refresh

---

## Technology Stack (Draft)

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Orchestration** | LangGraph | Fluxo condicional, retry loops, estado tipado |
| **LLM Provider** | OpenRouter | Flexibilidade de modelo, custo otimizável |
| **Language** | Python 3.11+ | Ecossistema LangChain, tipagem moderna |
| **Schema Catalog** | YAML files | Simples, versionável, legível |
| **CLI** | Click ou Typer | Interface mínima para MVP |
| **Validation** | Custom Python validators | Checagem de sintaxe TMDL e estrutura PBIR |
| **Testing** | Pytest | Testes unitários para cada agente |
| **Dev Workflow** | AgentSpec SDD | /define → /design → /build → /ship |

---

## Session Summary

| Metric | Value |
|--------|-------|
| Questions Asked | 6 |
| Approaches Explored | 3 |
| Features Removed (YAGNI) | 7 |
| Validations Completed | 2 |
| Duration | ~5 min |

---

## Next Step

**Ready for:** `/define .agents/sdd/features/BRAINSTORM_PBI_MULTI_AGENT.md`
