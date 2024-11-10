from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext,ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.schema import QueryBundle
from llama_index.readers.json import JSONReader
from llama_index.core.node_parser import SentenceSplitter
from openai import OpenAI
import Data_processing
#from Data_embedding import final_nodes
import chromadb
import openai
import yaml
import os
import dotenv
from dotenv import load_dotenv
import logging
import sys

with open(os.path.join(os.path.dirname(__file__),'config_setting.yaml'),'r') as file:
    data = yaml.safe_load(file)

embedding_model = data['embedding_model']
env_path = data['env_path']
db_name = data['db_name']
data_path = data['data_path']
base_url = data['base_url']
llm = data['llm']
db_store = data['db_store']
embedd_model = data['embedd_model']
car_parts_path = data['car_parts_path']
car_Wash_path = data['car_wash_path']
json_folder = [car_parts_path,car_Wash_path]

db_name = 'db2'
db_path = 'C:\Shilz\Project\Backend\db2'



dotenv_path = env_path
load_dotenv(dotenv_path)
api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

embed_instance = OpenAIEmbedding()

def load_json(json_file_path):
    read_json = JSONReader(
            levels_back=0,
            collapse_length=False,
            ensure_ascii=False,
            is_jsonl=False,
            clean_json=False
        )
    documents = read_json.load_data(input_file=json_file_path)
    node_parser = SentenceSplitter(chunk_size = 1024, chunk_overlap=50)
    output_chunks = node_parser.get_nodes_from_documents(documents)
    return output_chunks


class setup_DB():
   def __init__(self,db_name,db_path,embed_instance,llm,data_path):
      self.db_name = db_name
      self.db_path = db_path
      self.embedding_model = embed_instance
      self.llm = llm
      self.data_path = data_path
    
   def fetch_data(self):
        d_process = Data_processing.dataProcessing(self.data_path)
        self.output_nodes = d_process.run_data()

   def create_collection(self):
        chroma_client = chromadb.PersistentClient(path=self.db_path)
        chroma_collection = chroma_client.create_collection(self.db_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storageContext = StorageContext.from_defaults(vector_store=vector_store)
        vector_idx = VectorStoreIndex(self.output_nodes,storage_context=storageContext,embed_model = self.embedding_model)
        #print('data inserted successfully')
        return vector_idx
   def retrieve_db(self):
        db = chromadb.PersistentClient(path=db_path)
        chroma_collection = db.get_or_create_collection(self.db_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        vector_index = VectorStoreIndex.from_vector_store(vector_store,embed_model=self.embedding_model)
        #print('retrieved and index created')
        return vector_index
   def query_index(self,input,vector_index):
       query_engine = vector_index.as_query_engine(similarity_top_k=5)
       response = query_engine.query(input)
       return response
   def chat_index(self,input,vector_index):
       chat_engine = vector_index.as_chat_engine(similarity_top_k=5)
       response = chat_engine.chat(input)
       return response
   
if __name__ == "__main__":

   db_new = setup_DB(db_name,db_path,embed_instance,llm,data_path)
   db_new.fetch_data()
   #idx = db_new.create_collection()
   vector_index = db_new.retrieve_db()
   #for folder in json_folder:
   #    documents = load_json(folder)
   #     vector_index.insert_nodes(documents)
    
   #print("nodes inserted successfully")


   input = 'What are the braking part no for ?'
   response = db_new.query_index(input,vector_index)
   res = db_new.chat_index(input,vector_index)
   print(f"response from query engine:{response}")
   print(f"response from chat engine:{res}")
   for node in response.source_nodes:
       print(node.text)
   for n in res.source_nodes:
       print(n.text)    
       


   

   

            


   

   
