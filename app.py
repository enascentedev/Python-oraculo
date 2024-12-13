import tempfile
import os
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from loaders import *  
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Definição dos tipos de arquivos válidos para upload
TIPOS_ARQUIVOS_VALIDOS = [
    'Site', 'Youtube', 'Pdf', 'Csv', 'Txt'
]

# Configuração dos modelos disponíveis para o provedor OpenAI
CONFIG_MODELOS = {
    'OpenAI': {
        'modelos': ['gpt-4o-mini', 'gpt-4o', 'o1-preview', 'o1-mini'],  # Modelos atualizados conforme solicitado
        'chat': ChatOpenAI
    }
}

# Inicialização da memória de conversa
MEMORIA = ConversationBufferMemory()

def carrega_arquivos(tipo_arquivo, arquivo):
    """
    Carrega o conteúdo do arquivo ou URL fornecido pelo usuário.

    Args:
        tipo_arquivo (str): O tipo de arquivo a ser carregado.
        arquivo (str ou BytesIO): O arquivo ou URL fornecido pelo usuário.

    Returns:
        str: O conteúdo do documento carregado ou None em caso de erro.
    """
    try:
        if tipo_arquivo == 'Site':
            documento = carrega_site(arquivo)
        elif tipo_arquivo == 'Youtube':
            documento = carrega_youtube(arquivo)
        elif tipo_arquivo == 'Pdf':
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
                temp.write(arquivo.read())
                nome_temp = temp.name
            documento = carrega_pdf(nome_temp)
            os.remove(nome_temp)
        elif tipo_arquivo == 'Csv':
            with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
                temp.write(arquivo.read())
                nome_temp = temp.name
            documento = carrega_csv(nome_temp)
            os.remove(nome_temp)
        elif tipo_arquivo == 'Txt':
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
                temp.write(arquivo.read())
                nome_temp = temp.name
            documento = carrega_txt(nome_temp)
            os.remove(nome_temp)
        else:
            st.error('Tipo de arquivo inválido.')
            return None
        return documento
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):
    """
    Inicializa o modelo de linguagem com base no provedor e modelo selecionados.

    Args:
        provedor (str): O provedor de modelos (deve ser 'OpenAI').
        modelo (str): O modelo de linguagem selecionado.
        api_key (str): A chave API do OpenAI.
        tipo_arquivo (str): O tipo de arquivo fornecido pelo usuário.
        arquivo (str ou BytesIO): O arquivo ou URL fornecido pelo usuário.
    """
    # Validação do provedor
    if provedor != 'OpenAI':
        st.error('Provedor inválido selecionado.')
        return

    # Validação da chave API
    if not api_key:
        st.error('A chave API está vazia. Por favor, insira uma chave válida.')
        return

    # Log para depuração (exibindo apenas os primeiros caracteres da chave API por segurança)
    st.write(f'**Provedor selecionado:** {provedor}')
    st.write(f'**Modelo selecionado:** {modelo}')
    st.write(f'**API Key fornecida:** {api_key[:4]}****')  # Exibindo apenas os primeiros 4 caracteres

    # Carregamento do documento
    documento = carrega_arquivos(tipo_arquivo, arquivo)
    if documento is None:
        st.error("Falha ao carregar o documento.")
        return

    # Definição da mensagem do sistema para o modelo de linguagem
    system_message = f'''Você é um assistente amigável chamado Oráculo.
Você possui acesso às seguintes informações vindas 
de um documento {tipo_arquivo}: 

####
{documento}
####

Utilize as informações fornecidas para basear as suas respostas.

Sempre que houver $ na sua saída, substitua por S.

Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
sugira ao usuário carregar novamente o Oráculo!'''

    # Log para depuração
    st.write('**System Message:**', system_message)

    # Criação do template de prompt para o chat
    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    try:
        # Inicialização do cliente de chat do OpenAI com os modelos atualizados
        chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    except Exception as e:
        st.error(f'Erro ao inicializar o modelo: {e}')
        return

    # Log para depuração
    st.write('**Cliente de chat inicializado com sucesso.**')

    # Criação da cadeia de interação entre o template e o modelo de chat
    chain = template | chat

    # Armazenamento da cadeia na sessão do Streamlit
    st.session_state['chain'] = chain
    st.success('Oráculo inicializado com sucesso!')

def pagina_chat():
    """
    Renderiza a página principal de chat onde o usuário interage com o Oráculo.
    """
    st.header('🤖 Bem-vindo ao Oráculo')

    # Recupera a cadeia de chat da sessão
    chain = st.session_state.get('chain')
    if chain is None:
        st.error('Carregue o Oráculo antes de iniciar o chat.')
        st.stop()

    # Recupera a memória de conversa da sessão ou inicializa uma nova
    memoria = st.session_state.get('memoria', MEMORIA)

    # Exibe o histórico de mensagens na interface de chat
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    # Input para o usuário enviar mensagens
    input_usuario = st.chat_input('Fale com o Oráculo')
    if input_usuario:
        # Exibe a mensagem do usuário
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        # Prepara para exibir a resposta do Oráculo
        chat = st.chat_message('ai')
        try:
            # Envia a entrada do usuário e o histórico de chat para o modelo
            resposta = chat.write_stream(chain.stream({
                'input': input_usuario, 
                'chat_history': memoria.buffer_as_messages
            }))
        except Exception as e:
            st.error(f'Erro ao obter resposta do modelo: {e}')
            resposta = "Desculpe, ocorreu um erro ao processar sua solicitação."

        # Adiciona a mensagem do usuário e a resposta do Oráculo à memória de conversa
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

def sidebar():
    """
    Renderiza a barra lateral da aplicação com abas para upload de arquivos e configuração do modelo.
    """
    tabs = st.tabs(['Upload de Arquivos', 'Configuração do Modelo'])

    with tabs[0]:
        # Seção de upload de arquivos
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a URL do site')
        elif tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a URL do vídeo')
        elif tipo_arquivo == 'Pdf':
            arquivo = st.file_uploader('Faça o upload do arquivo PDF', type=['pdf'])
        elif tipo_arquivo == 'Csv':
            arquivo = st.file_uploader('Faça o upload do arquivo CSV', type=['csv'])
        elif tipo_arquivo == 'Txt':
            arquivo = st.file_uploader('Faça o upload do arquivo TXT', type=['txt'])

    with tabs[1]:
        # Seção de configuração do modelo
        provedor = 'OpenAI'  # Provedor fixo
        st.write(f'**Provedor selecionado:** {provedor}')
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
        api_key = OPENAI_API_KEY  # Utiliza a chave API definida no código
        st.write(f'**API Key fornecida:** {api_key[:4]}****')  # Exibindo apenas os primeiros 4 caracteres

    # Botão para inicializar o Oráculo
    if st.button('Inicializar Oráculo', use_container_width=True):
        # Validação dos inputs com base no tipo de arquivo
        if tipo_arquivo in ['Site', 'Youtube'] and not arquivo:
            st.error('Por favor, forneça a URL.')
        elif tipo_arquivo in ['Pdf', 'Csv', 'Txt'] and not arquivo:
            st.error('Por favor, faça o upload do arquivo.')
        elif not api_key:
            st.error('Por favor, insira a API key.')
        else:
            carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)

    # Botão para apagar o histórico de conversa
    if st.button('Apagar Histórico de Conversa', use_container_width=True):
        st.session_state['memoria'] = MEMORIA
        st.success('Histórico de conversa apagado com sucesso!')

def main():
    """
    Função principal que organiza a estrutura da aplicação Streamlit.
    """
    with st.sidebar:
        sidebar()
    pagina_chat()

if __name__ == '__main__':
    main()
