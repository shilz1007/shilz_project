import yaml
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from llama_index.llms.nvidia import NVIDIA

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
llm_synthetic = data['llm_synthetic']

dotenv_path = env_path
load_dotenv(dotenv_path)
api_key = os.environ.get("NVIDIA_API_KEY_DATA")

f_path = ''#submit folder path


def create_data(api_key,base_url,llm_synthetic,user_prompt):
    my_model = llm_synthetic
    key = api_key
    url = base_url
    client = OpenAI(base_url=url,api_key=key)
    
    completion = client.chat.completions.create(
        model= my_model,
        messages=[{"role":"user","content":user_prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=2048,
        stream=False
        )
    text = completion.choices[0].message.content       
    return text

def write_out(f_path,resp):
    final_file = f"{f_path}\\car_wash_North_Kol.txt"
    
    if len(resp) == 0:
        print("length of response is 0")
    else:    
        with open(final_file,"w") as f:
            f.write(resp + "\n")
        print("file written successfully")    

def get_user(path):
    with open(path, 'r') as file:
        content = file.read()
    return content

in_file = ''#submit user input
user_prompt = get_user(in_file)
#print(user_prompt)
"""
sample_user_prompt = "
You have to write the names and details of 100 automobile spare parts stores. Please carefully go through the below requirements and the rules and then create the data.
The creation should strictly follow the Requirements and the Rules.
Requirements -
1. Name of the stores. The name should be such that it is easily identifiable as an automobile store.
2. Phone number of the store - the phone number should be 10 digits starting with 98
3. Address of the store - the address should be spread across the city of Kolkata which is the capital of West Bengal.
4. Spare parts of the cars available. It should only have car company name like Maruti Suzuki ,Hyundai, Tata.
5. Every automobile store should have reviews by the user. The reviews should be realistic and a combination of both positive and negative.
Rules for spare parts of the cars available -
1. The 100 stores should be spread across Kolkata which is the capital of West Bengal, a state in India.
2. Each store should contain parts of different car companies. The rules for that are present below :-
	. 80% stores should have the spare parts of the cars of Hyundai, Tata, Mahindra and Maruti Suzuki, Renault, Nissan
	. 5% stores should only have parts of Mercedes.
	. 5% stores should only have parts of BMW. 
	. 10% stores should only have spare parts of MG Comet, PMV and Strom 
"

"""
resp = create_data(api_key,base_url,llm_synthetic,user_prompt)
write_out(f_path,resp)






