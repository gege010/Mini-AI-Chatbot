# ✨ AI Chat Assistant

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Langchain](https://img.shields.io/badge/Langchain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3-F55036)

Sebuah aplikasi chatbot interaktif yang dilengkapi dengan kemampuan pencarian web secara *real-time*. Berbeda dengan chatbot statis biasa, asisten ini dapat terhubung ke internet untuk mencari informasi terkini ketika pengguna menanyakan tentang fakta atau berita terbaru, sehingga memberikan jawaban yang lebih akurat dan relevan.

## 🚀 Fitur Utama
* **Pencarian Web Dinamis (Tool Calling):** AI secara otomatis memutuskan kapan harus mencari informasi di internet (via Tavily API) dan kapan cukup menjawab dari pengetahuan dasarnya.
* **Memori Percakapan:** Aplikasi ini melacak riwayat obrolan pengguna, memungkinkan percakapan lanjutan yang natural tanpa kehilangan konteks.
* **Optimasi Penggunaan API:** Dikonfigurasi agar membatasi jumlah penarikan data dari web untuk menjaga efisiensi token dan mencegah limitasi API (*rate limits*).
* **Antarmuka Minimalis:** Tampilan obrolan yang bersih dan responsif dibangun menggunakan Streamlit, dengan dukungan format teks (Markdown) yang rapi untuk membaca hasil pencarian.

## 🛠️ Tech Stack
* **LLM Engine:** Llama-3.3-70b-versatile via [Groq API](https://groq.com/) untuk respons generasi teks yang sangat cepat.
* **Orkestrasi:** [Langchain Core](https://python.langchain.com/) (Menggunakan fitur `.bind_tools()`).
* **Web Search:** [Tavily Search API](https://tavily.com/) yang dioptimalkan untuk menyuplai konteks ke LLM.
* **Frontend:** [Streamlit](https://streamlit.io/).

## 💻 Panduan Instalasi (Local Development)

**1. Clone Repositori**
```bash
git clone [https://github.com/USERNAME_GITHUB_ANDA/nama-repo-anda.git](https://github.com/USERNAME_GITHUB_ANDA/nama-repo-anda.git)
cd nama-repo-anda

```

**2. Buat Virtual Environment**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

```

**3. Instal Dependensi**

```bash
pip install -r requirements.txt

```

**4. Konfigurasi API Keys**
Buat file `.env` di *root directory* proyek dan tambahkan API Keys Anda:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
TAVILY_API_KEY=tvly_your_tavily_api_key_here

```

**5. Jalankan Aplikasi**

```bash
streamlit run app.py

```

## 🧠 Tentang Proyek Ini

Proyek ini dikembangkan sebagai bentuk implementasi dari integrasi alat bantu pihak ketiga (*Tool Calling*) pada Large Language Models (LLM). Fokus utamanya adalah membangun asisten virtual yang fungsional dan responsif, sekaligus mengatasi tantangan nyata dalam pengembangan aplikasi AI seperti manajemen memori sesi dan efisiensi konsumsi token.

---

