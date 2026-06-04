from sentence_transformers import SentenceTransformer

model = None


def load_model():
    global model

    if model is None:
        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )


def get_embedding(text):

    load_model()

    return model.encode(
        text
    ).tolist()