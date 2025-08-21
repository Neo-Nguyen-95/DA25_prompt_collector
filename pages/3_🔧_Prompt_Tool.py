#%% I. LIB
import streamlit as st
from data import SQLRepository
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
st.set_page_config(
    layout="wide"
    )

st.markdown("""
# 🔧 PROMPT TOOL

""")

# Styled anchor that looks like a button
st.markdown(
    """
Thầy cô có thể cùng tham gia đóng góp kho kiến thức cho AI tại đây.
    
<a href="https://forms.gle/tJv8av3FkSRhSUyS9" target="_blank">
    <button style="padding:0.6rem 1rem; border-radius:8px; margin-bottom: 20px">
        ĐÓNG GÓP NGAY ↗
    </button>
</a>

Để sử dụng tool, thầy cô hãy nhập các thông tin theo từng bước bên dưới.

--- 
    """,
    unsafe_allow_html=True
)


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
        
    st.markdown("""
    ---
                """) 
     
    #%%%% 3.1.2 OBJECTIVE
    st.markdown("""
    ### II. NHIỆM VỤ
                """)
        
    task = st.radio(
        "Thầy cô muốn yêu cầu GenAI làm gì?", 
        [
            "Tạo kế hoạch bài dạy", 
            "Tạo câu hỏi luyện tập", 
            # "Tạo đề kiểm tra", 
            "Nhiệm vụ khác"]
        )
    if task == "Tạo kế hoạch bài dạy":
        khbd = st.selectbox(
            "Chọn khung KHBD",
            ["theo công văn 2345/BGD", "theo công văn 5512/BGD", "theo mẫu riêng"]
            )
        if khbd == "theo mẫu riêng":
            custom_khbd = st.text_area("Nhập KHBD tại đây")
    
    elif task == "Tạo câu hỏi luyện tập":
        item_type_list = st.multiselect(
            "Lựa chọn loại câu hỏi muốn thiết kế",
            ["Trắc nghiệm nhiều lựa chọn (MC)",
             "Trắc nghiệm đúng/sai (TF)",
             "Trắc nghiệm trả lời ngắn (SA)"]
            )
        st.write("Số lượng mặc định là 2 câu/loại. Các câu hỏi đều ở mức M2. Bạn có thể sửa lại số lượng và độ khó trong prompt kết quả.")
    
    elif task == "Nhiệm vụ khác":
        custom_task = st.text_input("Điền nhiệm vụ của GenAI tại đây")
    
    
    st.markdown("""
    ---
                """)   
                
    #%%%% 3.1.3 DATA
    st.markdown("""
    ### III. DỮ LIỆU
                 """)
     
    lesson_list = st.multiselect(
        "Chọn các bài học",
        repo.get_lesson_list(subject, grade, author)
        )
    
    try:
        if khbd != "theo mẫu riêng":
            st.write(f"KHBD {khbd} sẽ được nhập tự động!")
    except:
        pass
    
    st.markdown("""
    ---
                """) 
     
     
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
        
        
with col2:

    #%%% 3.2 PROMPT OUTPUT
    st.markdown("""
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
        f"\nNhiệm vụ của bạn là {task.lower()}. Sử dụng thông tin trong phần #DỮ LIỆU. Kết quả trả ra cần tuân theo các bước được đề cập trong mục #KẾT QUẢ"
        )
    
    if task == "Tạo câu hỏi luyện tập":
        result_prompt += (
            "\nBạn sẽ thiết kế các dạng câu hỏi sau:"
            )
        for item_type in item_type_list:
            result_prompt += f"\n* 2 câu {item_type} ở mức M2"
    
    
    
            #%%%% 3.2.3 DATA OUTPUT
    result_prompt +=  ("\n\n#DỮ LIỆU")
    
    try:
        for lesson in lesson_list:
            result_prompt += f"\n##KIẾN THỨC {lesson}:\n {repo.get_knowledge(subject, grade, author, lesson)}"
        
    except:
        pass
    
    if task == "Tạo câu hỏi luyện tập":
        result_prompt += (
            f"\n##HÌNH THỨC CÁC LOẠI CÂU HỎI:\n{repo.get_item_info()}" + 
            f"\n##MỨC ĐỘ CÁC LOẠI CÂU HỎI:\n{repo.get_item_diff()}"
            )
    
    
    
            #%%%% 3.2.4 RESULT OUTPUT
    result_prompt +=  ("\n\n#KẾT QUẢ\nThực hiện theo #NHIỆM VỤ đã yêu cầu.")
    
    try:
        if khbd == "theo công văn 5512/BGD":
            result_prompt += f"\nTrả kết quả theo mẫu sau:\n{repo.get_cong_van('5512/BGDĐT-GDTrH', 'khung khbd')}"
        elif khbd == "theo công văn 2345/BGD":
            result_prompt += f"\nTrả kết quả theo mẫu sau:\n{repo.get_cong_van('2345/BGDĐT-GDTH', 'khung khbd')}"
    except:
        pass
    
    st.text_area(
        label="Prompt:",
        value=result_prompt,
        height=(result_prompt.count("\n")+1)*25
        )
    
   


    