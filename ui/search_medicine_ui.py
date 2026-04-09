import streamlit as st

def search_medicine_page():
    st.title("Indian Medicine Search")

    med_name = st.text_input("Enter medicine name (e.g., Dolo 650, Paracetamol):")

    if st.button("Search"):
        if not med_name.strip():
            st.warning("Please enter a medicine name.")
        else:
            netmeds_url = f"https://www.netmeds.com/catalogsearch/result/{med_name.replace(' ', '%20')}"
            
            # Redirect using HTML
            st.markdown(
                f"""
                <meta http-equiv="refresh" content="0; url={netmeds_url}">
                """,
                unsafe_allow_html=True
            )

            st.success("Redirecting to Netmeds...")