# 🚀 Python FastAPI Modern Web Application

Dự án được khởi tạo và điều phối tự động bởi **Antigravity Master Orchestrator** trong Antigravity IDE.

---

## 🏗️ KIẾN TRÚC & TÍNH NĂNG ĐÃ THIẾT LẬP
- **FastAPI Core:** Async framework tốc độ cao, hỗ trợ tự động sinh OpenAPI & Swagger documentation.
- **Pydantic v2 & Pydantic-Settings:** Type validation, serialize và quản lý biến môi trường chuẩn xác.
- **CORS & Middleware:** Sẵn sàng kết nối Frontend (Next.js, Vite/React, Vue) hoặc chạy Fullstack.
- **Tối ưu hóa ngữ cảnh AI (.antigravityignore):** Loại bỏ toàn bộ file rác, cache, build artifacts để tiết kiệm token và tăng tốc xử lý cho AI.
- **Linter & Formatter (Ruff):** Thiết lập cấu hình trong `pyproject.toml` để tự động format và kiểm tra lỗi cú pháp siêu tốc.
- **Đội ngũ Sub-agents chuyên biệt:**
  - `@architect-agent`: Phân tích yêu cầu, thiết kế schema và phân rã task.
  - `@coder-agent`: Viết code sạch, tối ưu hiệu năng theo phong cách Vibe Coder.
  - `@debugger-qa-agent`: Đọc log lỗi, chạy test tự động và self-healing.
  - `@docs-guide-agent`: Quản lý tài liệu và duy trì đồng bộ tri thức dự án.

---

## ⚡ HƯỚNG DẪN KHỞI CHẠY NHANH (QUICK START)

### 1. Cài đặt môi trường ảo & Thư viện (Terminal)
```bash
# Tạo môi trường ảo Python
python -m venv .venv

# Kích hoạt môi trường (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Chạy Server Development
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **Landing Page:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)
- **Health Check API:** [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

### 3. Chạy Unit & Integration Test
```bash
pytest
```

### 4. Kiểm tra Linter & Format code
```bash
ruff check . --fix
ruff format .
```

---

## 🎮 CẨM NANG ĐIỀU KHIỂN BẰNG LỆNH TẮT (TRIGGERS)
- `/plan [ý tưởng]`: Gọi `@architect-agent` phân tích và lên sơ đồ kiến trúc + task board.
- `/build [tính năng]`: Gọi `@coder-agent` triển khai code ngay lập tức từ A-Z.
- `/fix`: Gọi `@debugger-qa-agent` tự quét lỗi terminal và tự sửa (Self-healing).
- `/status`: Xem tiến độ và việc cần làm tiếp theo trong `.antigravity/01_TASK_BOARD.md`.
- `/style [thay đổi]`: Thay đổi chế độ tương tác và quy tắc làm việc bất kỳ lúc nào.
