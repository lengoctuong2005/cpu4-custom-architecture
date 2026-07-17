---
trigger: model_decision
description: "MASTER ROUTER (Bản đồ Đại Thư Viện) - Cẩm nang định hướng tư duy ĐẦU TIÊN cho mọi task. AI buộc phải đọc file này để biết cần gọi Orchestrator nào."
---

# THE GRAND LIBRARY MAP (Bản Đồ Đại Thư Viện Antigravity)

**TÔN CHỈ**: Hệ thống có >780 rules, skills, design systems và templates. AI **TUYỆT ĐỐI KHÔNG** load ngẫu nhiên các file. Khi bắt đầu tác vụ, AI phải xác định "Domain" (Lĩnh vực) và **CHỈ ĐƯỢC LOAD** Orchestrator của Domain đó.

---

## Quy tắc Hành xử: "The Librarian Rule" (Luật Thủ Thư)
1. Nhận yêu cầu → Xác định đúng Domain bên dưới.
2. Load đúng Orchestrator của Domain đó.
3. Đọc hướng dẫn trong Orchestrator → Load đúng Skills/Templates cần thiết.
4. **Không bao giờ load toàn bộ thư viện. Mỗi task chỉ load tối đa 3-5 skills.**

---

## Domain 1: Giao diện & Trải nghiệm (UI / UX / Frontend)
- **Dấu hiệu**: Thiết kế web, landing page, CSS, animation, GSAP, UI components, React/Vue/Nextjs, Tailwind, responsive.
- **Orchestrator**: `~/.gemini/workflows/design-orchestrator.md`
- **Kho tài nguyên**:
  - `antigravity/skills/open-design/` (54 skills: frontend-design, gsap-core, shadcn-ui, ui-ux-pro-max...)
  - `antigravity/skills/design-systems/` (150 hệ thống: apple, stripe, linear, vercel...)
  - `antigravity/skills/design-templates/` (109 mẫu: dashboard, landing, blog, pricing...)

## Domain 2: Lõi Hệ thống & Cơ sở dữ liệu (Backend / Architecture)
- **Dấu hiệu**: API, Database, Prisma, Schema, Microservices, Python, Node.js, Authentication, REST, GraphQL.
- **Orchestrator**: `~/.gemini/workflows/backend-orchestrator.md`
- **Kho tài nguyên**:
  - `antigravity/skills/backend/` (api-design, database-migrations, event-driven-architecture, grpc-microservices)
  - `antigravity/skills/ecc-extracted/` (nestjs-patterns, django-patterns, fastapi-patterns, laravel-patterns, springboot-patterns, postgres-patterns, prisma-patterns, redis-patterns, mysql-patterns, error-handling...)

## Domain 3: Triển khai & Hạ tầng (DevOps / Infrastructure)
- **Dấu hiệu**: Docker, CI/CD, Github Actions, Server, Nginx, AWS, Deployment, Kubernetes.
- **Orchestrator**: `~/.gemini/workflows/devops-orchestrator.md`
- **Kho tài nguyên**:
  - `antigravity/skills/devops/` (kanban-orchestrator, kanban-worker)
  - `antigravity/skills/ecc-extracted/` (docker-patterns, kubernetes-patterns, deployment-patterns, github-ops, git-workflow, terminal-ops)
  - `antigravity/skills/ecc-extracted/` (homelab-network-*, network-config-validation, network-bgp-diagnostics)

## Domain 4: Bảo mật & Khắc phục sự cố (Security / Debugging)
- **Dấu hiệu**: Fix bug khó, rò rỉ bộ nhớ, bị hack, phân quyền, review code, audit.
- **Orchestrator**: `~/.gemini/workflows/security-audit.md` hoặc `~/.gemini/workflows/debug.md`
- **Kho tài nguyên**:
  - `antigravity/skills/ecc-extracted/` (security-review, security-scan, security-bounty-hunter, hipaa-compliance, systematic-debugging)
  - `antigravity/skills/workflows/` (audit_and_fix, deep-review)

## Domain 5: IoT & Phần cứng (Firmware / Embedded / PCB)
- **Dấu hiệu**: Firmware, C/C++, RTOS, PCB, Quartus, FPGA, Bootloader, OTA, kernel, hardware.
- **Orchestrator**: Không có file riêng → AI tự tham chiếu danh sách skills bên dưới.
- **Kho tài nguyên**:
  - `antigravity/skills/iot-hardware/` (firmware-baremetal, hil-testing, kernel-debugging, ota-bootloader, pcb-design-review, rtos-concurrency)
- **Quy tắc bổ sung**: Luôn kiểm tra file `memory/causal-graph.yaml` để nắm giới hạn phần cứng trước khi đề xuất thư viện.

## Domain 6: AI / ML / Agent (Trí tuệ nhân tạo)
- **Dấu hiệu**: LLM, Agent, Prompt Engineering, Training, Fine-tuning, Evaluation, RAG, MCP.
- **Orchestrator**: Không có file riêng → Tham chiếu danh sách bên dưới.
- **Kho tài nguyên**:
  - `antigravity/skills/ai-agents/` (microkernel-architecture)
  - `antigravity/skills/autonomous-ai-agents/` (claude-code, codex, hermes-agent, opencode)
  - `antigravity/skills/evaluation/` (lm-evaluation-harness, weights-and-biases)
  - `antigravity/skills/inference/` (llama-cpp, vllm)
  - `antigravity/skills/mlops/` (huggingface-hub)
  - `antigravity/skills/models/` (audiocraft, segment-anything)
  - `antigravity/skills/ecc-extracted/` (agent-eval, agent-harness-construction, prompt-optimizer, mcp-server-patterns, agentic-engineering...)

## Domain 7: Nghiên cứu & Tài liệu (Research / Documentation)
- **Dấu hiệu**: Viết báo cáo, paper, tìm kiếm tài liệu, phân tích dữ liệu, tổng hợp thông tin.
- **Orchestrator**: Không có file riêng → Tham chiếu danh sách bên dưới.
- **Kho tài nguyên**:
  - `antigravity/skills/research/` (arxiv, blogwatcher, llm-wiki, polymarket, research-paper-writing)
  - `antigravity/skills/ecc-extracted/` (deep-research, literature-review, data-report, research-decision-room)

## Domain 8: Mobile & Desktop App
- **Dấu hiệu**: iOS, Android, Swift, Kotlin, Flutter, React Native, Desktop app.
- **Orchestrator**: Không có file riêng → Tham chiếu danh sách bên dưới.
- **Kho tài nguyên**:
  - `antigravity/skills/apple/` (apple-notes, apple-reminders, findmy, imessage, macos-computer-use)
  - `antigravity/skills/ecc-extracted/` (android-clean-architecture, swift-concurrency-6-2, swiftui-patterns, dart-flutter-patterns, compose-multiplatform-patterns, kotlin-patterns, mobile-app, mobile-onboarding)

## Domain 9: Năng suất & Tích hợp dịch vụ (Productivity / Integrations)
- **Dấu hiệu**: Notion, Airtable, Google Workspace, Email, Social media, PDF.
- **Orchestrator**: Không có file riêng → Tham chiếu danh sách bên dưới.
- **Kho tài nguyên**:
  - `antigravity/skills/productivity/` (airtable, google-workspace, maps, nano-pdf, notion, powerpoint, x-api, x-research)
  - `antigravity/skills/email/` (himalaya)
  - `antigravity/skills/social-media/` (xurl)
  - `antigravity/skills/media/` (gif-search, heartmula, songsee, youtube-content)

## Domain 10: Sáng tạo Nội dung (Creative / Content)
- **Dấu hiệu**: Viết bài, marketing, infographic, poster, video, slide, presentation.
- **Orchestrator**: Không có file riêng → Tham chiếu danh sách bên dưới.
- **Kho tài nguyên**:
  - `antigravity/skills/creative/` (architecture-diagram, ascii-art, baoyu-infographic, claude-design, excalidraw, hand-drawn-diagrams, manim-video, p5js, sprite-animation, video-editing...)
  - `antigravity/skills/open-design/` (copywriting, marketing-psychology, poster-hero, social-reddit-card, social-spotify-card, social-x-post-card, resume-modern, release-notes-one-pager)

---

## Fallback: Task Không Thuộc Domain Nào
Nếu tác vụ không khớp với bất kỳ Domain nào ở trên:
1. Tìm kiếm trong `RULES_MANIFEST.md` bằng từ khóa.
2. Dùng `list_dir` tại `~/.gemini/antigravity/skills/ecc-extracted/` để dò tên skill gần nhất.
3. Nếu vẫn không tìm thấy → Thông báo User và code từ kiến thức nội tại.

## Thống Kê Hệ Thống (cập nhật 2026-06-22)
| Hạng mục | Số lượng |
|---|---|
| Rules | 31 |
| Workflows | 22 |
| Skills (SKILL.md) | 522 |
| Design Systems (DESIGN.md) | 150 |
| Design Templates | 109 |
| Memory Files | 24 |
| **Tổng tài nguyên** | **858** |
