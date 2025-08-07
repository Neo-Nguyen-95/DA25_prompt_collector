#%% LIB
import streamlit as st
from data import SQLRepository
import os
import sqlite3
from pathlib import Path

#%% DATA

BASE_DIR = Path(__file__).resolve().parent.parent  # Access base dir in streamlit
database_name = str(list(BASE_DIR.glob('*.db'))[0])

connection = sqlite3.connect(
    database=database_name,
    check_same_thread=False
    )
repo = SQLRepository(connection)

#%% APP
st.markdown("""
# PROMPT TOOL

Thầy cô nhập các thông tin theo từng bước bên dưới.

--- 
""")

    #%%% USER INPUT
col1, col2 = st.columns(2)
with col1:
    #----------------------------------------------------------
    st.markdown("""
    ### I. BỐI CẢNH
                """)
    subject = st.selectbox(
        "Chọn môn học", 
        repo.get_subject_list()
        )
    grade = st.selectbox(
        "Chọn lớp", 
        repo.get_grade_list()
        )
    book = st.selectbox(
        "Chọn bộ sách",
        repo.get_author_list()
        )
    
    need_teaching_technique = st.checkbox(
        "Tôi muốn nhập phương pháp giảng dạy",
        key="teaching_technique"
        )
    if need_teaching_technique:
        teaching_technique = st.text_area(
            label="Điền phương pháp giảng dạy"
            )
        
    need_more_context = st.checkbox(
        "Tôi muốn nhập thêm thông tin",
        key="more_input"
        )
    if need_more_context:
        additional_requirement = st.text_area(
            label="Điền thêm thông tin tại đây"
            ) 
     
with col2:
    #----------------------------------------------------------
    st.markdown("""
    ### II. NHIỆM VỤ
                """)
        
    task = st.radio(
        "Thầy cô muốn yêu cầu GenAI làm gì?", 
        ["Tạo kế hoạch bài dạy", "Tạo câu hỏi luyện tập", "Tạo đề kiểm tra", "Nhiệm vụ khác"]
        )
    if task == "Tạo kế hoạch bài dạy":
        khbd = st.selectbox(
            "Chọn khung KHBD",
            ["theo công văn 2345/BGD", "theo công văn 5512/BGD", "theo mẫu riêng"]
            )
        if khbd == "theo mẫu riêng":
            custom_khbd = st.text_area("Nhập KHBD tại đây")
        
    elif task == "Nhiệm vụ khác":
        custom_task = st.text_input("Điền nhiệm vụ của GenAI tại đây")
        
    
st.markdown("""
---
            """)    
        
col1, col2 = st.columns(2)
with col1:
    #----------------------------------------------------------
    st.markdown("""
    ### III. DỮ LIỆU
                """)
    
    st.multiselect(
        "Chọn các bài học",
        ["blank list"]
        )
    
    # st.write(f"Dữ liệu {subject} {grade} - bộ sách {book} sẽ được nhập tự động!")
    try:
        if khbd != "theo mẫu riêng":
            st.write(f"KHBD {khbd} sẽ được nhập tự động!")
    except:
        pass
    
    
with col2:
    #----------------------------------------------------------
    st.markdown("""
    ### IV. KẾT QUẢ
                """)
    have_example = st.checkbox("Tôi có ví dụ")
    if have_example:
        st.text_area("Nhập ví dụ tại đây")
        
    have_output_format = st.checkbox("Tôi muốn thiết lập từng bước cho AI")
    if have_output_format:
        st.text_area("Nhập các bước AI cần thực hiện tại")
    

    #%%% PROMPT OUTPUT
st.markdown("""
---
### Kết quả Prompt
            """)
            
#----------------------------------------------------------
            
result_prompt =  (
    "#BỐI CẢNH" + 
    f"\nBạn là giáo viên {subject} {grade}. Bạn sử dụng bộ sách {book}. "
    )

if need_teaching_technique:
    result_prompt += f"Bạn ứng dụng phương pháp {teaching_technique} trong công việc."
    
if need_more_context:
    result_prompt += f"bạn cần lưu ý thêm rằng {additional_requirement}"
 
#----------------------------------------------------------
result_prompt +=  (
    "\n\n#NHIỆM VỤ" +
    f"\nNhiệm vụ của bạn là {task.lower()}."
    
    )
#----------------------------------------------------------
result_prompt +=  (
    "\n\n#DỮ LIỆU\n" 
    
    )
#----------------------------------------------------------
result_prompt +=  (
    "\n\n#KẾT QUẢ\n" 
    
    )

st.text_area(
    label="Prompt:",
    value=result_prompt,
    height=(result_prompt.count("\n")+1)*25
    )
    
   


    