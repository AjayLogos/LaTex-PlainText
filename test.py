import streamlit as st
from html import escape
import pandas as pd
import google.generativeai as genai
import xml.etree.ElementTree as ET

# Configure the API key globally (set this once in your code)
genai.configure(api_key="AIzaSyCpFA-5JSPdKkykJAXGGdOSQ9AVVIpk-a4") 


def convert_latex_to_html(latex_input):

    # Escape the LaTeX input for HTML
    escaped_latex = escape(latex_input)
    # Create embeddable HTML code
    html_output = f'<div style="font-size:1.5em;">$${escaped_latex}$$</div>'
    return html_output

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


def retrieve_question(question_id):
    data = pd.read_csv('data.csv')
    df = pd.DataFrame(data)
    question_row = df[df['question_id'] == question_id]
    question = question_row.iloc[0]['transformed_question']
    llm_response = question_row.iloc[0]['Agent_Builder_with_Gemini-1.5-pro_response']
    options = question_row.iloc[0]['options']
    solution = question_row.iloc[0]['transformed_solution']
    return question, llm_response ,options , solution

def convert_latex_to_html2(latex_input):
    # Clean and validate LaTeX input
    if not latex_input.strip():
        return "Invalid LaTeX input: empty string"

    try:
        # Ensure the LaTeX input is wrapped properly
        if not latex_input.startswith("$$") and not latex_input.startswith("$"):
            latex_input = f"$$ {latex_input} $$"
        
        # Escape the LaTeX input for HTML
        escaped_latex = escape(latex_input)

        # Create embeddable HTML code
        html_output = f'<div style="font-size:1.5em;">{escaped_latex}</div>'
        return html_output

    except Exception as e:
        return f"Error processing LaTeX: {str(e)}"



def main():
    # Sidebar inputs
    st.sidebar.title("Input")
    st.sidebar.write("Enter the question ID and select the method:")
    
    # Input: Question ID
    id_input = st.sidebar.text_input(
        "Enter Question ID:",
        placeholder="ILQ-6130"
    )

    # Render button
    render_button = st.sidebar.button("Render")

    # Main area for output
    st.title("Render LaTeX in Plain Text")

    if render_button:
        if id_input.strip():
            # Fetch the LaTeX expression based on the ID
            question , latex_expression , options , solution = retrieve_question(id_input.strip())

            st.header("Question:")
            question = convert_latex_to_text(question)
            st.text(question)

            st.header("Options:")
            options = convert_latex_to_text(options)
            st.text(options)

            st.header("Solution:")
            solution = convert_latex_to_text(solution)
            st.text(solution)
              
            if latex_expression:
                st.header("LLM Response:")
                plain_text = convert_latex_to_text(latex_expression)
                st.text(plain_text)

            else:
                st.error("No LaTeX found for the given ID!")
        else:
            st.error("Please provide a valid Question ID!")

if __name__ == "__main__":
    main()