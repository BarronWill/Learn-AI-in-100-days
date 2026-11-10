**Document Chat RAG**. Tôi bốc ngẫu nhiên trong danh sách 7 project nhẹ, hợp với máy của bạn (các RAG cơ bản, Agentic RAG, RAG SQL Router, Chat with Code, MCP Agentic RAG). Nó cũng trùng với project tôi đã gợi ý làm điểm bắt đầu.

### Mục tiêu

Một ứng dụng cho phép tải tài liệu lên và hỏi đáp, trả lời kèm trích dẫn đoạn nguồn.

### Kế hoạch gợi ý

1. **Chạy bản gốc trong repo** (1–2 buổi). Thay Llama 3.3 bằng API miễn phí (Gemini hoặc Groq) để chạy được trên máy bạn. Chỉ cần hiểu luồng: tài liệu → chunk → embedding → vector store → truy xuất → LLM.
2. **Viết lại phiên bản của bạn**: FastAPI + Qdrant hoặc Chroma, embedding nhỏ chạy local (bge-small). Tự làm tay 3 phần lõi: chunking, truy xuất, và prompt ghép ngữ cảnh. Phần UI, config, Docker thì nhờ AI.
3. **Đổi sang dữ liệu thật**: dùng tài liệu bạn quen, ví dụ tài liệu kỹ thuật công khai hoặc ghi chú học tập của bạn. Nếu muốn dùng tài liệu công ty (RFC/Onecall) thì cần kiểm tra quy định bảo mật trước.
4. **Cố tình làm nó hỏng rồi sửa**. Đây là phần học nhiều nhất. Hãy thử:

- Hỏi câu mà tài liệu không có. Hệ thống có bịa không?
- Đổi chunk size (200, 500, 1000) và so sánh chất lượng.
- Hỏi câu cần ghép thông tin từ hai đoạn khác nhau.
- Tạo khoảng 20 câu hỏi kèm đáp án đúng để tự chấm. Đây là bước đầu của evaluation.

Mỗi vấn đề bạn gặp sẽ dẫn tới project tiếp theo trong repo (Trustworthy RAG, Agentic RAG, RAG with Docling, như bảng tôi đưa trước đó).

Nếu bạn muốn, tôi có thể giúp phác khung thư mục và các module của bước 2, hoặc viết sẵn danh sách câu hỏi mẫu cho bước 4 theo loại tài liệu bạn chọn.