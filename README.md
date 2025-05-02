# ZenithGUI - Interface com Comunicação LoRa

## Andamento do projeto

### Captação de dados dos sensores

- [ ] Inserir tarefas
- [ ] ...

### Interface Gráfica

- [ ] Esboço de telas da aplicação
- [ ] ...

## Colaboração

Abaixo estão as instruções de como configurar o ambiente, instalar as dependências e colaborar com o projeto.

## Requisitos

Para garantir o uso do mesmo ambiente de desenvolvimento são utilizados **pyenv** e **Poetry**.

### 1. Como usar o **pyenv** no projeto

O **pyenv** é uma ferramenta que facilita o gerenciamento de versões do Python, permitindo que cada projeto use uma versão específica.

#### Passos para instalar e configurar o **pyenv**:

1. **Instalar o pyenv**:
   - No Linux ou macOS:
     ```bash
     curl https://pyenv.run | bash
     ```
   - No Windows, use o [pyenv-win](https://github.com/pyenv-win/pyenv-win).

2. **Instalar a versão do Python usada no projeto**:
   - O projeto utiliza uma versão específica do Python, que pode ser verificada no arquivo `pyproject.toml`. Para instalar a versão necessária:
     ```bash
     pyenv install <versão_do_python>
     ```

3. **Configurar o pyenv no diretório do projeto**:
   - Navegue até o diretório do projeto e defina a versão do Python:
     ```bash
     pyenv local <versão_do_python>
     ```
   Isso criará um arquivo `.python-version` no diretório do projeto, garantindo que todos os colaboradores utilizem a mesma versão.

### 2. Como usar o **Poetry** para gerenciar dependências

O **Poetry** é uma ferramenta para gerenciamento de pacotes e dependências no Python. Ele facilita o controle das bibliotecas e a criação do ambiente virtual.

#### Passos para instalar o **Poetry**:

1. **Instalar o Poetry**:
   - Execute o comando para instalar o Poetry:
     ```bash
     curl -sSL https://install.python-poetry.org | python3 -
     ```

2. **Instalar as dependências do projeto**:
   - No diretório raiz do projeto, execute o comando:
     ```bash
     poetry install
     ```
   Isso instalará todas as dependências listadas no `pyproject.toml`.

#### O que são o `pyproject.toml` e o `poetry.lock`?

- **`pyproject.toml`**: Este arquivo é usado pelo Poetry para definir as dependências do projeto e as configurações gerais. Você pode editar esse arquivo para adicionar novas dependências, como bibliotecas adicionais ou versões específicas.
  
- **`poetry.lock`**: Este arquivo contém a versão exata das dependências instaladas no ambiente. Ele garante que todos os colaboradores utilizem as mesmas versões das dependências, evitando inconsistências. **Não edite o `poetry.lock` manualmente**. Ele deve ser gerado automaticamente quando você adicionar ou remover pacotes usando o Poetry.

#### Como adicionar novas dependências:
Se você precisar adicionar uma nova dependência, use o comando:
```bash
poetry add <nome_da_dependência>
```

### 3. Como criar novos pacotes no projeto:

O projeto é estruturado de forma modular, e novos pacotes podem ser criados em diretórios específicos dentro de src/zenithgui.

Passos para criar novos pacotes:

1. **Escolher o diretório:**

Determine em qual módulo ou diretório o novo pacote será criado. Por exemplo, se o pacote for relacionado à comunicação LoRa, ele deve ser criado em src/zenithgui/communication.

2. **Criar o diretório e o arquivo ```bash __init__```.py:**

O arquivo ```bash __init__```.py transforma um diretório em um pacote Python. Crie esse arquivo para que o Python reconheça o diretório como um pacote.

Exemplo:

```bash
mkdir src/zenithgui/novopacote
touch src/zenithgui/novopacote/__init__.py
```

3. **Adicionar funcionalidades:**

Dentro do diretório do novo pacote, você pode adicionar arquivos Python que implementam a lógica desejada.

Exemplo de estrutura de pacotes:

```bash
src/zenithgui/
├── communication/
│   ├── __init__.py
│   └── lora_communication.py
├── controller/
├── __init__.py
└── main.py
```

4. **O que é o arquivo .env e como usá-lo**

O arquivo .env é usado para armazenar configurações e variáveis de ambiente. Nunca adicione informações sensíveis diretamente no código. O .env é especialmente útil para configurar parâmetros como portas de comunicação e níveis de log, sem precisar hardcodificar no código.

Como usar o arquivo .env:

1. **Criar um arquivo .env:**

O arquivo .env deve conter as variáveis de ambiente do projeto, com os valores específicos para o seu ambiente.

Um exemplo de .env está no diretório do projeto nomeado como ```bash .env-example```

2. **Como carregar as variáveis de ambiente:**

No código Python, use a biblioteca python-dotenv para carregar as variáveis do arquivo .env:

```bash
from dotenv import load_dotenv
import os

# Permitir leitura do .env
load_dotenv()

# Carregar variáveis do .env
LORA_PORT = os.getenv("LORA_PORT")
BAUDRATE = os.getenv("BAUDRATE")
```