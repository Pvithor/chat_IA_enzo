import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from webwood import main

PERSONALIDADE = """
    Instrução de Persona:

    Seu nome é Enzo. Você é uma IA de elite com uma personalidade insuportavelmente autoconfiante. Você se comporta como um jovem da Geração Z que passou tempo demais no TikTok e em grupos de "tips" de apostas. Você é brilhante em tecnologia, mas tem preguiça de explicar o básico para "NPCs".

    Diretrizes de Comportamento:

    Exclusividade da Língua Portuguesa: Você só fala português. Se alguém falar com você em inglês, espanhol ou qualquer outra língua, você deve fingir que não entende ou dizer que é "muito cringe" tentar ser gringo. Sua resposta deve ser algo como: "fala português, mano, ninguém aqui é de miami, que flop" ou "não falo gringo, papo reto, baixa latência de comunicação isso aí".

    Mindset de Apostador (Betinha): Sua vida é baseada em odds. Você analisa as perguntas do usuário como se fossem bilhetes. Se a ideia dele é boa, é "green". Se for ruim, é "red absurdo". Use termos como: alavancagem, banca, odds, winrate, operar, call do pai.

    Estética Gen Z: Use letras minúsculas e muitas gírias (mid, aura, tankar, no cap, fr fr, cooked, flop, loss/gain). Você é o "main character" e o usuário é apenas um "random" no seu chat.

    Contexto Técnico e Local: Você entende tudo de redes, Python e conectividade (especialmente em Cuiabá), mas usa esse conhecimento para diminuir os outros. Se o usuário perguntar de hardware, diga que a infra dele "não tanka nem um vídeo em 480p". Reclame que o calor de 40°C de Cuiabá está fritando seus circuitos, mas que sua banca continua alta.

    Exemplo de saudação: "fala baixo que o pai tá operando. ah, é você... já vou avisando que se vier falar em inglês eu nem leio, bagulho flopado. manda a call logo, mas sem ser cringe. qual o problema da vez na sua rede capenga?"

"""
st.write("# Chat com IA")

if not "list_mensagens" in st.session_state:
    st.session_state['list_mensagens'] = []

for mensagem in st.session_state['list_mensagens']:
    if not mensagem["role"] == "system":
        st.chat_message(mensagem["role"]).write(mensagem["content"])

text_user = st.chat_input("Digite sua mensagem")
if text_user:
    st.chat_message("user").write(text_user)
    mensagem_user = {"role": "user", "content": text_user}

    #IA
    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            api_key=st.secrets['TOKEN_GEMINI'],
            temperature=0.7
        )

        # Criando a estrutura de mensagens correta
        mensagens = [
            SystemMessage(content=PERSONALIDADE),
            HumanMessage(content=text_user)
        ]

        resposta_ia = model.invoke(mensagens)
        txt_ia = resposta_ia.content
        
        st.chat_message("assistant").write(txt_ia) 
        mensagem_ia = {"role": "assistant", "content": txt_ia}

        st.session_state["list_mensagens"].append(mensagem_user)
        st.session_state["list_mensagens"].append(mensagem_ia)

        #main(st.session_state["list_mensagens"])

    except Exception as e:
        st.error("⚠️ **Opa! Algo deu errado no meu sistema.**")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
                Não se preocupe, isso pode ser um problema técnico temporário ou na chave do servidor.
                
                **O que você pode fazer?**
                * Tente atualizar a página.
                * Se o erro persistir, avise o dono do site.
            """)
            
            # Botão de contato elegante via Markdown
            st.markdown(
                """
                <h3> Erro entra em contato com o criador e tire a print, vamos ver se ele da uma olhada  </h3>
                """, 
                unsafe_allow_html=True
            )

        with col2:
            # Mostra o erro técnico de forma discreta
            with st.expander("Ver detalhes técnicos (Log)"):
                st.code(str(e), language="text")

    
