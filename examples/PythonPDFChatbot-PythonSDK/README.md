# Dabarqus Python Chatbot UI Example: Python SDK

This is an example chatbot program using Dabarqus via the [Python SDK](https://pypi.org/project/dabarqus/) to chat with your PDFs. It using Gradio for the frontend UI, and Ollama to provide the LLMs.   

There is another version of this demo that uses the REST API that can be found under `PythonPDFChatbot-RESTAPI`

## Features

- Interactive chat interface
- Memory bank selection
- Integration with Dabarqus API for semantic search
- Powered by Gradio for easy web deployment

## Prerequisites

- Python 3.8+
- Dabarqus server running and accessible
- [Dabarqus Python SDK](https://pypi.org/project/dabarqus/)
- [Ollama](https://ollama.com/download)

## Installation

### Dabarqus Service
Important: This chatbot requires Dabarqus to be installed and running on your machine. Before using this chatbot, please ensure that you have:

- Downloaded and installed Dabarqus  
- Started the Dabarqus service on your machine  

The chatbot communicates with the Dabarqus service via its API, so having Dabarqus running is essential for the chatbot to function correctly.
Once Dabarqus is set up and running, you can proceed with using this chatbot. For more information on how to start and manage the Dabarqus service, please refer to the [Dabarqus quick start](https://github.com/electricpipelines/barq?tab=readme-ov-file#quick-start).

### Chatbot installation

1. Clone the repository:   
`git clone https://github.com/electricpipelines/barq.git`    
`cd DabarqusChatbotUI/examples/PythonPDFChatbot-RESTAPI`   

2. Create a virtual environment (**optional but recommended**):  
`python -m venv venv`  
`source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'`  

3. Install the required dependencies:  
`pip install -r requirements.txt`

### Ollama
If you have not already download and set
1. Follow the installion instructions on the [Ollama](https://ollama.com/download)  

2. After installation, install at least LLM:  
`ollama pull llama3`

## Running the Application
1. Ensure your Dabarqus server is running and accessible.  
2. Start the Gradio application:  
`python app.py`   
3. The application will start and provide a local URL (usually http://127.0.0.1:7860).   
4. Open this URL in your web browser to access the chat interface.

### Memory Banks
You need a **memory bank** to chat with your PDFs. You have a few options:   
- Run the CreatingAMemoryBank example.   
- Create a memory bank through the admin interface:   
    1. Open the Dabarqus admin interface (typically at `http://localhost:6568/admin`).  
    2. Navigate to the "Memory Banks" section.   
    3. You should see your newly created memory bank (e.g., "MyNewRecipeBook") listed.  

## File Structure

- `app.py`: Main application file containing the Gradio interface
- `templates/`: Directory containing prompt templates
- `sample_prompt.md`: Sample prompt file for the chatbot