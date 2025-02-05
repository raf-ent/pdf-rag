# **PDF Q&A RAG**

This project is a **FastAPI-based** retrieval-augmented generator (RAG) service that allows users to upload PDFs, store their contents as embeddings in **Qdrant**, and query the stored data using **Cohere's embedding model**. It also integrates **Groq's LLM models** for answering questions based on the extracted content.

---

## **🚀 Features**
- 📄 **Upload PDFs** and split them into smaller text chunks  
- 🧠 **Embed text using Cohere's API** for efficient retrieval  
- 📌 **Store embeddings in Qdrant** for vector-based search  
- 🔍 **Query the stored data** to retrieve relevant document snippets  
- 🗣 **Answer questions** using Groq's LLM with relevant context  
- 🔄 **Stream responses in real-time** for an interactive experience  
- 🏗 **Memory support** to remember past queries  

---

## **🛠 Technologies Used**
- **FastAPI** (Backend API framework)
- **Qdrant** (Vector database for efficient search)
- **Cohere** (Embedding model for text processing)
- **Groq** (LLMs for question answering)
- **LangChain** (Text processing utilities)
- **Streamlit** (Frontend integration)

---

## **📦 Installation**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/raf-ent/pdf-rag.git
cd pdf-rag
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
Create a `.env` file in the root directory and add the following:
```sh
COHERE_API_KEY=your-cohere-api-key
GROQ_API_KEY=your-groq-api-key
QDRANT_API_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
PORT=8000
```

### **Alternative for Qdrant API**
Pull the Qdrant Docker Image
   ```
   docker pull qdrant/qdrant
   ```
   
Run the Qdrant Docker Container:
   ```
   docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
   ```

---

## **▶ Running the App**
### **1️⃣ Start the FastAPI Backend**
```sh
uvicorn main:app --reload
```

### **2️⃣ Start the Streamlit Frontend**
If you're using the Streamlit interface:
```sh
streamlit run client.py
```

---

## **📌 API Endpoints**
### **🔹 Upload a PDF**
```http
POST /upload/
```
- **Description:** Uploads a PDF file, extracts its text, splits it into chunks, generates embeddings using Cohere, and stores them in Qdrant.

**Request:**  
- `pdf_file` (Multipart file upload) 

**Response:**  
```json
{
  "embeddings": [[0.12, 0.43, ...], [0.56, -0.23, ...]]
}
```

---

### **🔹 Query the Stored Data**
```http
POST /query/
```
- **Description:** Accepts a query, retrieves relevant content from Qdrant based on the query embedding, fetches previous query history, and streams a response using the Groq language model.

**Request Body:**  
```json
{
  "collection_name": "document_name",
  "query": "What is the main topic of this document?"
}
```

**Response:** *(Streaming)*
```
The document discusses ...
```



---
