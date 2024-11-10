from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.nvidia import NVIDIA
from llama_index.embeddings.openai import OpenAIEmbedding
from openai import OpenAI
from dotenv import load_dotenv
import DbSetup
import time
import yaml,os
import gradio as gr



with open(os.path.join(os.path.dirname(__file__),'config_setting.yaml'),'r') as file:
    data = yaml.safe_load(file)

base_url = data['base_url']
car_parts_path = data['car_parts_path']
cars_wash_path = data['car_wash_path']
db_name = data['db_name']
data_path = data['data_path']
llm = data['llm']
embed = data['embedd_model']
env_path = data['env_path']
db_name = 'db2'
db_path = 'C:\Shilz\Project\Backend\db2'
dotenv_path = env_path
load_dotenv(dotenv_path)
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
embed_instance = OpenAIEmbedding()

def setup_index(db_name,db_path,embed_instance,llm,data_path):
    new_index = DbSetup.setup_DB(db_name,db_path,embed_instance,llm,data_path)
    vector_index = new_index.retrieve_db()
    retriever = VectorIndexRetriever(index=vector_index,similarity_top_k=2)
    response_synthesizer = get_response_synthesizer(
    response_mode="compact",
    )
    query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,)
    return query_engine
query_engine = setup_index(db_name,db_path,embed_instance,llm,data_path)

def query_function(user_query):
    response = query_engine.query(user_query)
    return response

chat_history = []
def q_function(user_input):
    global chat_history
    chat_history.append({"user": user_input})
    for response_piece in generate_streaming_response(query_engine, user_input, chat_history):
         chat_history[-1]["bot"] = chat_history[-1].get("bot", "") + response_piece
         formatted_history = format_chat_history(chat_history)
         yield formatted_history

def generate_streaming_response(query_engine, user_input, history):
    # Simulate streaming by breaking the response into parts
    full_response = query_engine.query(user_input, history=history)
    for response_piece in full_response.split():
        yield response_piece + " " 
        time.sleep(0.1) 

def format_chat_history(chat_history):
    return "\n".join([f"User: {h['user']}\nBot: {h.get('bot', '')}" for h in chat_history])

def create_gradio_ui():
    with gr.Blocks(theme=gr.themes.Default(primary_hue=gr.themes.colors.green, secondary_hue=gr.themes.colors.yellow)) as demo:
        gr.Markdown("### Car Product Knowledge Q&A")
        with gr.Row():
            gr.Image("C:\\Shilz\\Project\\Backend\\Data_Creation\\image (1).png", show_label=False, show_download_button=False, interactive=False, show_fullscreen_button=False,width=300,height=300)
            gr.Image("C:\\Shilz\\Project\\Backend\\Data_Creation\\image (2).png", show_label=False, show_download_button=False, interactive=False, show_fullscreen_button=False,width=300,height=300)
            gr.Image("C:\\Shilz\\Project\\Backend\\Data_Creation\\image.png", show_label=False, show_download_button=False, interactive=False, show_fullscreen_button=False,width=300,height=300)
        with gr.Row():
            user_input = gr.Textbox(placeholder="Ask a question about car products...", label="Question")
            output = gr.Textbox(label="Answer", lines=10)
        user_input.submit(query_function, inputs=user_input, outputs=output)
    return demo


def create_gradio_ui_main():
    with gr.Blocks() as demo:
        gr.Markdown("### Car Product Knowledge Q&A")  # Display a title
        with gr.Row():
            gr.Image("C:\\Shilz\\Project\\Backend\\Data_Creation\\image (1).png",show_label=False,show_download_button=False,interactive=False,show_fullscreen_button=False)
            gr.Image("C:\\Shilz\\Project\\Backend\\Data_Creation\\image (2).png",show_label=False,show_download_button=False,interactive=False,show_fullscreen_button=False)
            gr.Image("C:\\Shilz\\Project\\Backend\\Data_Creation\\image.png",show_label=False,show_download_button=False,interactive=False,show_fullscreen_button=False)  
        with gr.Row():
            user_input = gr.Textbox(placeholder="Ask a question about car products...", label="Question")
            output = gr.Textbox(label="Answer")
        user_input.submit(q_function, inputs=user_input, outputs=output)
    return demo

demo = create_gradio_ui()
demo.launch(share=True)