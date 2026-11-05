# Project Submission Report: Multilingual Lecture-to-Notes & Quiz Generator

**Course:** Working With Large Language Models (WWLLM) — Continuous Internal Evaluation 3 (CIE 3)  
**Student Name:** M Raghavendra Samarth  
**Repository:** [https://github.com/RaghavendraSamarth/lecture-notes-quiz](https://github.com/RaghavendraSamarth/lecture-notes-quiz)  
**Live Deployed Application:** [https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/](https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/)  

---

## 1. Problem Definition & Relevance

Modern digital education relies heavily on video and audio lectures across diverse disciplines and multilingual student bodies. However, students often struggle to:
1. Retain core conceptual takeaways from long lectures without concise, grounded study notes.
2. Self-assess their factual understanding immediately after listening.
3. Trust AI-generated summaries and quizzes that frequently suffer from ungrounded hallucinations, external bias, or unverified claims.

This project addresses these challenges by delivering an end-to-end, privacy-preserving lecture processing pipeline that converts spoken lecture audio or text into **auditable, factual study notes** and **source-grounded 5-question cloze quizzes**, complete with automated grading and source sentence verification.

---

## 2. Model & Dataset Selection

### Models & Frameworks:
- **Speech-to-Text (ASR):** `faster-whisper` (`small` model) leveraging CTranslate2 with `int8` CPU quantization. Features Voice Activity Detection (`vad_filter=True`) and automatic language identification with probability scoring. Includes custom PyAV (`av`) compatibility handling to guard against runtime signature deprecations.
- **Extractive Grounded Summarizer:** Term frequency-inverse sentence length baseline with an introductory topic prior (`+0.15` first-sentence bias), ensuring high-density factual retention without generative drift.
- **Distractor & Cloze Generation Engine:** In-domain lexical candidate extraction filtering non-trivial domain tokens (`[A-Za-z-]{4,}` excluding generic transitionals like *because*, *therefore*, *however*), drawing distractors strictly from the source transcript's vocabulary.
- **Optional GenAI Integration:** Pretrained Indic foundation model **BharatGen Param-1** (`bharatgenai/Param-1`) via the Hugging Face Transformers pipeline for comparative 4-bullet abstractive synthesis.

### Dataset & Test Benchmark:
- **Benchmark Suite (`evaluation_cases.csv`):** 30 curated lecture passages spanning 7 academic disciplines: Computer Science (algorithms, stacks, databases, networking), Biology & Medicine (photosynthesis, DNA, circulatory system), Physics (Newton's laws, thermodynamics, sound waves), Chemistry (covalent bonds, periodic table), Civics & Governance (Constitution, fundamental rights), Economics (supply and demand, inflation), and Earth Sciences (monsoon, water cycle).
- Each benchmark case contains a representative lecture passage alongside verified human gold concepts.

---

## 3. Working End-to-End Application

The application is implemented in Python using **Streamlit** ([`app.py`](app.py)):

1. **Input Interface:** Supports direct multi-format audio uploads (`.wav`, `.mp3`, `.m4a`, `.flac`) with one-click local transcription, as well as manual transcript pasting and editing.
2. **Audio Transcription:** Automatically detects spoken language, measures confidence, and streams transcription into the editable text workspace.
3. **Study Notes Generation:** Outputs concise, ordered bullet points summarizing key concepts, with one-click file download (`lecture_notes.txt`).
4. **Interactive 5-Question Quiz:** Dynamically presents multiple-choice questions with randomized option ordering (`A`, `B`, `C`, `D`).
5. **Instant Scoring & Audit:** Validates learner responses, displays the overall score, and exposes the exact verbatim source sentence for each question to support auditability.

---

## 4. GenAI, Speech & Auditable Integration

```
  [ Lecture Audio (.wav / .mp3) ]
                 │
                 ▼
     ┌───────────────────────┐
     │     faster-whisper    │  (int8 CPU, VAD filtering, language detection)
     └───────────┬───────────┘
                 │
                 ▼
     [ Raw Lecture Transcript ] ◄── (Direct Text Input)
                 │
        ┌────────┴────────────────────────┬────────────────────────┐
        ▼                                 ▼                        ▼
┌───────────────────┐           ┌───────────────────┐    ┌───────────────────┐
│ Extractive Notes  │           │ Cloze Quiz Engine │    │ BharatGen Param-1 │
│ Sentence Scorer   │           │ & Distractor Pool │    │ (Optional GenAI   │
└─────────┬─────────┘           └─────────┬─────────┘    │  Abstractive LLM) │
          │                               │              └─────────┬─────────┘
          ▼                               ▼                        ▼
   Concise Factual                 5-Question MCQs          4-Bullet Abstractive
     Study Notes                  with Source Audit                 Draft
```

- **Auditable Provenance:** Every quiz answer is strictly extracted from the transcript text, providing 100% source-grounding and zero hallucination.
- **Comparative AI Output:** Learners can toggle BharatGen Param-1 to observe trade-offs between strictly extractive grounded notes and generative abstractive summaries.

---

## 5. Quantitative Testing & Error Analysis

### Quantitative Benchmark Results (`evaluate.py`):
Running deterministic validation across all 30 benchmark cases:

| Metric | Target | Result | Status |
| :--- | :---: | :---: | :---: |
| **Test Cases Evaluated** | $\ge 30$ | **30 cases** | Passed |
| **Mean Gold-Term Note Coverage** | $> 80\%$ | **92.7%** | Passed |
| **Quiz Answer Source-Grounding** | $100\%$ | **100.0%** | Passed |

- **Mean Gold-Term Coverage (92.7%):** Out of all core curriculum terms identified in the gold annotations, 92.7% are preserved in the top-ranked summary notes.
- **Source-Grounding Rate (100.0%):** Every generated question answer exists verbatim within its declared source sentence.

### Failure & Error Analysis:
1. **Low-Frequency Detail Omission:** Because extractive scoring emphasizes high-frequency domain vocabulary, critical definitions that appear only once in passing may be outranked by repeated concepts.
2. **Lexical Cloze Term Ambiguity:** Term selection picks trailing alphabetic words of length $\ge 5$; in rare cases with descriptive text, an adjective may be blanked rather than the primary noun.
3. **Distractor Homogeneity in Short Transcripts:** In short transcripts ($< 30$ words), the available vocabulary pool is limited, leading to distractors that may be grammatically distinguishable or share obvious clues.
4. **Script Segmentation Boundaries:** Sentence splitting depends on standard terminators (`.`, `!`, `?`, `।`); non-standard or unpunctuated ASR outputs can produce overly long single sentences.
5. **ASR Error Cascade:** Any phonetic misrecognitions made during audio transcription propagate directly into the extractive notes and quiz blanks.

---

## 6. Demonstration, Documentation & Repository

- **GitHub Repository:** [https://github.com/RaghavendraSamarth/lecture-notes-quiz](https://github.com/RaghavendraSamarth/lecture-notes-quiz)
  - Clean version history with `.gitignore` excluding all virtual environments, cache, and audio files.
  - Comprehensive `README.md` with badges, architecture, live app link, reproduction commands, and rubric mapping.
- **Live Interactive Demo:** [https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/](https://lecture-notes-quiz-tqwsq7j9me8yvqklyxqnnn.streamlit.app/)
- **Reproduction Commands:**
  ```bash
  git clone https://github.com/RaghavendraSamarth/lecture-notes-quiz.git
  cd lecture-notes-quiz
  python -m venv .venv
  .\.venv\Scripts\activate
  pip install -r requirements.txt
  python evaluate.py           # Runs quantitative benchmark
  streamlit run app.py         # Launches web interface
  ```
