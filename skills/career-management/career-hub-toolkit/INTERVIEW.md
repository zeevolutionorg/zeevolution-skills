# Interview script — exact questions

Use this wording. Don't improvise questions.

## Rules for asking

- **Skip what's already known.** Anything given in the command (`/career-hub-toolkit Ana Souza, Data Scientist L3, google`) or saved by setup is not asked again; show it in the confirmation (E) instead.
- **Multiple choice whenever possible**, through the agent's question tool (Claude's question dialog, Cursor's ask-questions tool). Free text only for names, dates and the ladder.
- **Batches of up to 4 questions**, in the order below. At most 2 batches before the confirmation.
- **Every question has a default.** "Not sure" = the default.
- **Ask in the user's language** (English or Português (Brasil)).

---

## A. One-time setup (`/setup-zeevolution-skills`)

| # | English | Português (Brasil) | Options (EN / pt-BR) | Default |
|---|---|---|---|---|
| S1 | "What's your name, as it should appear in the documents?" | "Qual é o seu nome, do jeito que deve aparecer nos documentos?" | Free text | — (required) |
| S2 | "What's your discipline?" | "Qual é a sua disciplina?" | Engineering · Data Science · Design · Product Management · Other / Engenharia · Ciência de Dados · Design · Gestão de Produto · Outra | Engineering |
| S3 | "Where should documents be created?" | "Onde os documentos devem ser criados?" | Google Workspace (Docs/Sheets/Drive) · Microsoft 365 (Word/Excel/OneDrive) · Files I upload myself (.docx/.xlsx) · Markdown I copy and paste myself / Arquivos que eu mesmo(a) subo (.docx/.xlsx) · Markdown que eu copio e colo | Detected; Files if the agent can write files and run Python, otherwise Markdown |
| S4 | "In which folder should new documents go? Paste a folder link or name, or leave empty to create 'zeevolution-skills' at the root." | "Em qual pasta os novos documentos devem ficar? Cole o link ou o nome de uma pasta, ou deixe vazio para criar 'zeevolution-skills' na raiz." | Free text / link | Create `zeevolution-skills/` |
| S5 | "Which language should documents use?" | "Em qual idioma os documentos devem ser escritos?" | English · Português (Brasil) | Conversation language |
| S6 | "Does your company have a career ladder you'd like to reuse by default? (You can still change it per person.)" | "Sua empresa tem uma trilha de carreira que você quer usar por padrão? (Dá para trocar por pessoa depois.)" | Yes, I'll share it now · Not now · We don't have one / Sim, vou compartilhar agora · Agora não · Não temos | Not now |

## B. Toolkit — mode and person

| # | English | Português (Brasil) | Options | Default | Asked when |
|---|---|---|---|---|---|
| T1 | "Who is this Career Hub for?" | "Para quem é este Hub de Carreira?" | Myself (self mode) · Someone I lead (lead mode) / Para mim · Para alguém que eu lidero | `me` → self; a name → lead | Mode unclear from the command |
| T2 | "What's the person's full name?" | "Qual é o nome completo da pessoa?" | Free text | — (required) | Lead mode, name not given |
| T3 | "What's their role and discipline?" *(self: "What's your role and discipline?")* | "Qual é o cargo e a disciplina dessa pessoa?" *(self: "Qual é o seu cargo e a sua disciplina?")* | Role (free text) + Engineering · Data Science · Design · Product Management · Other | Discipline from setup | Not given |
| T4 | "What's the current level? Use your company's name for it (e.g., 'L3', 'Senior', 'Designer II') or pick: Early career · Mid · Senior · Lead · Principal." | "Qual é o nível atual? Use o nome que sua empresa usa (ex.: 'L3', 'Sênior', 'Designer II') ou escolha: Início de carreira · Pleno · Sênior · Lead · Principal." | Free text or option | — (required) | Not given |
| T5 | "What's the next level they're growing toward?" *(self: "you're growing toward")* | "Qual é o próximo nível que essa pessoa busca?" *(self: "que você busca?")* | Free text or option | One step above T4 | Unless given |

## C. Toolkit — context and optional docs

| # | English | Português (Brasil) | Options | Default | Asked when |
|---|---|---|---|---|---|
| T6 | "When did you start working together (or when does this hub start)?" *(self: "When do you want this hub to start?")* | "Quando vocês começaram a trabalhar juntos (ou quando este hub começa)?" *(self: "Quando você quer que este hub comece?")* | Date | Today | Always |
| T7 | "Is this person joining the team now, or joined in the last 90 days?" | "Essa pessoa está entrando no time agora ou entrou nos últimos 90 dias?" | Yes, add the 30/60/90 Onboarding Plan · No / Sim, incluir o Plano de Onboarding 30/60/90 · Não | No | Lead mode |
| T8 | "Do you also want the Evidence Doc? It's meant for when a level is at risk; most people don't need it now." | "Você também quer o Documento de Evidências? Ele é para quando um nível está em risco; a maioria das pessoas não precisa agora." | Yes · No / Sim · Não | No | Lead mode |
| T9 | "When is your next 1:1? The Hub recommends meeting every two weeks to follow up on these documents." | "Quando é o próximo 1:1 de vocês? O Hub recomenda se encontrar a cada duas semanas para acompanhar estes documentos." | Date · Not scheduled yet / Data · Ainda não marcado | Two weeks from today | Always |
| T10 | "Should I use your saved ladder for this person?" | "Posso usar a trilha salva para essa pessoa?" | Yes · Use a different ladder · Use the generic ladder / Sim · Usar outra trilha · Usar a trilha genérica | Yes | A default ladder exists |

## D. Ladder (`career-ladder`)

Asked when there's no saved ladder, or T10 = "Use a different ladder".

| # | English | Português (Brasil) | Options | Default |
|---|---|---|---|---|
| L1 | "Do you have a career ladder for this role?" | "Você tem uma trilha de carreira para esse cargo?" | Paste the text · Share a link to a doc · Upload a file · No ladder, use the generic one / Colar o texto · Compartilhar o link de um documento · Enviar um arquivo · Sem trilha, usar a genérica | Generic |
| L2 | "Here's how I mapped it: {n} levels × {m} pillars ({pillar names}). Does this look right?" | "Mapeei assim: {n} níveis × {m} pilares ({nomes dos pilares}). Está certo?" | Looks right · Fix pillars · Fix levels / Está certo · Corrigir pilares · Corrigir níveis | Looks right |
| L3 | "I'll use a generic ladder with 4 pillars (Impact, Craft, Direction, Collaboration & Leadership). It's marked as generic so you can replace it at the next Career Check. OK?" | "Vou usar uma trilha genérica com 4 pilares (Impacto, Ofício, Direção, Colaboração e Liderança). Ela fica marcada como genérica para você trocar no próximo Check de Carreira. Pode ser?" | OK · Let me share a ladder instead / Pode · Prefiro compartilhar uma trilha | OK |

## E. Confirmation (nothing is created before "Create")

**English:**

> "I'm about to create **{doc_count} documents** for **{person_name}** ({role}, {discipline}, {level} → {next_level}) in **{platform}** › `{root_folder}/Career Hub — {person_name}`, in **{language}**, using the **{ladder_source}**. Docs: {doc_list}. Next 1:1: {next_meeting_date}."
>
> **"Create these documents?"** → Create · Change something · Cancel

**Português (Brasil):**

> "Vou criar **{doc_count} documentos** para **{person_name}** ({role}, {discipline}, {level} → {next_level}) em **{platform}** › `{root_folder}/Hub de Carreira — {person_name}`, em **{language}**, usando a **{ladder_source}**. Documentos: {doc_list}. Próximo 1:1: {next_meeting_date}."
>
> **"Posso criar estes documentos?"** → Criar · Mudar algo · Cancelar

## F. Edge cases

| # | English | Português (Brasil) | Options | Asked when |
|---|---|---|---|---|
| F2 | "A Career Hub already exists for {person_name}. What should I do?" | "Já existe um Hub de Carreira para {person_name}. O que faço?" | Add only the missing docs · Create a new hub next to it · Cancel / Adicionar só os documentos que faltam · Criar um novo hub ao lado · Cancelar | An existing hub is found — asked **before** E |
| F1 | "The Hub recommends a bi-weekly 1:1 to follow up on these documents. Want me to create a recurring event every two weeks starting {next_meeting_date}, with the Hub linked?" | "O Hub recomenda um 1:1 quinzenal para acompanhar estes documentos. Quer que eu crie um evento recorrente a cada duas semanas a partir de {next_meeting_date}, com o link do Hub?" | Yes, create it · No, I'll do it / Sim, pode criar · Não, eu faço | After creation, only if the agent has calendar tools |

## Question count

| Scenario | Questions |
|---|---|
| First run ever (setup + lead mode, nothing in the command) | 6 setup + up to 9 toolkit + 1–2 ladder + confirmation ≈ 17, in 5 batches |
| Typical run after setup (`/career-hub-toolkit Ana Souza, Data Scientist L3`) | T5, T6, T7, T8, T9 (+T10) + confirmation = 6–7, in 2 batches |
| Self mode after setup (`/career-hub-toolkit me`) | T4, T5, T6, T9 + confirmation = 5, in 2 batches |
