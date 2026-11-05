"""Lecture-to-notes and quiz generator with optional local ASR and Param-1."""
import re
import streamlit as st
from core import make_notes, make_quiz

st.set_page_config(page_title="Lecture Notes and Quiz", page_icon="🎓", layout="wide")
st.title("Multilingual Lecture-to-Notes & Quiz Generator")
st.caption("Transcribe a lecture, create concise notes, and generate five source-grounded multiple-choice questions.")

def transcribe(audio):
    try:
        import av
        # Ensure compatibility across PyAV versions by stripping deprecated kwargs
        _orig_open = av.open
        def _compat_open(*args, **kwargs):
            kwargs.pop("metadata_errors", None)
            return _orig_open(*args, **kwargs)
        av.open = _compat_open

        from faster_whisper import WhisperModel
        model=WhisperModel("small", device="cpu", compute_type="int8")
        segments, info=model.transcribe(audio, vad_filter=True)
        return " ".join(s.text.strip() for s in segments), f"faster-whisper small, detected {info.language} ({info.language_probability:.0%} confidence)"
    except Exception as e:
        return "", f"ASR unavailable: {type(e).__name__} ({e}). Paste a transcript below."

@st.cache_resource(show_spinner="Loading BharatGen Param-1 (first run may download model weights)...")
def load_param1():
    from transformers import pipeline
    return pipeline("text-generation", model="bharatgenai/Param-1", trust_remote_code=True)

st.subheader("1. Provide a lecture")
uploaded=st.file_uploader("Upload audio (optional)", type=["wav","mp3","m4a","flac"])
if uploaded and st.button("Transcribe audio"):
    with open("lecture_upload.tmp","wb") as f: f.write(uploaded.getbuffer())
    text, note=transcribe("lecture_upload.tmp")
    st.session_state["transcript"]=text
    st.info(note)
transcript=st.text_area("Transcript (paste/edit here)", value=st.session_state.get("transcript",""), height=220,
                        placeholder="Paste a transcript in English or an Indic language. The extractive baseline preserves the transcript language.")
with st.expander("Model configuration"):
    use_param=st.checkbox("Generate an additional note draft with BharatGen Param-1 (optional; large model download)",value=False)
    st.write("Audio transcription attempts faster-whisper small locally (CPU int8). Param-1 follows the Hugging Face model-card Transformers pipeline. Both optional model paths may require downloads and substantial memory. Extractive notes and quiz work offline.")

if st.button("Generate notes and quiz", type="primary"):
    if not transcript.strip(): st.warning("Provide audio or a transcript first.")
    else:
        notes=make_notes(transcript)
        quiz=make_quiz(transcript)
        st.session_state["notes"]=notes
        st.session_state["quiz"]=quiz
        st.session_state["source"]=transcript
        st.session_state["param_notes"]=""
        if use_param:
            prompt=("Summarize the lecture transcript below as 4 concise factual bullet points. "
                    "Use only information in the transcript. If a detail is unclear, omit it.\n\n"
                    f"TRANSCRIPT:\n{transcript}\n\nNOTES:")
            try:
                generated=load_param1()(prompt,max_new_tokens=220,do_sample=False)
                st.session_state["param_notes"]=generated[0]["generated_text"][len(prompt):].strip()
            except Exception as e:
                st.warning(f"Param-1 could not load or generate ({type(e).__name__}); extractive notes remain available.")

if "notes" in st.session_state:
    st.subheader("2. Lecture notes")
    st.write("\n".join(f"- {x}" for x in st.session_state["notes"]) if st.session_state["notes"] else "Not enough sentence text to summarize.")
    if st.session_state.get("param_notes"):
        st.subheader("Optional BharatGen Param-1 note draft")
        st.write(st.session_state["param_notes"])
        st.caption("Compare generated notes with the transcript; the prompt requests grounding but does not guarantee it.")
    st.download_button("Download notes", "\n".join(st.session_state["notes"]), file_name="lecture_notes.txt")
    st.subheader("3. Five-question quiz")
    if len(st.session_state["quiz"]) < 5:
        st.info(f"The transcript contains only {len(st.session_state['quiz'])} suitable factual sentences; add more transcript text for five questions.")
    for i,q in enumerate(st.session_state["quiz"],1):
        st.markdown(f"**{i}. {q['question']}**")
        st.radio("Choose one",q["options"],key=f"answer_{i}",label_visibility="collapsed")
    if st.button("Check answers"):
        correct=0
        for i,q in enumerate(st.session_state["quiz"],1):
            chosen=st.session_state.get(f"answer_{i}")
            ok=chosen==q["answer"]
            correct+=ok
            st.write(f"{i}. {'Correct' if ok else 'Review'} — answer: {q['answer']}. Source: {q['source']}")
        st.success(f"Score: {correct}/{len(st.session_state['quiz'])}")
    st.caption("Quiz generation uses extractive cloze questions with source sentences shown for audit. Check technical accuracy before assigning.")
