"""Dependency-free extractive notes and quiz baseline."""
import re

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?।])\s+", text) if len(s.split()) >= 5]

def make_notes(text, count=6):
    ss=sentences(text)
    if not ss: return []
    words=re.findall(r"\w+", text.lower())
    stop=set("the a an and or but is are was were of to in for on with by from as that this it we they you".split())
    freq={}
    for w in words:
        if w not in stop and len(w)>2: freq[w]=freq.get(w,0)+1
    scored=[]
    for i,s in enumerate(ss):
        terms=[w.lower() for w in re.findall(r"\w+",s)]
        score=sum(freq.get(w,0) for w in terms)/max(1,len(terms)) + (0.15 if i==0 else 0)
        scored.append((score,i,s))
    selected=sorted(scored,reverse=True)[:min(count,len(ss))]
    return [s for _,_,s in sorted(selected,key=lambda x:x[1])]

def make_quiz(text, limit=5):
    ss=sentences(text)
    candidates=[]
    for s in ss:
        terms=[w for w in re.findall(r"[A-Za-z][A-Za-z-]{4,}",s) if w.lower() not in {"because","therefore","however","important"}]
        if terms: candidates.append((s,terms[-1]))
    out=[]
    all_terms=list(dict.fromkeys(w for _,a in candidates for w in re.findall(r"[A-Za-z][A-Za-z-]{4,}",text) if w.lower()!=a.lower()))
    for idx,(s,answer) in enumerate(candidates[:limit],1):
        q=re.sub(re.escape(answer), "________", s, count=1, flags=re.I)
        distractors=[]
        for w in all_terms:
            if w.lower()!=answer.lower() and w.lower() not in [d.lower() for d in distractors]: distractors.append(w)
            if len(distractors)==3: break
        opts=[answer]+distractors[:3]
        if len(opts)<4: opts += [f"Option {i}" for i in range(len(opts)+1,5)]
        shift=idx%4
        opts=opts[shift:]+opts[:shift]
        out.append({"question":q,"options":opts,"answer":answer,"source":s})
    return out
