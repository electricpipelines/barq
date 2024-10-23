import gradio as gr
import ollama
from retriever import retrieve_data, convert_prompt_to_retrieval_prompt
import requests
import json
import os
from datetime import datetime

def check_dependencies():
    errors = []
    
    # Check Ollama
    try:
        ollama.list()
    except Exception as e:
        errors.append(f"Ollama is not running or installed properly. Error: {str(e)}")
    
    # Check Dabarqus
    try:
        response = requests.get("http://localhost:6568/health")
        if response.status_code != 200:
            errors.append("Dabarqus is not responding properly.")
    except requests.RequestException:
        errors.append("Dabarqus is not running or installed properly.")
    
    return errors

def display_error_message(errors):
    if errors:
        error_msg = "The following errors occurred:\n" + "\n".join(errors)
        gr.Warning(error_msg)
        return gr.update(visible=True), error_msg
    return gr.update(visible=False), ""

with gr.Blocks(title="dabarqus") as demo:
    error_box = gr.Textbox(visible=False, label="Errors")

# Get available Ollama models
def get_ollama_models():
    try:
        models = ollama.list()
        return [model['name'] for model in models['models']]
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return ["llama3"]  # Default model if fetching fails


def get_memory_banks():
    url = "http://localhost:6568/api/silk/memorybanks"
    try:
        response = requests.get(url)
        response.raise_for_status()
        memory_banks = response.json()

        return [bank.get('name') for bank in memory_banks['SilkMemoryBanks'] if bank.get('name')]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching memory banks: {e}")
        return ["Default"]  # Return a default option if the API call fails


def chat_function(message, history, memory_bank, model, query_limit, retrieval_prompt_template, full_prompt_template):
    # Convert the user's message to a retrieval prompt
    retrieval_prompt = convert_prompt_to_retrieval_prompt(message, retrieval_prompt_template)
    
    # Retrieve data
    retrieved_data = retrieve_data(retrieval_prompt, memory_bank, int(query_limit))
    
    # Prepare the prompt for the LLM
    full_prompt = f"{full_prompt_template} : RAG_response {retrieved_data}, keywords: {retrieval_prompt}, original_prompt: {message}"
    
    # Use Ollama to generate a response
    response = ""
    stream = ollama.chat(
        model=model,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                  {"role": "user", "content": full_prompt}],
        stream=True,
    )
    
    for chunk in stream:
        response += chunk['message']['content']
        yield history + [("Human", message), ("AI", response)]


def save_conversation(history):
    if not history:
        gr.Warning("No conversation to save.")
        return None, gr.update(visible=False)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(history, f)
    
    gr.Info(f"Conversation saved as {filename}")
    return filename, gr.update(visible=True)

def toggle_load_file(file, chatbot):
    if file is None:
        # If no file is selected, just toggle visibility
        return gr.update(visible=True), chatbot
    
    try:
        with open(file.name, "r") as f:
            history = json.load(f)
        gr.Info("Conversation loaded successfully.")
        return gr.update(value=None, visible=False), history
    except json.JSONDecodeError:
        gr.Warning("Invalid JSON file. Please select a valid conversation file.")
    except Exception as e:
        gr.Warning(f"Error loading conversation: {str(e)}")
    
    return gr.update(value=None), chatbot
def show_load_file():
    return gr.update(visible=True)

def hide_load_file():
    return gr.update(visible=False)


def save_prompts(retrieval_prompt, full_prompt):
    prompts = {
        "retrieval_prompt": retrieval_prompt,
        "full_prompt": full_prompt
    }
    with open("custom_prompts.json", "w") as f:
        json.dump(prompts, f)
    gr.Info("Prompts saved successfully.")

def load_prompts():
    if os.path.exists("custom_prompts.json"):
        with open("custom_prompts.json", "r") as f:
            prompts = json.load(f)
        return prompts["retrieval_prompt"], prompts["full_prompt"]
    else:
        gr.Warning("No saved prompts found.")
        return None, None



def enable_input(choice):
    return gr.update(interactive=bool(choice)), gr.update(interactive=bool(choice))



with gr.Blocks(title="dabarqus") as demo:
    memory_banks = get_memory_banks()
    ollama_models = get_ollama_models()

    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("") # Empty markdown to take up space
        with gr.Column(scale=2):
            with gr.Row():
                save_button = gr.Button("Save", size="sm")
                load_button = gr.Button("Load", size="sm")
            file_output = gr.File(label="Saved Conversation", visible=False)
            file_input = gr.File(label="Load Conversation", file_types=[".json"], visible=False)

    with gr.Row():
        memory_bank = gr.Dropdown(
        choices=memory_banks,
        label="Select Memory Bank",
        value=None,
        allow_custom_value=False,
        info="Choose a memory bank to query for relevant information."
    )
        model_selection = gr.Dropdown(
            choices=ollama_models,
            label="Select Inference Model",
            value=ollama_models[0] if ollama_models else None,
            info="Select the Ollama model for inference. Make sure Ollama is installed and running."
        )



    query_limit = gr.Slider(minimum=1, maximum=50, value=10, step=1, label="Number of RAG results")
    
    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column(scale=4):
            msg = gr.Textbox(
                label="Type your message here",
                placeholder="Enter your question...",
                interactive=False,
                elem_classes="large-text-input"
            )
        with gr.Column(scale=1):
            submit = gr.Button("Send", interactive=False)

    with gr.Accordion("Advanced Settings", open=False):
        retrieval_prompt = gr.Textbox(
            label="Retrieval Prompt",
            placeholder="Enter the retrieval prompt...",
            lines=3,
            value="Take the user's prompt to create a prompt for a semantic database retriever. Only respond with a list of comma-separated keywords. DO NOT say anything before or after the keywords."
        )
        
        prompt_template = gr.TextArea(
            label="Prompt Template",
            placeholder="Enter the prompt template...",
            value="Use these results from your recipe catalog to form your answer (include the file reference in your answer if you use one)"
        )
        with gr.Row():
            save_prompts_btn = gr.Button("Save Prompts")
            load_prompts_btn = gr.Button("Load Prompts")
    clear = gr.Button("Clear Chat")
    
    memory_bank.change(enable_input, inputs=[memory_bank], outputs=[msg, submit])

    msg.submit(
    chat_function,
    inputs=[msg, chatbot, memory_bank, model_selection, query_limit, retrieval_prompt, prompt_template],
    outputs=[chatbot]
    )
    submit.click(
        chat_function,
        inputs=[msg, chatbot, memory_bank, model_selection, query_limit, retrieval_prompt, prompt_template],
        outputs=[chatbot]
    )
    clear.click(lambda: None, None, chatbot, queue=False)

    save_button.click(
        save_conversation,
        inputs=[chatbot],
        outputs=[file_output, file_output]
    )

    load_button.click(
        toggle_load_file,
        inputs=[file_input, chatbot],
        outputs=[file_input, chatbot]
    )
# Launch the app
if __name__ == "__main__":

    demo.launch()
    demo.load(lambda: display_error_message(check_dependencies()), outputs=[error_box])



# Styling
demo.style(
    """
    .large-text-input textarea {
        font-size: 16px !important;
    }
    .gradio-slider input[type="number"] {
        width: 80px;
    }
    /* Add these new styles */
    #component-22 {  /* Adjust this ID to match your save/load row */
        margin-top: -20px;  /* Reduce space above the save/load row */
    }
    #component-22 .gr-button {  /* Adjust this ID to match your save/load buttons */
        min-width: 60px;  /* Make buttons smaller */
        height: 30px;  /* Make buttons shorter */
    }

    .advanced-settings {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
    }
    
    .advanced-settings .gr-form {
        border: none;
        padding: 0;
    }
    """
)