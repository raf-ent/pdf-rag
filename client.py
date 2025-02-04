import streamlit as st
import requests

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"

def main():
    st.set_page_config(page_title="PDF QA Assistant", page_icon="📚")
    st.title("PDF QA Assistant")

    tab1, tab2 = st.tabs(["Upload PDF", "Ask Question"])

    with tab1:
        st.header("Upload PDF Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            with st.spinner("Processing PDF..."):
                sent_file = {"pdf_file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post(f"{BACKEND_URL}/upload/", files=sent_file)
                
                if response.status_code == 200:
                    st.success("PDF processed successfully!")
                    collection_name = uploaded_file.name.split(".")[0]
                    st.session_state.collection_name = collection_name
                    st.write(f"Collection name: `{collection_name}`")
                else:
                    st.error(f"Error processing PDF: {response.text}")

    with tab2:
        st.header("Ask Questions")
        
        collection_name = st.text_input(
            "Collection Name (from uploaded PDF)",
            value=st.session_state.get("collection_name", ""),
            help="This should be the PDF filename"
        )
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if question := st.chat_input("Ask a question about the PDF"):
            if not collection_name:
                st.error("Please enter a collection name first")
                return

            st.session_state.messages.append({"role": "user", "content": question})
            
            with st.chat_message("user"):
                st.markdown(question)

            payload = {
                "collection_name": collection_name,
                "query": question
            }

            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/query/",
                        json=payload,
                        stream=True
                    )
                    
                    if response.status_code == 200:
                        for chunk in response.iter_content(chunk_size=None):
                            if chunk:
                                full_response += chunk.decode("utf-8")
                                response_placeholder.markdown(full_response + "▌")
                        response_placeholder.markdown(full_response)
                    else:
                        st.error(f"Error: {response.text}")
                        full_response = "Sorry, I couldn't process your question."
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
                    full_response = "Unable to connect to the server."

            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()