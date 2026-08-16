# Refleksi — Multi-Agent Systems W4 (Task 5)

> OKR G1-Q3-08 | Selesai 16 Agu 2026 | Praktik: LangGraph 1.2.11, ADK 2.7.0, DeepSeek via litellm

## 1. Apa beda orchestrator vs supervisor? Kapan pakai masing-masing?

- Orchestrator: routing FIXED/pre-planned. Agent pusat pecah task, assign ke worker, worker tidak bisa mengubah alur. Cocok untuk pipeline yang predictable (RAG, report generation).
- Supervisor: routing DINAMIS. Supervisor mengevaluasi hasil tiap step lalu memutuskan agent berikutnya, bisa loop sampai FINISH. Cocok untuk task yang butuh iterasi (research -> evaluasi -> research lagi -> summarize).
- Keputusan: kalau alur bisa digambar sekali jalan = orchestrator/pipeline; kalau keputusan tergantung hasil antara = supervisor.
- Praktik: Task 2 (supervisor, loop guard 5 iterasi) vs Task 4 (pipeline 2 node). Di Task 2 terlihat langsung supervisor memilih researcher berulang kali karena notes belum dianggap cukup.

## 2. Kapan multi-agent TIDAK diperlukan?

- Task tunggal dengan scope jelas (1 prompt + tools cukup)
- Over-engineering: cost naik (banyak LLM call), latency naik, debug lebih susah
- Rule of thumb dari praktik: kalau 1 agent + tools bisa handle, jangan multi-agent. Multi-agent untuk task yang BENAR-BENAR bisa di-dekomposisi dan tiap bagian butuh keahlian/tools berbeda.

## 3. LangGraph vs ADK: mana yang dipilih untuk use case BSIM? Kenapa?

- Pilih LANGGRAPH untuk BSIM IT Resilience Assessment.
- Alasan: butuh kontrol halus (loop, retry, human-in-the-loop, checkpointing) untuk workflow assessment yang panjang dan auditable; graph state machine eksplisit = mudah di-justify ke governance/compliance.
- ADK tetap berguna untuk prototyping cepat (hierarchy bawaannya intuitif, delegasi otomatis).
- Catatan: ADK 2.7 API berubah signifikan (Runner.run generator + new_message, create_session async, FunctionTool). Kurva belajar ADK rendah TAPI docs berubah cepat.

## 4. Apa saja anti-pattern yang harus dihindari?

- Multi-agent untuk task sederhana (cost + latency)
- Agent tanpa loop guard (selalu max_iterations — terbukti perlu di Task 2, supervisor bisa loop terus)
- State raksasa tanpa struktur (TypedDict per domain)
- Tool call tanpa error handling (Task 4: try/except + fallback data)
- Semua agent pakai model mahal (worker murah, supervisor/utama kuat)
- Prompt supervisor tanpa fallback decision (Task 2: decision tidak valid -> fallback RESEARCHER)

## 5. Bagaimana multi-agent bisa dipakai di proyek BSIM IT Resilience?

- Pipeline assessment: agent Collector (baca config/dokumen) -> agent Analyzer (cek vs baseline) -> agent Scorer (skor risiko) -> agent Reporter (generate laporan) — urutan fix, cocok pipeline.
- Supervisor layer di atasnya: memutuskan area mana yang perlu digali lebih dalam berdasarkan hasil awal (mirip pola Task 2).
- Governance angle: graph yang eksplisit = audit trail per step = mendukung 3 Lines of Defense dan OJK/BI compliance yang sedang dibangun (AI Principle & Pattern).
- Extend dari PoC Bedrock: multi-agent orchestration di atas Bedrock (deepseek/claude via Bedrock Converse).
