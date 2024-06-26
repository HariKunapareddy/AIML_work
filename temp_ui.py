import streamlit as st
import streamlit.components.v1 as components

# Set the page configuration
st.set_page_config(page_title="Telecom", layout="wide")

# CSS for background image and styling
background_image_url = "https://as2.ftcdn.net/v2/jpg/04/35/60/39/1000_F_435603999_qcRMI77UVgIk64kpL4y1cF6AtKZvX5PE.jpg"  # Replace with your image URL
st.markdown(f"""
    <style>
        .main {{
            background: url({background_image_url});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .header {{
            font-size: 2.5em;
            font-weight: bold;
            color: #FF6200;
        }}
        .subheader {{
            font-size: 1.5em;
            color: #fff;
        }}
        .button {{
            background-color: #00D8B6;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            font-size: 1em;
        }}
        .button:hover {{
            background-color: #00B89C;
        }}
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <div class='header'>Growth starts here</div>
        <div class='subheader'>Designed to deliver the most user-friendly, intuitive and productive technology environments</div>
        <button class='button' onclick="window.location.href='#'">VIEW SOLUTIONS</button>
    </div>
""", unsafe_allow_html=True)

# Add more content as needed
st.markdown("### Additional Content")
st.write("Here you can add more sections or information about your solutions, products, and services.")

# For example, using columns for additional information
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Solution 1")
    st.write("Description of solution 1.")

with col2:
    st.header("Solution 2")
    st.write("Description of solution 2.")

with col3:
    st.header("Solution 3")
    st.write("Description of solution 3.")



components.html("""
<style>
  df-messenger {
    z-index: 999;
    position: fixed;
    --df-messenger-font-color: #000;
    --df-messenger-font-family: Google Sans;
    --df-messenger-chat-background: #f3f6fc;
    --df-messenger-message-user-background: #d3e3fd;
    --df-messenger-message-bot-background: #fff;
    bottom: 16px;
    right: 16px;
  }
</style>
""",height=400)
