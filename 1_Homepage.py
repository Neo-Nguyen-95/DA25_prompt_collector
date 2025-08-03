import streamlit as st

st.set_page_config(
    page_title="Prompt For Education",
    page_icon="😉"
    )

st.title("ỨNG DỤNG HỖ TRỢ GIAO TIẾP HIỆU QUẢ VỚI GENAI DÀNH CHO GIÁO VIÊN")

st.markdown("""
*Xin chào các thầy cô đến với ứng dụng Prompt4Edu,*

Ứng dụng được tạo ra nhằm hỗ trợ các thầy cô giao tiếp với các công cụ GenAI một cách hiệu quả. Ứng dụng có 3 phần chính được thiết kế như sau:
    
1. :blue[**Introduction**]: Giới thiệu sơ lược về GenAI, đặc điểm của GenAI và cách giao tiếp hiệu quả với GenAI.

2. :green[**Prompt Tool**]: Chứa các bộ prompt mẫu cho từng cấu phần của một prompt đầy đủ. Thầy cô chỉ cần chọn từng cấu phần để tự xây dựng thành prompt riêng của mình. Đặc biệt, phần kiến thức phổ thông được cập nhật theo CTGDPT 2018 được tạo nên bởi cộng đồng giáo viên và tôi. Tất cả cấu phần này đều ở định dạng text, các thầy cô có thể copy & paste dễ dàng khi chat với GenAI.

3. :orange[**Chatbot Agent**]: Hỗ trợ giải đáp thắc mắc của thầy cô xung quanh chủ đề giao tiếp với GenAI.

---
            """)

col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("""
**About me**

Xin chào, tôi là Neo. Khoa học dữ liệu với tôi không chỉ là công việc mà còn là niềm vui. Bạn có thể tìm hiểu thêm về tôi và công việc tôi đang làm tại LinkedIn cá nhân này nhé. Hi hi!
                """)
    
with col2:
    st.markdown("""
**About the project & its story**

Trong một lần đi tập huấn giáo viên về sử dụng GenAI hiệu quả, tôi có cung cấp cho các thầy cô một prompt khá chi tiết, đầy đủ, giúp GenAI của các thầy cô trả lời đúng theo nhu cầu của mình. Tuy nhiên, nhiều thầy cô thắc mắc với tôi rằng "Prompt quá dài, quá khó nhớ, và trông khá khó hiểu" hay "Viết xong prompt này thì thà tôi tự làm còn hơn". Tức là kể cả khi có người hướng dẫn, nhiều thầy cô vẫn cảm thấy khó khăn để có cái nhìn đa chiều để có thể propmt hiệu quả, chưa kể nhiều thầy cô khác không được tiếp nhận nhiều tới các khoá học về AI.

Vậy nên tôi quyết định tạo ra app này để hỗ trợ các thầy cô tạo được thói quen prompt với đầy đủ các thành phần. Khi thầy cô tự tin vào năng lực prompt của mình thì app này có thể sẽ không cần tới nữa.

                """)
                
                
                
                
                