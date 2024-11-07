import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage
from agent import app
import json

if 'name' not in st.session_state:
    st.session_state.name = ''
st.set_page_config(layout="wide")


if st.session_state.name == '':
    name_input_placeholder = st.empty()  # Create a placeholder for the name input
    button_placeholder = st.empty()      # Create a placeholder for the button

    with name_input_placeholder:
        name_input = st.text_input('Enter your Name:')

    with button_placeholder:
        submit_button = st.button('Submit')

    if submit_button and name_input:
        st.session_state.name = name_input
        name_input_placeholder.empty()   # Clear the name input box
        button_placeholder.empty() 

if st.session_state.name:
    # st.write(f"Welcome, {st.session_state.name}!")
    st.write(f"Welcome, sir!")

    input_text = st.text_input('Enter your Query:')
    start_button = st.button('Generate')

    if start_button and input_text:
        placeholder = st.empty()
        config = {"configurable": {"thread_id": st.session_state.name}}
        print(st.session_state.name)

        # converting user input to HumanMessage specific format
        inputs = {"messages": [HumanMessage(content=input_text)]}
        
        with st.spinner("Getting output"):
            # Getting output throught the app created
            for output in app.stream(inputs,config=config):
                for key, value in output.items():
                    print(f"Output from node '{key}':")
                    print("---")
                    if key=='agent':
                        if 'tool_calls' in value['messages'][0].additional_kwargs.keys():
                            with st.sidebar:
                                print(f"Tool Called: {value['messages'][0].additional_kwargs.get('tool_calls')[0].get('function')}")
                                # Printing tool called in a side window
                                func_detected = value['messages'][0].additional_kwargs.get('tool_calls')[0].get('function')
                                st.markdown(f"# Tool Called")
                                st.write({func_detected.get('name')})
                                st.markdown(f"## Parameters")
                                st.write({func_detected.get('arguments')})
                    print(value['messages'][0].content)
        if value['messages'][0].content:
            # Final output by LLM
            st.markdown(value['messages'][0].content)
        