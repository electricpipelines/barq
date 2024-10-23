# Create a Memory Bank Example

This example uses the [Dabarqus Python SDK](https://pypi.org/project/dabarqus/) to store pdfs of your choice into a memory bank (semantic index). With this memory bank, you can retrieve relevant information using Dabarqus. It is recommended to run this example first so that you have a working memory bank before you try out other examples.

## Prerequisites

- Python 3.8+
- Dabarqus server running and accessible

## Setup

1. Create a virtual enviroment (**optional, but recommended**):  
    `python -m venv ./venv`  
    **Mac or Linux**:  
    `source venv/bin/activate`
    **Windows**:  
    `venv\Scripts\activate.ps1`
2. Install the required Python libraries:  
    `python -m pip install requirements.txt`  
3. Run the app:  
    `python store_files.py`  

## Sample Usage  
Run the following:  
`python ./store_files.py --memory-bank MyNewRecipeBook --input-path ./recipes/`  

This will store the contents of `./recipes`, an list of included recipes, into a new memory bank called `MyNewRecipeBook`.  

After running the script:
1. You'll see progress messages as each file is processed and added to the memory bank.
2. Once complete, you'll receive a confirmation message that the memory bank has been created.

## Verifying the Memory Bank

To verify that your memory bank was created successfully:
1. Open the Dabarqus admin interface (typically at `http://localhost:6568/admin`).
2. Navigate to the "Memory Banks" section.
3. You should see your newly created memory bank (e.g., "MyNewRecipeBook") listed.