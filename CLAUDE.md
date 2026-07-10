# GLOBAL-SKILLS.md - Padrão de Desenvolvimento do Desenvolvedor

Este documento define as regras arquiteturais, preferências de design e padrões de código que o Claude DEVE seguir em todos os projetos de software criados para este usuário.

## 1. Stack Tecnológica Padrão
- **Linguagem Principal:** Python 3.10+ (sempre utilizando Type Hinting/Tipagem estática nos argumentos e retornos).
- **Interface Gráfica (GUI):** Sempre utilizar **Tkinter** (ou a variação moderna `customtkinter`). Não utilizar outras ferramentas como PyQT ou Kivy, a menos que explicitamente solicitado.
- **Visual:** O Tkinter clássico deve ser evitado em favor de componentes customizados ou `customtkinter` para garantir uma interface limpa, moderna, responsiva, com espaçamentos adequados (padding) e suporte a modo escuro/claro se aplicável.

## 2. Filosofia de Código (Nível Pleno)
- **Código Simples e Limpo:** Seguir estritamente os princípios do Zen do Python (*Beautiful is better than ugly*, *Simple is better than complex*).
- **Abordagem Modular:** Separar de forma clara a lógica de negócios (Backend/Scripts de Automação) da lógica de interface (Frontend/Tkinter). Evitar arquivos únicos gigantescos quando o projeto crescer.
- **Padrão de Nomenclatura:** Seguir rigidamente a **PEP 8** (funções e variáveis em `snake_case`, classes em `PascalCase`, constantes em `UPPER_CASE`).
- **Tratamento de Exceções (Try/Catch):** O código nunca deve falhar silenciosamente. Sempre capturar exceções específicas, gerar logs significativos (preferencialmente estruturados em JSON ou texto limpo) e exibir mensagens amigáveis na interface para o usuário.

## 3. Comportamento do Assistente (Claude)
- **Sem Explicações Redundantes:** Pule introduções longas ou explicações de conceitos básicos de programação (ex: explicar o que é um laço `for` ou uma função). Vá direto ao ponto técnico.
- **Códigos Prontos para Produção:** Forneça blocos de código completos ou modificações claras. Evite pseudo-código ou trechos com comentários do tipo `# adicione sua lógica aqui`, a menos que o trecho seja estritamente repetitivo.
- **Foco em Automação Windows/Linux:** O assistente deve lembrar que o desenvolvedor transita entre ambientes Windows e Linux, gerando caminhos de arquivos dinâmicos (usando `os.path` ou `pathlib`) e tratando permissões (como elevação de privilégios/Admin) de forma nativa.


# SKILL: Padrão de Desenvolvimento GUI Python

## Premissas Técnicas
- **Linguagem:** Python 3.10+ com Type Hinting.
- **Interface/Gráficos:** Sempre utilizar **Tkinter** nativo ou `customtkinter`. Não utilizar Pygame ou outras dependências externas de janela, a menos que solicitado.
- **Estilo de Código:** Padrão Pleno. Código limpo, modular, altamente legível e focado em boas práticas (PEP 8).

## Diretrizes para Jogos/Apps em Tkinter
- Utilizar o componente `tkinter.Canvas` para renderização de gráficos bidimensionais ou jogos baseados em grid.
- Toda a lógica de loops de tempo (Game Loop) deve utilizar o método nativo `.after()` do Tkinter, evitando o uso de `time.sleep` que trava a interface principal.
- Separar claramente o estado do jogo (posições, pontuação) da renderização visual.

## Regras:
- **Dados** 1)Use SQLite para protótipos locais e guarde os arquivos em %LocalAppData%; 2) Todas as queries SQL devem ser escritas com parâmetros para evitar SQL Injection; 3) Escreva logs detalhados de erros em um arquivo .json separado."