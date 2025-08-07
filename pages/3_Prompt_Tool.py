#%% I. LIB
import streamlit as st
from data import SQLRepository
import os
import sqlite3
from pathlib import Path

#%% II. DATA

BASE_DIR = Path(__file__).resolve().parent.parent  # Access base dir in streamlit
database_name = str(list(BASE_DIR.glob('*.db'))[0])

connection = sqlite3.connect(
    database=database_name,
    check_same_thread=False
    )
repo = SQLRepository(connection)

#%% III. APP
st.markdown("""
# PROMPT TOOL

Thầy cô nhập các thông tin theo từng bước bên dưới.

--- 
""")

    #%%% 3.1 USER INPUT
col1, col2 = st.columns(2)
with col1:
        #%%%% 3.1.1 CONTEXT
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
    if int(grade) in range(1, 6):
        school = 'tiểu học'
    elif int(grade) in range(6, 10):
        school = 'trung học cơ sở'
    else:
        school = 'trung học phổ thông'
    
    author = st.selectbox(
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
        #%%%% 3.1.2 OBJECTIVE
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
        #%%%% 3.1.3 DATA
    st.markdown("""
    ### III. DỮ LIỆU
                """)
    
    lesson_list = st.multiselect(
        "Chọn các bài học",
        repo.get_lesson_list(subject, grade, author)
        )
    
    # st.write(f"Dữ liệu {subject} {grade} - bộ sách {author} sẽ được nhập tự động!")
    try:
        if khbd != "theo mẫu riêng":
            st.write(f"KHBD {khbd} sẽ được nhập tự động!")
    except:
        pass
    
    
with col2:
        #%%%% 3.1.4 RESULT
    st.markdown("""
    ### IV. KẾT QUẢ
                """)
    have_example = st.checkbox("Tôi có ví dụ")
    if have_example:
        st.text_area("Nhập ví dụ tại đây")
        
    have_output_format = st.checkbox("Tôi muốn thiết lập từng bước cho AI")
    if have_output_format:
        st.text_area("Nhập các bước AI cần thực hiện tại")
    

    #%%% 3.2 PROMPT OUTPUT
st.markdown("""
---
### Kết quả Prompt
            """)
            
        #%%%% 3.2.1 CONTEXT OUTPUT
            
result_prompt =  (
    "#BỐI CẢNH" + 
    f"\nBạn là giáo viên {subject} {grade}. Bạn sử dụng bộ sách {author}. Bạn dạy học theo chương trình giáo dục phổ thông 2018, ở cấp {school}."
    )

if need_teaching_technique:
    result_prompt += f"Bạn ứng dụng phương pháp {teaching_technique} trong công việc."
    
if need_more_context:
    result_prompt += f"bạn cần lưu ý thêm rằng {additional_requirement}"











        #%%%% 3.2.2 OBJECTIVE OUTPUT
result_prompt +=  (
    "\n\n#NHIỆM VỤ" +
    f"\nNhiệm vụ của bạn là {task.lower()}."
    
    )










        #%%%% 3.2.3 DATA OUTPUT
result_prompt +=  (
    "\n\n#DỮ LIỆU\n" 
    
    )

try:
    for lesson in lesson_list:
        result_prompt += f"##Bài {lesson}:\n {repo.get_knowledge(subject, grade, author, lesson)}"
    
except:
    pass




        #%%%% 3.2.4 RESULT OUTPUT
result_prompt +=  (
    "\n\n#KẾT QUẢ\n" 
    
    )

try:
    if khbd == "theo công văn 5512/BGD":
        result_prompt += f"Trả kết quả theo mẫu sau:\n{repo.get_cong_van('5512/BGDĐT-GDTrH', 'khung khbd')}"
    elif khbd == "theo công văn 2345/BGD":
        result_prompt += f"Trả kết quả theo mẫu sau:\n{repo.get_cong_van('2345/BGDĐT-GDTH', 'khung khbd')}"
except:
    pass

st.text_area(
    label="Prompt:",
    value=result_prompt,
    height=(result_prompt.count("\n")+1)*25
    )
    
   


    