RED_FLAGS = {
    "chest pain": "Possible cardiac emergency",
    "slurred speech": "Possible stroke",
    "unable to breathe": "Respiratory emergency",
    "severe abdominal pain": "Possible acute abdomen",
    "loss of consciousness": "Neurological emergency"
}

def detect_red_flags(text: str):
    hits = []
    for phrase, reason in RED_FLAGS.items():
        if phrase in text.lower():
            hits.append({"phrase": phrase, "reason": reason})
    return hits
