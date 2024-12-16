import os
import openai
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, 
    SimpleField, 
    SearchableField,
    SearchFieldDataType, 
    VectorField, 
    VectorSearchAlgorithmConfiguration,
    VectorSearch
)
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
FORM_RECOGNIZER_ENDPOINT = os.getenv("FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")

OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE", "azure")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2023-05-15")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME", "my-vector-index")

STORAGE_ACCOUNT_URL = os.getenv("STORAGE_ACCOUNT_URL")
STORAGE_CONTAINER_NAME = os.getenv("STORAGE_CONTAINER_NAME")

EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_COMPLETION_MODEL = "gpt-4"  # Adjust if you have a different deployment name

openai.api_type = OPENAI_API_TYPE
openai.api_base = OPENAI_API_BASE
openai.api_version = OPENAI_API_VERSION
openai.api_key = OPENAI_API_KEY

# Authentication for Azure services
# If running locally and signed in with Azure CLI, DefaultAzureCredential should work.
# Otherwise, consider providing keys directly.
credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)

# Step 1: List and Download PDFs from Blob Storage
blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=credential)
container_client = blob_service_client.get_container_client(STORAGE_CONTAINER_NAME)

pdf_files = [b.name for b in container_client.list_blobs() if b.name.endswith(".pdf")]

local_files = []
for pdf in pdf_files:
    local_path = pdf.split("/")[-1]  # just take filename if folders are not involved
    with open(local_path, "wb") as f:
        data = container_client.download_blob(pdf)
        f.write(data.readall())
    local_files.append(local_path)

# Step 2: Extract Text Using Form Recognizer
document_analysis_client = DocumentAnalysisClient(FORM_RECOGNIZER_ENDPOINT, FORM_RECOGNIZER_KEY)
all_chunks = []
CHUNK_SIZE = 1000

def get_embedding(text):
    response = openai.Embedding.create(
        input=[text],
        engine=EMBEDDING_MODEL
    )
    return response['data'][0]['embedding']

for local_pdf_path in local_files:
    with open(local_pdf_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f)
    result = poller.result()

    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    # Step 3: Chunk the extracted text
    chunks = [extracted_text[i:i+CHUNK_SIZE] for i in range(0, len(extracted_text), CHUNK_SIZE)]

    # Label the chunks with a source (the PDF file they came from)
    for idx, c in enumerate(chunks):
        all_chunks.append({
            "id": f"{local_pdf_path}-{idx}",
            "content": c,
        })

# Step 4: Generate Embeddings for each chunk
for doc in all_chunks:
    doc["contentVector"] = get_embedding(doc["content"])

# Step 5: Create (if not exists) and Populate the Azure Cognitive Search Index
index_client = SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=credential)
search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=SEARCH_INDEX_NAME, credential=credential)

# We'll assume the embedding dimension is 1536 for text-embedding-ada-002
dimension = 1536

fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String),
    VectorField(name="contentVector", dimensions=dimension, searchable=True, 
                 vector_search_dimensions=dimension,
                 vector_search_configuration="my-vector-config")
]

vector_search = VectorSearch(
    algorithm_configurations=[
        VectorSearchAlgorithmConfiguration(name="my-vector-config", kind="hnsw")
    ]
)

index = SearchIndex(
    name=SEARCH_INDEX_NAME,
    fields=fields,
    vector_search=vector_search
)

# Create the index if it doesn't exist
try:
    index_client.create_index(index)
except Exception as e:
    print("Index likely already exists or another error occurred:", e)

# Upload documents
# If the index already contains data, consider merging/upserting or deleting old data first.
search_client.upload_documents(all_chunks)

# Step 6: Retrieval and QA function
def retrieve_relevant_chunks(query, top_k=3):
    q_emb = get_embedding(query)
    results = search_client.search(
        search_text="",
        vector={"value": q_emb, "fields": "contentVector", "k": top_k},
        select=["content"]
    )
    returned_chunks = [doc["content"] for doc in results]
    return returned_chunks

def answer_question(query):
    relevant_chunks = retrieve_relevant_chunks(query)
    context = "\n".join(relevant_chunks)
    prompt = f"Use the following context to answer the question.\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    response = openai.ChatCompletion.create(
        engine=CHAT_COMPLETION_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that uses only the given context to answer questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    return response['choices'][0]['message']['content']

# Example query
question = "What are the main topics covered across these documents?"
answer = answer_question(question)
print("Answer:", answer)