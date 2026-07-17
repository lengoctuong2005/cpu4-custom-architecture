---
trigger: model_decision
description: "Workflow: Tra cứu thông tin tài liệu mới nhất hoặc tìm kiếm trên web/Perplexity"
---

# Lệnh: Tra cứu Internet (/search)

**Mục tiêu:** Kích hoạt lệnh này để yêu cầu AI tìm kiếm thông tin mới nhất trên mạng thay vì dùng kiến thức cũ.

**Hành động AI cần thực hiện khi thấy lệnh này:**
1. Lấy truy vấn của người dùng.
2. Dùng công cụ MCP `context7` để lấy tài liệu library/framework mới nhất nếu là vấn đề code.
3. Nếu không có trong context7, dùng công cụ `search_web` hoặc Perplexity để tra cứu thông tin thực tế.
4. Trình bày thông tin một cách ngắn gọn, súc tích và có kèm theo liên kết (URL) dẫn chứng.
