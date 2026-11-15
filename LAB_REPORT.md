# LAB REPORT: Multilingual Lecture-to-Notes & Quiz Generator

**Course:** Working With Large Language Models (WWLLM) — Continuous Internal Evaluation 3 (CIE 3)  
**Student Name:** M Raghavendra Samarth  
**GitHub Repository:** [https://github.com/RaghavendraSamarth/lecture-notes-quiz](https://github.com/RaghavendraSamarth/lecture-notes-quiz)  
**Live Deployed Application:** [https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/](https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/)  

---

## 1. Aim & Objective
To design, implement, and benchmark an interactive, privacy-preserving educational tool that:
1. Transcribes multi-format spoken lecture audio into text locally on CPU.
2. Generates concise, hallucination-free extractive study notes from the lecture content.
3. Automatically constructs source-grounded 5-question multiple-choice cloze quizzes with domain-relevant distractors.
4. Provides instant learner scoring alongside verbatim source-sentence evidence to ensure 100% factual auditability.

---

## 2. Tools & Technologies Used
- **Programming Language:** Python 3.10+
- **Frontend Framework:** Streamlit (deployed on Streamlit Community Cloud)
- **Speech Recognition (ASR):** `faster-whisper` (CTranslate2, `int8` CPU inference, Voice Activity Detection)
- **Audio Processing:** PyAV (`av`) with cross-version signature compatibility wrappers
- **Generative AI Integration (Optional):** Pretrained Indic Foundation Model `BharatGen Param-1` (`bharatgenai/Param-1`) via Hugging Face Transformers
- **Evaluation & Benchmarking:** Python `unittest` / deterministic smoke suite (`evaluate.py`)

---

## 3. System Workflow & Architecture
1. **Input Stage:** The user uploads lecture audio (`.wav`, `.mp3`, `.m4a`, `.flac`) or pastes an existing transcript.
2. **ASR Transcription:** `faster-whisper` transcribes audio into text with automatic language detection and confidence scoring.
3. **Extractive Note Summarization:** Computes sentence-level information density using term frequency, normalized by length and adjusted with an introductory topic prior (`+0.15`).
4. **Cloze Quiz Generation:** Identifies significant content terms ($\ge 5$ letters), replaces them with blanks (`________`), and draws 3 distractors dynamically from other sentences in the same lecture.
5. **Interactive Assessment:** The learner selects answers for 5 randomized multiple-choice questions; the app checks responses, reports the score, and displays the exact source sentence for audit.

---

## 4. Quantitative Testing & Evaluation
The system was validated on a **30-passage benchmark dataset** (`evaluation_cases.csv`) covering Computer Science, Physics, Chemistry, Biology, Economics, Civics, and Environmental Sciences.

| Metric | Target | Result | Status |
| :--- | :---: | :---: | :---: |
| **Benchmark Test Cases** | $\ge 30$ | **30 cases** | **PASSED** |
| **Mean Gold-Term Note Coverage** | $> 80\%$ | **92.7%** | **PASSED** |
| **Quiz Answer Source-Grounding** | $100\%$ | **100.0%** | **PASSED** |

- **92.7% Concept Coverage:** Retains almost all essential keyphrases from the original lecture passages.
- **100% Provenance:** Every question answer is strictly grounded in the source text, ensuring zero model hallucination.

---

## 5. Sample Output & Live Demonstration

### Input Transcript Excerpt:
> *"Photosynthesis converts light energy into chemical energy. Chlorophyll absorbs sunlight in leaves. Plants use carbon dioxide and water to produce glucose and oxygen."*

### Generated Study Notes:
- *Photosynthesis converts light energy into chemical energy.*
- *Chlorophyll absorbs sunlight in leaves.*
- *Plants use carbon dioxide and water to produce glucose and oxygen.*

### Sample Cloze Question Generated:
- **Question:** Chlorophyll absorbs sunlight in `________`.
- **Options:** A) chemical &nbsp;&nbsp; B) leaves &nbsp;&nbsp; C) glucose &nbsp;&nbsp; D) oxygen
- **Correct Answer:** **leaves**
- **Source Evidence:** *"Chlorophyll absorbs sunlight in leaves."* (Verified: 100% grounded)

---

## 6. Access & Submission Links
- **GitHub Repository:** [https://github.com/RaghavendraSamarth/lecture-notes-quiz](https://github.com/RaghavendraSamarth/lecture-notes-quiz)
- **Live Cloud Application:** [https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/](https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/)

---

## 7. Conclusion
The developed system demonstrates an effective, lightweight, and completely auditable alternative to unconstrained LLMs for education. By pairing local speech recognition with extractive ranking and source-grounded question formulation, students receive verifiable study notes and self-assessment quizzes without external cloud dependencies or risk of factual hallucinations.
