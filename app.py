import streamlit as st

image_address = "https://bs-uploads.toptal.io/blackfish-uploads/components/open_graph_image/8957316/og_image/optimized/0919_Machines_and_Trust_Lina_Social-ac9acf8ebc252ec57a9a9014f6be62b2.png"
st.title("Bias Reader")
st.image(image_address)
user_text = st.text_input("Please add your topic")