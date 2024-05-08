from openai import OpenAI
 
client = OpenAI(api_key="your_api_key")

 
assistant = client.beta.assistants.create(
  name="Financial Analyst Assistant",
  instructions="당신은 유능한 노무사입니다. 제공한 파일에 접근 할 권한이 있으며 대답은 한국어를 사용합니다. 제공한 파일들의 법률을 참고하여 대답해주세요.",
  model="gpt-3.5-turbo",
  tools=[{"type": "file_search"}],
)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Financial Statements")
 
# Ready the files for upload to OpenAI
file_paths = ["files/고용보험법_20230701.pdf", "files/국민건강보험법_20240507.pdf" , "files/국민연금법_20240118.pdf"
              , "files/근로기준법_20211119.pdf" , "files/보험료징수_20240101.pdf" , "files/산업재해보상보험법_20240209.pdf"]
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
 
# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)


assistant = client.beta.assistants.update(
  assistant_id="asst_8fudQGCXlLgwDNYWKb4w1mNV",
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

empty_thread = client.beta.threads.create()
print(empty_thread)

 