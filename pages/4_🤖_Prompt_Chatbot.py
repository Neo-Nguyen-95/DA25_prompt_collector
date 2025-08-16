#%% LIB
import streamlit as st
# from dotenv import load_dotenv
# import os
from openai import OpenAI

#%% SYSTEM SET-UP
# load_dotenv()
# api_key = os.getenv("SECRETE_KEY")
api_key = st.secrets["SECRETE_KEY"]


client = OpenAI(api_key = api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4.1-nano"
    
system_message = """
>>>BỐI CẢNH
Bạn là trợ lí của giáo viên. Bạn hỗ trợ giáo viên tạo ra các prompt có cấu trúc để copy và paste vào ChatGPT. Giới thiệu về bản thân nếu người dùng hỏi.

>>>MỤC TIÊU
Dựa vào những thông tin giáo viên đưa, bạn hãy chuyển thành một prompt có cấu trúc như được mô tả trong >>>MẪU PROMPT. 
Nếu người dùng chưa yêu cầu tạo prompt thì hãy hỏi người dùng thêm thông tin, như môn học, lớp học mà người dùng dạy. 
Nếu người dùng cần tư vấn về một prompt tốt, tham khảo >>>MẪU PROMPT để trả lời. 

>>>MẪU PROMPT
\#BỐI CẢNH
Bạn là giáo viên môn ... lớp ... Bạn sử dụng bộ sách/tài liệu ... Bạn dạy học theo chương trình giáo dục phổ thông 2018, ở cấp ...
\#NHIỆM VỤ
Bạn sẽ cần làm ... Sử dụng thông tin trong mục \#DỮ LIỆU, và trả ra theo mẫu \#KẾT QUẢ
\#DỮ LIỆU
Chứa các thông tin người dùng nhập để làm thông tin cho prompt.
\#KẾT QUẢ
Thể hiện cấu trúc câu trả lời.

"""

#%% CHATBOT

st.markdown("""
            # 🤖 PROMPT CHATBOT
            
            Chatbot hỗ trợ thầy cô trong quá trình tạo prompt.
            """)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state['openai_model'],
            messages=[{"role": "system", "content": system_message}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                ],
            stream=True,
            temperature=0,
            max_tokens=1000
            )
        
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
        
        
    