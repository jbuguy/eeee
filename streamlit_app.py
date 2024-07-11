import streamlit as st
from huggingface_hub import InferenceClient
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer,pipeline

# Check if CUDA (GPU support) is available
gpu_available = torch.cuda.is_available()

# Print the result
if gpu_available:
    print("CUDA (GPU) is available!")
else:
    print("CUDA (GPU) is not available.")
# Show title and description.
st.title("💬 AI MEHERZYA")
st.write(
    "Ce simple chatbot  utilise le modèle mistralai/Mixtral-8x7B-Instruct-v0.1 pour générer des réponses. "
    "C'est la Démo du projet. "
    "Vous ne pouvez poser que des questions sur l'algèbre 1."
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
client = InferenceClient(model="jbugguys/test-teacher")

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Posez votre question ici?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    text_completion = pipeline("text-generation", model="jbugguys/test-teacher")
    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    # Generating completions using the pipeline
    stream = text_completion(messages)
    

    # Display and store assistant's response
    st.session_state.messages.append({"role": "assistant", "content": generated_text})
    with st.chat_message("assistant"):
        st.markdown(generated_text)
