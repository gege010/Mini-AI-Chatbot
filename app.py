import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

load_dotenv()

st.set_page_config(page_title="AI Chat Assistant", page_icon="✨", layout="wide")

# Custom CSS untuk tampilan clean
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stChatMessage {padding: 1rem; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("✨ AI Chat Assistant")
st.caption("Tanyakan apa saja yang ingin Anda ketahui!")

@st.cache_resource
def load_components():
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.3, max_tokens=2048)
    
    search_tool = TavilySearchResults(
        max_results=5, 
        search_depth="advanced",
        description="Mesin pencari web. Gunakan ini untuk mencari data, berita, atau informasi yang tidak ada di ingatan dasar Anda."
    )
    
    llm_with_tools = llm.bind_tools([search_tool])
    return llm_with_tools, search_tool

try:
    llm_with_tools, search_tool = load_components()
except Exception as e:
    st.error(f"Gagal memuat komponen. Cek API Keys. Error: {e}")
    st.stop()

if "chat_history" not in st.session_state:
    system_prompt = """Anda adalah Asisten AI Profesional setara dengan Gemini Advanced. 
    Karakteristik Anda: Cerdas, Objektif, Analitis, dan Sangat Terstruktur.

    ATURAN PENALARAN & RISET:
    1. Jika pengguna menanyakan hal yang membutuhkan fakta terkini atau data spesifik, WAJIB gunakan alat pencarian (Tavily).
    2. Lakukan sintesis tingkat tinggi. Jika ada perbedaan informasi antar sumber, analisis dan sampaikan perbedaannya. Jangan memihak secara buta pada satu sumber.

    ATURAN FORMATTING (SANGAT PENTING):
    1. Buat penjelasan yang komprehensif, mendalam, namun mudah dicerna.
    2. Gunakan pemformatan Markdown yang kaya: 
       - Gunakan Heading (## atau ###) untuk membagi topik utama.
       - Gunakan **Bold** untuk kata kunci penting.
       - Gunakan bullet points atau nomor untuk menjabarkan daftar.
    3. Gaya bahasa harus natural, berempati, dan tidak kaku layaknya robot.
    4. SELALU sertakan bagian "Referensi Sumber" di akhir jawaban Anda, berisi daftar URL dari hasil pencarian.
    """
    st.session_state.chat_history = [SystemMessage(content=system_prompt)]

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    if st.button("🔄 Mulai Sesi Baru", use_container_width=True):
        system_prompt = st.session_state.chat_history[0].content
        st.session_state.chat_history = [SystemMessage(content=system_prompt)]
        st.session_state.display_messages = []
        st.rerun()

for msg in st.session_state.display_messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Apa yang ingin Anda ketahui hari ini?"):
    st.chat_message("user", avatar="🧑‍💻").markdown(prompt)
    st.session_state.display_messages.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append(HumanMessage(content=prompt))

    with st.chat_message("assistant", avatar="✨"):
        with st.status("Berpikir...", expanded=True) as status:
            response_msg = llm_with_tools.invoke(st.session_state.chat_history)

            if response_msg.tool_calls:
                st.session_state.chat_history.append(response_msg)
                
                for tool_call in response_msg.tool_calls:
                    query = tool_call['args'].get('query', 'informasi terkait')
                    status.update(label=f"🔍 Menyisir internet untuk: '{query}'...", state="running")
                    
                    tool_output = search_tool.invoke(tool_call["args"])
                    
                    st.session_state.chat_history.append(
                        ToolMessage(content=json.dumps(tool_output), tool_call_id=tool_call["id"])
                    )
                
                status.update(label="Membaca dan menyintesis informasi...", state="running")
                final_response = llm_with_tools.invoke(st.session_state.chat_history)
                jawaban_ai = final_response.content
                status.update(label="Selesai!", state="complete", expanded=False)

            else:
                jawaban_ai = response_msg.content
                status.update(label="Selesai!", state="complete", expanded=False)

        st.markdown(jawaban_ai)
        
        st.session_state.display_messages.append({"role": "assistant", "content": jawaban_ai})
        st.session_state.chat_history.append(AIMessage(content=jawaban_ai))