import streamlit as st

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Modulo di Feedback</h1>", unsafe_allow_html=True)

with st.form("Feedback_form"):
    st.write("Compile to send your feedback:")
    name = st.text_input("Your name is:")
    rating = st.slider("Satisfaction Level (1 = Completely not, 5 = Fully satisfied):", min_value=1, max_value=5, value=3)
    comments = st.text_area("Other Comments")
    submit_button = st.form_submit_button("Send Feedback")

if submit_button:
    if not name.strip():
        st.error("Error: Insert your Name")
    else:
        st.write("Your Feedback")
        st.write(f"Name: {name}")
        st.write(f"Rating: {rating}/5")
        st.write(f"Comments: {comments if comments.strip() else 'No comments delivered'}")
        
        if rating <= 2:
            st.warning("We are Bad")
        elif rating >= 4:
            st.success("Vamos!")
        else:
            st.info("Senza infamia e senza lodi")