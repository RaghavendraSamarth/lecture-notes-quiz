"""Quantitative smoke evaluation: summary keyword coverage and quiz/source grounding."""
import csv
from core import make_notes,make_quiz

rows=list(csv.DictReader(open("evaluation_cases.csv",encoding="utf-8-sig")))
coverage=[]; quiz_ground=[]
for r in rows:
    notes=" ".join(make_notes(r["transcript"])).lower()
    terms=[x.lower() for x in r["gold_terms"].split(";")]
    coverage.append(sum(t in notes for t in terms)/len(terms))
    qs=make_quiz(r["transcript"])
    quiz_ground.append(sum(q["answer"].lower() in q["source"].lower() for q in qs)/max(1,len(qs)))
print(f"cases={len(rows)}; mean gold-term note coverage={sum(coverage)/len(coverage):.1%}; quiz answer source-grounding={sum(quiz_ground)/len(quiz_ground):.1%}")
print("Metrics are deterministic prototype smoke checks, not human ratings of note quality or educational validity.")
