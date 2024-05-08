from openai import OpenAI
import streamlit as st
import time


assistant_id = "your_assistant_id"
thread_id = "your_thread_id"
client = OpenAI(api_key="your_api_key")


st.title("💬 노무사Chatbot")
st.caption("by 김대훈")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와 드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )


    print(message)

    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
    )

    print(run)
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == 'completed': 

            break
        else:
            time.sleep(2)



    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    print(messages.data)

    msg = messages.data[0].content[0].text.value
    print(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


    

