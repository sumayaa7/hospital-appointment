from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
VECTOR_DIR = BASE_DIR / "vector_store"


def load_documents():
    docs = []
    if DOCS_DIR.exists():
        md_loader = DirectoryLoader(
            str(DOCS_DIR),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        txt_loader = DirectoryLoader(
            str(DOCS_DIR),
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        pdf_loader = DirectoryLoader(str(DOCS_DIR), glob="**/*.pdf", loader_cls=PyPDFLoader)
        docs.extend(md_loader.load())
        docs.extend(txt_loader.load())
        docs.extend(pdf_loader.load())
    return docs


def main():
    documents = load_documents()
    if not documents:
        raise RuntimeError("No documents found in ./docs")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    VECTOR_DIR.mkdir(exist_ok=True)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DIR),
        collection_name="hospital_docs",
    )

    print(f"Indexed {len(chunks)} chunks into {VECTOR_DIR}")


if __name__ == "__main__":
    main()
