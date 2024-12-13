# Oráculo

fonte de sabedoria ou conhecimento profundo

## Visão Geral

O Oráculo é uma aplicação interativa que permite interagir com uma variedade de fontes de dados, incluindo vídeos do YouTube, arquivos CSV, PDFs e TXT, tudo por meio de uma interface de conversação. O projeto oferece flexibilidade ao permitir a escolha entre diferentes provedores de modelos de linguagem, como  a'gpt-4o-mini', 'gpt-4o', 'o1-preview', 'o1-mini' todos da OpenAI (pago), oferecendo a liberdade de personalizar a experiência de conversa conforme as necessidades do usuário.

## Funcionalidades

O Oráculo é uma aplicação interativa que permite a interação com diversas fontes de dados, como vídeos do YouTube, arquivos CSV, PDFs e TXT, tudo por meio de uma interface de conversação. O projeto oferece flexibilidade ao permitir a escolha entre diferentes modelos de linguagem da OpenAI, como gpt-4o-mini, gpt-4o, o1-preview e o1-mini, oferecendo a liberdade de personalizar a experiência de conversa conforme as necessidades do usuário.

As principais funcionalidades incluem:

Interação com Diversas Fontes de Dados: O Oráculo permite que o usuário interaja com dados provenientes de fontes como vídeos do YouTube, arquivos CSV, PDFs e TXT. A aplicação facilita a consulta e extração de informações dessas fontes, transformando dados estáticos em interações dinâmicas e úteis.

Escolha de Modelos de Linguagem: O projeto oferece flexibilidade ao permitir a escolha entre diversos modelos de linguagem pagos da OpenAI. Os modelos disponíveis incluem:

gpt-4o-mini
gpt-4o
o1-preview
o1-mini
Essa funcionalidade oferece liberdade para personalizar a IA de acordo com a necessidade de cada usuário, seja para responder de forma mais específica ou adaptar-se ao tipo de dado com o qual está interagindo.

Personalização da Experiência de Conversação: O Oráculo permite a personalização da IA, adaptando as respostas e o comportamento com base no modelo de linguagem selecionado. O usuário pode ajustar o modelo conforme o tipo de dados carregados e o contexto da conversa, garantindo uma experiência única e eficaz.

Interface de Conversação Intuitiva: Desenvolvido com Streamlit, a interface é amigável e de fácil navegação, permitindo que o usuário carregue arquivos, escolha modelos de linguagem e interaja com os dados de forma fluida e sem complicação.

Execução Local e Privacidade: Toda a aplicação roda localmente na máquina do usuário, garantindo que os dados carregados (sejam arquivos ou links de vídeos) não sejam expostos a servidores externos. O processo de consulta e interação com os dados acontece de maneira privada, sem necessidade de enviar ou armazenar dados fora do ambiente local.

Essas funcionalidades tornam o Oráculo uma ferramenta poderosa para explorar dados de maneira interativa, enquanto garante a segurança e privacidade dos dados manipulados, com a flexibilidade de utilizar diferentes modelos de linguagem de forma local e sem expor informações sensíveis.

## Vídeo Demonstrativo

<div align="center">
  <img src="./public/chatGpt-1.gif" alt="Demonstração do Projeto" width="600">
</div>

## Tecnologias Empregadas

**Backend:**
LangChain: Um conjunto de ferramentas que facilita a construção de pipelines de processamento de linguagem natural (NLP). Especificamente, foram usadas as seguintes bibliotecas do LangChain:

ConversationBufferMemory: Para gerenciar o histórico de conversação, mantendo o contexto ao longo das interações.
ChatOpenAI: Para integrar modelos de linguagem da OpenAI, permitindo a comunicação entre o usuário e a IA.
ChatPromptTemplate: Para estruturar as prompts usadas no modelo de linguagem, tornando as respostas mais direcionadas e úteis.
Loaders: Utilizado para carregar e processar diferentes tipos de arquivos, como CSV, PDFs, TXT e YouTube, permitindo que o sistema extraia informações de diversas fontes.

dotenv: Usado para carregar variáveis de ambiente, ajudando na configuração de chaves de API e credenciais de forma segura, sem a necessidade de expô-las no código-fonte.

tempfile e os: Bibliotecas padrão do Python, utilizadas para manipulação de arquivos temporários e gerenciamento de caminhos de diretórios, respectivamente.

**Frontend:**

Streamlit: Utilizado para criar a interface do usuário (UI) do Oráculo, proporcionando uma forma simples e interativa para o usuário carregar arquivos, selecionar modelos de linguagem e interagir com o sistema. O Streamlit é um framework que facilita a criação de web apps rápidos e eficientes para dados e machine learning.

## RODAR PROJETO

Deve ser criada uma chave da openIA (paga, tenho uma desdo ano passado paguei 5 dólares e uso até hj :D)
no meu projeto criei uma variável de ambiente no meu computador com o conteúdo da chave , esse conteudo não pode ser exposto no GitHub pois se vazar a openIA bloqueia a chave ( já passei por isso pra aprender kkkk)

# Criação do ambiente virtual

python3 -m venv desenvolvimento

# Ativação do ambiente virtual no bash

source desenvolvimento/Scripts/activate

## Instalando bibliotecas do projeto

pip install -r requirements.txt

## RODAR PROJETO LOCAL

streamlit run app.py
