# 🎓 Multilingual Lecture-to-Notes & Quiz Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Quiz Grounding](https://img.shields.io/badge/Quiz%20Source%20Grounding-100%25-brightgreen.svg)]()
[![Gold Note Coverage](https://img.shields.io/badge/Gold%20Term%20Coverage-92.7%25-success.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end, privacy-preserving lecture processing and learning assessment pipeline built in Python and Streamlit. The application accepts spoken lecture audio or raw transcripts, generates concise extractive study notes, constructs source-grounded multiple-choice cloze quizzes with distractors, and provides instant interactive evaluation with full source attribution. It additionally supports optional local speech-to-text (`faster-whisper`) and an optional GenAI abstractive draft via **BharatGen Param-1**.

**Individual Submission:** M Raghavendra Samarth  
**Coursework:** Working With Large Language Models (WWLLM) — CIE 3 Activity

---

## 🌟 Key Features

1. **Local Speech Recognition (ASR) with Cross-Version Compatibility**
   - Transcribes uploaded lecture audio (`.wav`, `.mp3`, `.m4a`, `.flac`) directly on CPU using `faster-whisper` (`small` model, `int8` quantization).
   - Features built-in voice activity detection (VAD), language detection, and confidence scoring.
   - Includes cross-version PyAV (`av`) compatibility handling to eliminate `metadata_errors` runtime mismatches.

2. **Auditable Extractive Note Generation (Zero Hallucinations)**
   - Ranks sentences using an informational-frequency metric (word frequency weighted by sentence length with opening-sentence topic boosting).
   - Operates completely offline without external API costs or model hallucinations, preserving the original language of the lecture.

3. **Source-Grounded 5-Question Cloze Quiz**
   - Extracts key domain concepts from informative sentences to construct fill-in-the-blank cloze questions.
   - Dynamically samples plausible in-domain distractors from the lecture's own lexicon to ensure topic relevance.
   - Automatically randomizes answer choices across four positions (`A`, `B`, `C`, `D`).

4. **Interactive Self-Assessment & Source Evidence Audit**
   - Instant answer verification and automated score calculation.
   - Displays the exact source sentence for every question to allow learners and educators to audit factual groundings immediately.
   - Built-in one-click note export (`lecture_notes.txt`).

5. **Optional GenAI Abstractive Synthesis (BharatGen Param-1)**
   - Optional toggle to synthesize a 4-bullet abstractive summary using the official [BharatGen Param-1](https://huggingface.co/bharatgenai/Param-1) Transformers pipeline.
   - Enables learners to compare extractive source-grounded notes directly against generative abstractive summaries.

---

## 📊 Live Demonstration Example

### Sample Input Transcript
> *"Photosynthesis converts light energy into chemical energy. Chlorophyll absorbs sunlight in leaves. Plants use carbon dioxide and water to produce glucose and oxygen."*

### Generated Study Notes
- *Photosynthesis converts light energy into chemical energy.*
- *Chlorophyll absorbs sunlight in leaves.*
- *Plants use carbon dioxide and water to produce glucose and oxygen.*

### Sample Generated Cloze Question
| Field | Content |
| :--- | :--- |
| **Question** | `Chlorophyll absorbs sunlight in ________.` |
| **Options** | A) chemical &nbsp;&nbsp; B) leaves &nbsp;&nbsp; C) glucose &nbsp;&nbsp; D) oxygen |
| **Correct Answer** | **leaves** |
| **Source Grounding** | `Chlorophyll absorbs sunlight in leaves.` |
| **Audit Status** | Verified against source transcript (100% ground rate) |

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/multilingual-lecture-notes-quiz.git
cd multilingual-lecture-notes-quiz
```

### 2. Create and Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
Install the core application requirements:
```bash
pip install -r requirements.txt
```

*(Optional)* To enable local faster-whisper ASR and BharatGen Param-1 generative summaries:
```bash
pip install -r requirements-models.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Evaluation & Benchmark Results

The benchmark suite in `evaluate.py` quantitatively evaluates **30 diverse lecture passages** across Computer Science, Biology, Physics, Economics, Civics, and Earth Science (`evaluation_cases.csv`).

### Run the Evaluation
```bash
python evaluate.py
```

### Quantitative Metrics:
- **Test Passages:** 30 domain cases
- **Mean Gold-Term Note Coverage:** `92.7%` *(Proportion of benchmark gold keyphrases retained in the extracted notes)*
- **Quiz Answer Source-Grounding:** `100.0%` *(Rate at which quiz answers are strictly present in their displayed source sentences)*

> **Note on Evaluation:** These deterministic smoke tests evaluate information retention and provenance. Word Error Rate (WER) is not bundled due to the absence of paired audio-human reference corpora; independent speech benchmark datasets should be used for acoustic evaluations.

---

## 🔍 Failure Analysis & Limitations

- **Extractive Sentence Selection:** Frequency-based ranking favors high-density passages and may occasionally omit low-frequency but critical transitional concepts.
- **Cloze Blank Selection:** Term selection targets longer alphabetic words; in highly specialized contexts, it may select a descriptive adjective rather than a noun concept.
- **Distractor Plausibility:** Distractors are drawn from the remaining vocabulary of the lecture. In short transcripts with limited vocabulary, distractors may occasionally belong to different syntactic categories.
- **Script Segmentation:** Sentence segmentation relies on standard sentence terminators (`.`, `!`, `?`, `।`). Transcripts lacking appropriate punctuation may produce long compound sentences.
- **Error Propagation:** Downstream notes and cloze questions reflect the transcript directly; uncorrected ASR transcription errors will naturally propagate into notes and quiz blanks.

---

## 📁 Repository Structure

```text
├── app.py                   # Streamlit web application & interactive UI
├── core.py                  # Extractive note summarization & cloze quiz engine
├── evaluate.py              # 30-case benchmark evaluation script
├── evaluation_cases.csv     # 30 domain lecture passages with gold-standard terms
├── requirements.txt         # Core dependencies (Streamlit, compatible ASR libraries)
├── requirements-models.txt  # Optional neural model dependencies (faster-whisper, transformers, torch)
├── .gitignore               # Ignored environments, model checkpoints, and audio buffers
└── README.md                # Project documentation
```

---

## 🎯 Coursework Rubric Mapping

- **Frontend & User Experience:** Streamlit interface providing audio upload, real-time transcript editing, one-click note downloads, and interactive multiple-choice quiz submission with immediate feedback.
- **GenAI / Speech Integration:** Integrated local CPU-int8 `faster-whisper` ASR and optional abstractive note drafting via the `BharatGen Param-1` Hugging Face pipeline.
- **Factual Grounding & Auditing:** Default pipeline is 100% extractive and provenance-linked; every question explicitly displays its source sentence for auditing.
- **Empirical Evaluation:** 30 benchmark cases measured across gold-term coverage (92.7%) and source-grounding rate (100.0%) with comprehensive failure analysis.

---

## 📚 References & Acknowledgments

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — Highly optimized Whisper inference using CTranslate2
- [BharatGen Param-1](https://huggingface.co/bharatgenai/Param-1) — Pretrained Indic foundation model
- [AI4Bharat IndicConformer](https://github.com/AI4Bharat/IndicConformerASR) — Multilingual speech recognition for Indic languages
- [Streamlit](https://streamlit.io/) — Python application framework
