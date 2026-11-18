# Uso manual — sem IA

Monte um Hub de Carreira completo à mão em **cerca de 20–30 minutos**, no Google Workspace ou no Microsoft 365. Com uma cópia-mestre, cada nova pessoa leva **cerca de 10 minutos**.

[English](MANUAL.md)

## 1. Baixe o Kit Manual

Na [Release](https://github.com/zeevolution/zeevolution-skills/releases) mais recente, baixe `career-management-kit-pt-BR.zip` e descompacte.

| Pasta | O que tem | Para quê |
|---|---|---|
| `markdown/` | Os templates em texto `.md` | Google Docs (colar ou importar), Notion, Confluence, Obsidian |
| `word/` | Os mesmos templates em `.docx` | Word / OneDrive / SharePoint, ou upload no Google Drive |
| `sheets/` | `05 - 🪜 Avaliação de Trilha.xlsx`, a planilha pronta | Excel ou Google Planilhas. **Nunca recrie a partir do texto.** |
| `START-HERE.pdf` | Uma página com estes passos | Todo mundo |

**Quais documentos copiar**

- **Sua própria carreira (modo pessoal):** 00 Hub de Carreira, 01 Notas de 1:1, 02 PDI **e** 04 Plano de Foco (copie os dois; escolha um depois), 03 Brag Document, 05 Avaliação de Trilha.
- **Alguém que você lidera (modo líder):** de 00 a 06. Inclua o **07 Documento de Evidências** só se um nível estiver em risco, e o **08 Plano de Onboarding** só para quem está chegando no time.

> O **PDI** e o **Plano de Foco** são alternativos: vocês vão usar um, não os dois. Os dois começam com um aviso explicando isso; escolham juntos no primeiro 1:1 ou Check de Carreira.

## 2. Caminho 1 — Google Workspace (Docs, Planilhas, Drive)

1. **Crie a pasta.** No Google Drive: **Novo › Nova pasta** → `Hub de Carreira — <Nome da pessoa>`. No modo líder, compartilhe só com a pessoa.
2. **Crie os documentos.** Escolha um jeito:
   - **Upload (mais rápido):** arraste todos os arquivos de `word/` para a pasta. Clique com o botão direito em cada um › **Abrir com › Documentos Google**, depois **Arquivo › Salvar como Documentos Google**, e apague o original. Dica: ative **Configurações › Converter uploads** no Drive e todo upload vira Documento Google automaticamente.
   - **Copiar e colar:** em qualquer Documento Google, ative **Ferramentas › Preferências › Ativar Markdown** (uma vez). Crie um documento em branco, abra o `.md` num editor de texto (ou no GitHub, botão **Raw**), copie tudo e, no documento, clique com o botão direito › **Colar do Markdown**. Renomeie o documento como o arquivo.
3. **Crie a Avaliação de Trilha.** Suba `sheets/05 - 🪜 Avaliação de Trilha.xlsx` e clique com o botão direito › **Abrir com › Planilhas Google** (ou deixe o Converter uploads fazer isso). Listas suspensas, fórmulas e cores vêm junto. Preencha **só as células amarelas**.
4. **Substitua os campos.** Em cada documento: **Editar › Localizar e substituir** (Ctrl/Cmd + Shift + H). Substitua: `{{person_name}}`, `{{leader_name}}`, `{{role}}`, `{{discipline}}`, `{{level}}`, `{{next_level}}`, `{{start_date}}`, `{{next_meeting_date}}`, `{{cycle}}`, `{{ladder_source}}`. No fim, procure `{{` para garantir que não sobrou nada (os `{{doc_link_…}}` são tratados no próximo passo).
5. **Ligue tudo pelo Hub.** Abra cada documento, **Compartilhar › Copiar link**, e coloque o link na linha dele na tabela de documentos do Hub (selecione o nome › Inserir link). Em cada documento, aponte o link **← Voltar ao Hub de Carreira** para o Hub.
6. **Escolha a trilha de carreira.** Tem a da empresa? Cole na aba **🪜 Trilha** da planilha (níveis na coluna A, pilares na linha 4) e marque **Trilha de carreira** como *Trilha da empresa* na aba Avaliação. Não tem? Mantenha a trilha genérica; o aviso lembra de revisar no próximo Check de Carreira.
7. **Marque o quinzenal.** No Google Agenda, crie um 1:1 recorrente **a cada 2 semanas** com o link do Hub na descrição, como recomenda o bloco no topo do Hub.

## 3. Caminho 2 — Microsoft 365 (Word, Excel, OneDrive / SharePoint)

1. **Crie a pasta.** No OneDrive ou SharePoint: **+ Adicionar novo › Pasta** → `Hub de Carreira — <Nome da pessoa>`. No modo líder, compartilhe só com a pessoa.
2. **Crie os documentos.** Suba todos os arquivos de `word/` (arrastar e soltar, ou **Carregar › Arquivos**). Eles abrem direto no Word para a web ou desktop; não precisa converter. Use os `.docx`, não os `.md`: o suporte a Markdown no Word ainda é parcial.
3. **Crie a Avaliação de Trilha.** Suba `sheets/05 - 🪜 Avaliação de Trilha.xlsx`. Abre no Excel com tudo funcionando. Preencha **só as células amarelas**.
4. **Substitua os campos.** Em cada documento: **Página Inicial › Substituir** (Ctrl + H, ou Cmd + Shift + H no Mac). Mesma lista do passo 4 do Google; depois procure `{{`.
5. **Ligue tudo pelo Hub.** No OneDrive, selecione cada arquivo › **Copiar link** e coloque na linha dele na tabela do Hub. Aponte o **← Voltar ao Hub de Carreira** de cada documento para o Hub.
6. **Escolha a trilha de carreira.** Igual ao passo 6 do Google, na aba **🪜 Trilha** do Excel.
7. **Marque o quinzenal.** No Outlook, crie um 1:1 recorrente **a cada 2 semanas** com o link do Hub no corpo.

## 4. Caminho 3 — Outras ferramentas (Notion, Confluence, Obsidian, arquivos)

Importe ou cole os `.md` direto; a maioria dessas ferramentas lê Markdown. Deixe o `.xlsx` num drive compartilhado com link no Hub. Os passos 4–7 são iguais.

## 5. Cópia-mestre reutilizável

1. Siga o Caminho 1 ou 2 uma vez **sem** substituir os campos. Nomeie a pasta `Hub de Carreira — MODELO`.
2. Para cada nova pessoa: **Google:** botão direito em cada arquivo › **Fazer uma cópia** na nova pasta. **Microsoft:** selecione os arquivos › **Copiar para** › a nova pasta.
3. Depois faça só os passos 4–7 — cerca de 10 minutos por pessoa.

## 6. Mantendo suas cópias atualizadas

Os templates melhoram com o tempo. O [CHANGELOG.md](../CHANGELOG.md) lista, por release, quais documentos mudaram e como, para você atualizar sua cópia-mestre à mão. Hubs já em uso nunca são afetados.

## 7. Depois que o hub existe

O **Hub de Carreira** é a página central. A cada duas semanas:

1. Abra o Hub e percorra a tabela de status.
2. Faça o 1:1 nas Notas de 1:1 (reflexão → feedback → ações).
3. Atualize um documento de desenvolvimento (o plano escolhido, o Brag ou a Avaliação de Trilha).
4. Atualize status e datas de "última revisão" no Hub.

Uma vez por trimestre, o primeiro quinzenal é o **Check de Carreira**. Uma vez por ciclo, revisem juntos a Avaliação de Trilha e a Avaliação de Desempenho.
