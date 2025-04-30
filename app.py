import uuid
import streamlit as st
from utils.crypto_funcs import rsa_keygen, encrypt, decrypt

st.title("🥷 Criptografía RSA")

if "private_key" not in st.session_state:
    st.session_state.private_key, st.session_state.public_key = rsa_keygen()

option = st.selectbox("¿Qué quieres hacer hoy?", ["Encriptar", "Desencriptar"])

# === ENCRIPTAR ===
if option == "Encriptar":
    uploaded_file = st.file_uploader("Sube un archivo .txt para encriptar", type="txt")

    if uploaded_file:
        text_2_encrypt = uploaded_file.read().decode('utf-8')
        encrypted_content = encrypt(text_2_encrypt, st.session_state.public_key)

        encrypted_content_str = ','.join(map(str, encrypted_content))
        st.session_state.encrypted_content = encrypted_content_str

        myuuid = uuid.uuid4()

        st.subheader("🔒 Texto encriptado:")
        st.download_button("Descargar texto encriptado", encrypted_content_str, f"encrypted_text_{myuuid}.txt")

        st.subheader("🔑 Clave privada:")
        st.download_button("Descargar clave privada", f"{st.session_state.private_key[0]},{st.session_state.private_key[1]}", f"private_key_{myuuid}.pem")


# === DESENCRIPTAR ===
elif option == "Desencriptar":
    st.subheader("🔒 Archivo Encriptado")
    uploaded_encrypted_file = st.file_uploader("Sube el archivo encriptado (.txt)", type="txt")

    st.subheader("🔑 Clave Privada")
    key_to_decrypt = st.file_uploader("Selecciona la clave privada (.pem)", type="pem")

    if uploaded_encrypted_file and key_to_decrypt:
        encrypted_content_str = uploaded_encrypted_file.read().decode('utf-8') 
        actual_key = key_to_decrypt.read().decode('utf-8') 

        encrypted_content = list(map(int, encrypted_content_str.split(',')))

        try:
            decrypted_content = decrypt(encrypted_content, (int(actual_key.split(',')[0]), int(actual_key.split(',')[1])))
            st.subheader("🤓 Texto desencriptado:")
            st.success(decrypted_content)

        except ValueError as e:
            st.error(f"Error al desencriptar: {str(e)}")
