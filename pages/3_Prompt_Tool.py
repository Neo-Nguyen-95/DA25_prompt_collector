import streamlit as st

st.markdown("""
# PROMPT TOOL

Thầy cô nhập các thông tin theo từng bước bên dưới.

--- 
""")

            
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### I. BỐI CẢNH
                """)
    subject = st.selectbox(
        "Chọn môn học", 
        ["Toán", "Văn", "Tiếng Anh", "Khoa học tự nhiên", "Lịch Sử", "Địa Lí"]
        )
    grade = st.selectbox(
        "Chọn lớp", 
        ["6", "7", "8", "9", "10", "11", "12"]
        )
    book = st.selectbox(
        "Chọn bộ sách",
        ["Cánh Diều", "Kết Nối Tri Thức", "Chân Trời Sáng Tạo"]
        )
    
    need_teaching_technique = st.checkbox(
        "Tôi muốn nhập phương pháp giảng dạy",
        key="teaching_technique"
        )
    if need_teaching_technique:
        teaching_technique = st.text_area(
            label="Điền phương pháp giảng dạy"
            )
        
    need_more_input = st.checkbox(
        "Tôi có thêm thông tin",
        key="more_input"
        )
    if need_more_input:
        additional_requirement = st.text_area(
            label="Điền thêm thông tin tại đây"
            ) 
     
with col2:
    
    st.markdown("""
    ### II. NHIỆM VỤ
                """)
        
    task = st.radio(
        "Thầy cô muốn yêu cầu GenAI làm gì?", 
        ["Tạo kế hoạch bài dạy", "Tạo câu hỏi luyện tập", "Tạo đề kiểm tra", "Khác"]
        )
    if task == "Tạo kế hoạch bài dạy":
        khbd = st.selectbox(
            "Chọn khung KHBD",
            ["theo công văn 2345/BGD", "theo công văn 5512/BGD", "theo mẫu riêng"]
            )
        if khbd == "theo mẫu riêng":
            custom_khbd = st.text_area("Nhập KHBD tại đây")
        
    if task == "Khác":
        custom_task = st.text_input("Điền nhiệm vụ của GenAI tại đây")
        
    
st.markdown("""
---
            """)    
        
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### III. DỮ LIỆU
                """)
    
    st.write(f"Dữ liệu {subject} {grade} - bộ sách {book} sẽ được nhập tự động!")
    if khbd != "theo mẫu riêng":
        st.write(f"KHBD {khbd} sẽ được nhập tự động!")
    
    
with col2:
    st.markdown("""
    ### IV. KẾT QUẢ
                """)
    have_example = st.checkbox("Tôi có ví dụ")
    if have_example:
        st.text_area("Nhập ví dụ tại đây")
        
    have_output_format = st.checkbox("Tôi muốn thiết lập từng bước cho AI")
    if have_output_format:
        st.text_area("Nhập các bước AI cần thực hiện tại")
    


st.markdown("""
---
### Kết quả Prompt
            """)
            
result_prompt =  (
    "#BỐI CẢNH\n" + 
    f"Bạn là giáo viên {subject} {grade}. Bạn sử dụng bộ sách {book}. "
    )

if need_teaching_technique:
    result_prompt += f"Bạn ứng dụng phương pháp {teaching_technique} trong công việc."
    
if need_more_input:
    result_prompt += f"bạn cần lưu ý thêm rằng {additional_requirement}"
    
result_prompt +=  (
    "\n#NHIỆM VỤ\n" 
    
    )

result_prompt +=  (
    "\n#DỮ LIỆU\n" 
    
    )

result_prompt +=  (
    "\n#KẾT QUẢ\n" 
    
    )

st.code(result_prompt)
    
   


    