from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.docstore import InMemoryDocstore  # ✅ Add this
import os
import faiss

class VectorStroreClient:
    def __init__(self, db_path="faiss_db"):
        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.db_path = db_path

        if os.path.exists(db_path):
            self.db = FAISS.load_local(db_path, self.embedding, allow_dangerous_deserialization=True)
        else:
            dim = len(self.embedding.embed_query("temp"))
            index = faiss.IndexFlatL2(dim)
            self.db = FAISS(
                embedding_function=self.embedding,
                index=index,
                docstore=InMemoryDocstore({}),  # ✅ Correct fix
                index_to_docstore_id={}
            )

    def add_speech(self, speaker, speech_text, metadata=None):
        doc = Document(page_content=speech_text, metadata={"speaker": speaker, **(metadata or {})})
        self.db.add_documents([doc])
        self.db.save_local(self.db_path)

    def retrieve_similar(self, query, top_k=3):
        return self.db.similarity_search(query, k=top_k)

    def get_all_documents(self):
        return self.db.similarity_search("", k=100)
