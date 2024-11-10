import pandas as pd
import llama_index
from llama_index.core import SimpleDirectoryReader 
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.json import JSONReader

data_path = ""#submit folder path
#json_file_path = 
class dataProcessing:
    def __init__(self,path):
        self.path = path    

    def load_data(self):
        self.reader = SimpleDirectoryReader(input_dir = self.path,filename_as_id=True).load_data()  
            
    def chunk_documents(self):
        node_parser = SentenceSplitter(chunk_size = 1024, chunk_overlap=50)
        self.output_chunks = node_parser.get_nodes_from_documents(self.reader)
        return self.output_chunks
    
    def run_data(self):
        self.load_data()
        final_nodes = self.chunk_documents()    
        #print(len(final_nodes))
        return final_nodes

if __name__ == "__main__":
    process_data = dataProcessing(data_path)
    out_nodes = process_data.run_data()
    print(len(out_nodes))
    