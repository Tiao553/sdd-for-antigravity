# DEFINE: PBI Multi-Agent PBIP Generator

> A standalone Python multi-agent system that generates complete, valid Power BI PBIP projects from natural language requirements using LangGraph orchestration and OpenRouter LLMs.

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | PBI_MULTI_AGENT |
| **Date** | 2026-04-23 |
| **Author** | define-agent |
| **Status** | ✅ Complete (Designed) |
| **Clarity Score** | 15/15 |
| **Source** | BRAINSTORM_PBI_MULTI_AGENT.md |

---

## Problem Statement

Equipes de BI gastam horas criando relatórios Power BI repetitivos e padronizados manualmente — montando modelos semânticos, escrevendo medidas DAX, e posicionando visuais em layouts similares. Esse trabalho mecânico consome ciclos de sprint que poderiam ser usados em análise de valor. Um sistema multi-agent pode gerar projetos PBIP completos e válidos a partir de requisitos em linguagem natural, acelerando drasticamente o ciclo de desenvolvimento de relatórios e eliminando erros de montagem manual.

---

## Target Users

| User | Role | Pain Point |
|------|------|------------|
| Analista de BI | Cria relatórios e dashboards no Power BI | Gasta horas montando relatórios padrão que seguem templates similares — trabalho repetitivo e propenso a erros |
| Engenheiro de Dados | Modela semantic layers e pipelines de dados | Precisa criar modelos semânticos TMDL repetitivos para diferentes domínios de negócio |
| Gestor / Stakeholder | Consome insights de dados para decisão | Quer relatórios rápidos sob demanda sem esperar sprint de BI ou disponibilidade da equipe |

---

## Goals

What success looks like (prioritized):

| Priority | Goal |
|----------|------|
| **MUST** | Gerar projeto PBIP completo e válido que abre no Power BI Desktop sem erros |
| **MUST** | Implementar pipeline de 6 agentes especializados com LangGraph (Requirement Analyst → Schema Mapper → TMDL Builder → DAX Specialist → Layout Designer → PBIP Assembler) |
| **MUST** | Suportar catálogo de schemas em YAML como knowledge base dos agentes |
| **MUST** | Integrar com OpenRouter para flexibilidade de modelo LLM e otimização de custo por agente |
| **MUST** | Gerar dados sintéticos (shadow data) inline via expressões M (Power Query) para que o relatório funcione sem necessidade de um banco de dados real |
| **SHOULD** | Implementar retry loops automáticos para validação TMDL (max 3 tentativas) |
| **SHOULD** | Gerar relatório com pelo menos 3 tipos de visuais funcionais (tabela, gráfico de barras, KPI card) |
| **SHOULD** | Executar pipeline completo em menos de 60 segundos |
| **COULD** | Suportar checkpointing para pausar/retomar geração |
| **COULD** | CLI via Click ou Typer para interface mínima de uso |

**Priority Guide:**
- **MUST** = MVP fails without this
- **SHOULD** = Important, but workaround exists
- **COULD** = Nice-to-have, cut first if needed

---

## Success Criteria

Measurable outcomes (must include numbers):

- [ ] Sistema gera PBIP válido que abre no Power BI Desktop sem erros em 100% dos schemas de referência testados
- [ ] TMDL gerado passa validação de sintaxe em ≥95% dos casos (com retry, 100%)
- [ ] Relatório gerado contém pelo menos 3 visuais funcionais (tabela, gráfico de barras, KPI card)
- [ ] Pipeline completo executa em menos de 60 segundos para um relatório single-page
- [ ] Medidas DAX geradas são sintaticamente corretas em ≥90% dos casos (com retry do DAX Specialist, ≥98%)
- [ ] Catálogo de schemas suporta no mínimo 3 domínios de referência (vendas, RH, financeiro)
- [ ] Estrutura de pastas PBIP gerada é 100% compatível com o formato PBI Desktop/Fabric

---

## Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Happy path — relatório de vendas | Schema de vendas carregado no catálogo YAML | Usuário submete "Crie um dashboard de vendas por região e produto" | PBIP gerado abre no PBI Desktop com tabela, bar chart, e KPI card funcionais |
| AT-002 | TMDL com erro — retry automático | TMDL Builder gera TMDL com erro de sintaxe | TMDL Validator detecta erro na primeira tentativa | Sistema faz retry com feedback do erro; TMDL válido gerado na 2ª ou 3ª tentativa |
| AT-003 | Retry esgotado — falha graceful | TMDL Builder falha 3 vezes consecutivas | Retry count atinge máximo (3) | Sistema retorna status "failed" com lista de erros, sem crash |
| AT-004 | Schema não encontrado | Usuário pede relatório sobre domínio não presente no catálogo | Schema Mapper não encontra mapeamento | Sistema retorna erro claro: "Schema não encontrado para domínio X" |
| AT-005 | DAX complexo — YoY calculation | Requisito inclui "crescimento ano a ano" | DAX Specialist gera medida YoY | Medida DAX usa CALCULATE + SAMEPERIODLASTYEAR corretamente |
| AT-006 | Múltiplas tabelas com relacionamentos | Schema tem tabelas fato + dimensão | TMDL Builder gera modelo | Relationships.tmdl contém foreign keys corretas entre tabelas |
| AT-007 | Estrutura PBIP completa | Pipeline executa com sucesso | PBIP Assembler monta pasta final | Todos os arquivos obrigatórios presentes (.pbip, .platform, model.tmdl, report.json) |
| AT-008 | Prompt vago — extração robusta | Usuário submete "quero ver as vendas" | Requirement Analyst interpreta prompt | JSON de requisitos contém entidade "vendas" e visual default (tabela) |
| AT-009 | OpenRouter fallback | Modelo primário retorna erro 429 | Sistema tenta chamada ao LLM | Retry com backoff exponencial ou troca de modelo via OpenRouter |
| AT-010 | Tempo de execução | Schemas de referência carregados | Pipeline executa end-to-end | Tempo total ≤ 60 segundos |
| AT-011 | Shadow Data funcional | PBIP aberto no PBI Desktop | Visuals carregam dados sintéticos | Expressões M no Power Query geram dados inline e gráficos são renderizados sem pedir credenciais |

---

## Out of Scope

Explicitly NOT included in this feature (MVP):

- **Visuais avançados** — mapas, scatter plots, treemaps (tabela + bar chart + KPI card resolve MVP)
- **Interface web/chat interativa** — CLI é suficiente para validar o conceito
- **Conexão direta a bancos de dados** — substituído pela geração de *shadow data* (dados sintéticos inline) via M expressions
- **Temas customizados / branding** — layout padrão do PBI funciona
- **Multi-página automática** — uma página resolve 80% dos casos MVP
- **Deploy no Fabric Service via API** — foco em gerar arquivo local primeiro
- **Streaming / real-time refresh** — batch é suficiente para v1

---

## Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| Technical | Power BI Desktop necessário para validação visual — não há preview headless | Testes automatizados limitados a validação de sintaxe/estrutura; validação visual é manual |
| Technical | Formato PBIP ainda em evolução — Microsoft pode alterar schema entre versões | Design deve isolar geração de TMDL/PBIR em módulos substituíveis |
| Technical | DAX gerado por LLM é propenso a alucinações — requer validação rigorosa | Necessário retry loop com feedback de erros e possível validação via regex/parser |
| External | Sem API oficial da Microsoft para gerar PBIP programaticamente | Engenharia reversa dos formatos TMDL e PBIR a partir de projetos de referência |

---

## Technical Context

> Essential context for Design phase — prevents misplaced files and missed infrastructure needs.

| Aspect | Value | Notes |
|--------|-------|-------|
| **Deployment Location** | Novo repositório standalone (fora do AgentSpec) | Projeto Python independente; AgentSpec é apenas o harness de desenvolvimento |
| **KB Domains** | microsoft-fabric, data-modeling, genai | Patterns de Fabric para formato PBIP, modelagem dimensional para schemas, GenAI para prompts |
| **IaC Impact** | None | Aplicação local/CLI — sem infraestrutura cloud no MVP |
| **Output Format** | PBIP (TMDL + PBIR JSON) | Text-based, Git-friendly, AI-native |

**Why This Matters:**

- **Location** → Design phase creates a standalone Python project structure, not within AgentSpec
- **KB Domains** → Design phase pulls TMDL patterns from `microsoft-fabric`, dimensional modeling from `data-modeling`, prompt engineering from `genai`
- **IaC Impact** → No infrastructure planning needed; pure local CLI application

---

## Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Orchestration** | LangGraph | Fluxo condicional, retry loops, estado tipado — ideal para pipeline de compilação |
| **LLM Provider** | OpenRouter | Flexibilidade de modelo, custo otimizável por agente |
| **Language** | Python 3.11+ | Ecossistema LangChain, tipagem moderna (TypedDict, dataclasses) |
| **Schema Catalog** | YAML files | Simples, versionável, legível por humanos e LLMs |
| **CLI** | Click ou Typer | Interface mínima para MVP |
| **Validation** | Custom Python validators | Checagem de sintaxe TMDL e estrutura PBIR |
| **Testing** | Pytest | Testes unitários para cada agente e integração end-to-end |
| **Dev Workflow** | AgentSpec SDD | /define → /design → /build → /ship |

---

## Agent Architecture

### Pipeline de 6 Agentes

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

## Assumptions

Assumptions that if wrong could invalidate the design:

| ID | Assumption | If Wrong, Impact | Validated? |
|----|------------|------------------|------------|
| A-001 | Formato PBIP (TMDL + PBIR JSON) é estável o suficiente para v1 | Precisaria adaptar parsers/geradores a cada mudança de schema da Microsoft | [ ] |
| A-002 | LLMs acessíveis via OpenRouter conseguem gerar TMDL sintaticamente válido com few-shot prompting | Precisaria de fine-tuning ou abordagem template-based ao invés de geração livre | [ ] |
| A-003 | 3 domínios de referência (vendas, RH, financeiro) são suficientes para validar a abordagem | Precisaria de mais domínios para cobrir edge cases de schema mapping | [ ] |
| A-004 | Execução em menos de 60s é viável com 6 chamadas sequenciais ao LLM via OpenRouter | Precisaria de paralelização ou redução de agentes para atingir SLA de tempo | [ ] |

**Note:** Validate critical assumptions before DESIGN phase. Unvalidated assumptions become risks.

---

## Clarity Score Breakdown

| Element | Score (0-3) | Notes |
|---------|-------------|-------|
| Problem | 3 | Dor específica (horas em relatórios repetitivos), impacto claro (ciclos de sprint desperdiçados), solução definida (geração automática via multi-agent) |
| Users | 3 | Três personas identificadas com roles e pain points distintos |
| Goals | 3 | 9 goals com priorização MoSCoW, mensuráveis e acionáveis |
| Success | 3 | 7 critérios com números concretos (≥95%, ≤60s, ≥3 visuais, 3 domínios) |
| Scope | 3 | 7 itens explicitamente fora de escopo, 4 constraints técnicas documentadas |
| **Total** | **15/15** | |

**Scoring Guide:**
- 0 = Missing entirely
- 1 = Vague or incomplete
- 2 = Clear but missing details
- 3 = Crystal clear, actionable

**Minimum to proceed: 12/15** ✅

---

## Open Questions

None — ready for Design. All critical decisions were made during the brainstorm phase:

- ✅ Framework: LangGraph
- ✅ LLM Provider: OpenRouter
- ✅ Output format: PBIP (not PBIT)
- ✅ Agent count: 6 specialized agents
- ✅ Schema source: YAML catalog
- ✅ Scope boundaries: 7 YAGNI items defined

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-23 | define-agent | Initial version — extracted from BRAINSTORM_PBI_MULTI_AGENT.md |

---

## Next Step

**Ready for:** `/build .agents/sdd/features/DESIGN_PBI_MULTI_AGENT.md`
