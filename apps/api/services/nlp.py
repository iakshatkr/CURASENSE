from sentence_transformers import SentenceTransformer, util
import json
import os

class SymptomNLP:
    def __init__(self):
        # FAST & lightweight
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Load KB
        kb_path = os.path.join(os.path.dirname(__file__), "../../..", "packages/kb/conditions.json")
        with open(kb_path, "r") as f:
            self.conditions = json.load(f)

        # Precompute embeddings
        self.condition_descriptions = [c["description"] for c in self.conditions]
        self.condition_names = [c["name"] for c in self.conditions]

        # Embed descriptions (main similarity)
        self.description_embeddings = self.model.encode(
            self.condition_descriptions,
            convert_to_tensor=True
        )

        # Embed condition names (for zero-shot)
        self.name_embeddings = self.model.encode(
            self.condition_names,
            convert_to_tensor=True
        )

    def rank(self, user_text: str):
        # Encode user text once
        user_emb = self.model.encode(user_text, convert_to_tensor=True)

        # Embedding Similarity (Descriptions)
        desc_scores = util.cos_sim(user_emb, self.description_embeddings)[0]

        # Zero-shot similarity (Condition names)
        name_scores = util.cos_sim(user_emb, self.name_embeddings)[0]

        combined = []
        for idx, (d_score, n_score) in enumerate(zip(desc_scores, name_scores)):
            final_score = float(0.7 * d_score + 0.3 * n_score)

            combined.append({
                "name": self.conditions[idx]["name"],
                "similarity_score": float(d_score),
                "zero_shot_score": float(n_score),
                "final_score": final_score,
                "rationale": self.conditions[idx]["description"]
            })

        combined = sorted(combined, key=lambda x: x["final_score"], reverse=True)
        return combined[:5]
