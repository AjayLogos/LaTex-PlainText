
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import google.generativeai as genai
# from IPython.display import display, Image
# Configure the API key globally (set this once in your code)
genai.configure(api_key="AIzaSyCpFA-5JSPdKkykJAXGGdOSQ9AVVIpk-a4") 


# def convert_latex_to_html(latex_input):

#     # Escape the LaTeX input for HTML
#     escaped_latex = escape(latex_input)
#     # Create embeddable HTML code
#     html_output = f'<div style="font-size:1.5em;">$${escaped_latex}$$</div>'
#     return html_output

def convert_latex_to_text(latex_text):

    try:
        # Use the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate content from the LaTeX input
        prompt = f"Convert the following LaTeX text to plain  text:\n\n{latex_text}  without changing any content"
        response = model.generate_content(prompt)

        # Return the plain text from the response
        return response.text if hasattr(response, 'text') else "Error: No text generated from the model."

    except Exception as e:
        return f"Error: {e}"


def retrieve_question(question_id,data_src):
    # print("Data Source used :", data_src)
    data =pd.read_excel(data_src)
    df=pd.DataFrame(data)

    question_row = df[df['Doubt_id'] == question_id]
    question = question_row.iloc[0]['Question']
    soltuion = question_row.iloc[0]['Solution']

    if data_src == "rag_engine_2.0_flash_unseen_data_results_evaluated_processed.xlsx":
        llm_response = question_row.iloc[0]['RAG_Engine_with_Gemini_2.0_flash_response']
    else:
        llm_response = question_row.iloc[0]['RAG_Engine_with_Gemini_thinking_response']

    return question,soltuion, llm_response

def get_image_from_html(html_text):
    """Extracts the image from HTML and returns its binary content."""
    soup = BeautifulSoup(html_text, "html.parser")
    img_tag = soup.find("img")
    
    if img_tag and "src" in img_tag.attrs:
        img_url = img_tag["src"]
        # st.write(f"**Extracted Image URL:** {img_url}")  # Display URL in Streamlit
        response = requests.get(img_url, stream=True)
        
        if response.status_code == 200:
            return response.content  # Returns the image binary content
        else:
            # st.error("Failed to download image.")
            return None
    else:
        html_text = BeautifulSoup(html_text, "html.parser").get_text()
        st.header("Solution",divider='blue')
        st.write(html_text)
        return None

# def convert_latex_to_html2(latex_input):
#     # Clean and validate LaTeX input
#     if not latex_input.strip():
#         return "Invalid LaTeX input: empty string"

#     try:
#         # Ensure the LaTeX input is wrapped properly
#         if not latex_input.startswith("$$") and not latex_input.startswith("$"):
#             latex_input = f"$$ {latex_input} $$"
        
#         # Escape the LaTeX input for HTML
#         escaped_latex = escape(latex_input)

#         # Create embeddable HTML code
#         html_output = f'<div style="font-size:1.5em;">{escaped_latex}</div>'
#         return html_output

#     except Exception as e:
#         return f"Error processing LaTeX: {str(e)}"



def main():
    # Sidebar inputs
    st.sidebar.title("Input")
    # st.sidebar.write("Select the Data and Enter the question ID")
    
    option = st.sidebar.selectbox('which data to use?',
    ('rag_engine_2.0_flash_unseen_data_results_evaluated_processed.xlsx', 'rag_engine_thinking_mode_merged_prompt_new_data_eval_1_processed.xlsx'))

    # st.sidebar.write('You selected:', option)
    # Input: Question ID
    id_input = st.sidebar.text_input(
        "Enter Doubt ID:",
        placeholder="6130"
    )

    # Render button
    render_button = st.sidebar.button("Render")

    # Main area for output
    st.title("Render LaTeX in Plain Text")

    if render_button:
        if id_input.strip():
            # print("option : ", option)
            # Fetch the LaTeX expression based on the ID
            # question , latex_expression , options , solution = retrieve_question(id_input.strip())
            question , solution , latex_expression = retrieve_question(float(id_input),str(option))

            st.header("Question:",divider='blue')
            question = convert_latex_to_text(question)
            st.text(question)
            
            image_content = get_image_from_html(solution)

            if image_content:
                st.header("Solution",divider='blue')
                st.image(image_content, caption="Extracted Image", use_container_width=True)

            if latex_expression:
                st.header("LLM Response:",divider='blue')
                plain_text = convert_latex_to_text(latex_expression)
                st.text(plain_text)

            else:
                st.error("No LaTeX found for the given ID!")
        else:
            st.error("Please provide a valid Question ID!")

if __name__ == "__main__":
    main()


#%%
# import pandas as pd
# data = pd.read_csv('data.csv')
# df = pd.DataFrame(data)
# question_row = df[df['question_id'] == 'ILQ-892391']
# # %%
# print(question_row.iloc[0]['Agent_Builder_with_Gemini-1.5-pro_response'])
# %%
