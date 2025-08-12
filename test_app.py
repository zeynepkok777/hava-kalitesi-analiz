import streamlit as st

st.title("Test Uygulaması")
st.write("Bu bir test uygulamasıdır.")
st.write("Eğer bu sayfayı görüyorsanız, Streamlit çalışıyor demektir!")

# Basit bir slider
x = st.slider("Bir sayı seçin", 0, 100, 50)
st.write(f"Seçtiğiniz sayı: {x}")
