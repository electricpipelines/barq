# Dabarqus

**Dabarqus** &ndash; Zero to RAG in minutes. Dabarqus is a stand alone application that implements a complete RAG solution. It is designed to be easy to use and easy to integrate with your existing applications. Dabarqus includes a REST API, a command-line interface, and an admin dashboard.

## Table of Contents

1. [Quick Start](#quick-start)
   - [Ubuntu](#ubuntu)
   - [macOS](#macos)
   - [Windows](#windows)
2. [Features](#features)
3. [Barq - Command-line Interface](#barq---command-line-interface-to-dabarqus)
   - [Using with the CLI](#using-with-the-cli)
     - [Store](#store)
     - [Retrieve](#retrieve)
4. [API - REST Interface](#api---rest-interface-to-dabarqus)
   - [Using the API](#using-the-api)
5. [Examples](#examples)

## **Quick start**

### Ubuntu

Dabarqus works on CPU only, or can use NVIDIA CUDA for higher performance. For the CUDA (cublas) version, you will need to install the NVIDIA driver. The CPU version does not require any additional software. Note that to use the CUDA version, you will need to have an NVIDIA GPU with CUDA support, and to download the CUDA version of Dabarqus.

0. To install NVIDIA drivers on Ubuntu:

    ```bash
    sudo ubuntu-drivers install
    ```

1. Unzip the Dabarqus file into a folder

    ```bash
    unzip Dabarqus-linux-DOWNLOADED_VERSION.zip
    cd Dabarqus-linux-DOWNLOADED_VERSION
    chmod +x ./bin/*
    ./bin/barq service install
    ```

2. Open a browser and go to `http://localhost:6568/admin`

### macOS

1. Unzip the Dabarqus file into a folder

    ```bash
    unzip Dabarqus-linux-DOWNLOADED_VERSION.zip
    cd Dabarqus-linux-DOWNLOADED_VERSION
    ./bin/barq service install
    ```

2. Open a browser and go to `http://localhost:6568/admin`

### Windows

1. Double click the Dabarqus-windows-DOWNLOADED_VERSION.exe and install
2. Double click the Dabarqus icon

## Features

1. **Ingest documents, databases, and APIs**: Ingest diverse data sources like PDFs*, emails, and raw data.
   - No matter where your data resides, Dabarqus can make it available to your LLM

2. **LLM-Style Prompting**: Use simple, LLM-style prompts when speaking to your memory banks.
   - Dabarqus will retrieve relevant data using the same prompt you give your LLM
   - No need to construct special queries or learn a new query language

3. **REST API**: Comprehensive control interface for downloading models, prompting semantic indexes, and even LLM inference.
   - REST is a standard interface that enjoys wide adoption, so your team doesn't need to learn a new, complex system
   - Allows comprehensive integration with existing development tools for easy adoption

4. **Multiple Semantic Indexes (Memory Banks)**: Group your data into separate semantic indexes (memory banks).
   - Keep your data organized by subject matter, category, or whatever grouping you like
   - Memory banks are portable, so you can create and use them wherever you like

5. **SDKs**: Native SDKs in [Python](https://pypi.org/project/dabarqus/) and [Javascript](https://www.npmjs.com/package/dabarqus).
   - Easily integrates with Python and Javascript projects

6. **LLM-Friendly Output**: Produces LLM-ready output that works with ChatGPT, Ollama, and any other LLM provider
   - Works seamlessly with the LLM of your choice

7. **Admin Dashboard**: Monitor performance, test memory banks, and make changes in an easy-to-use UI
   - Easy access to Dabarqus features
   - Monitor app performance with real-time graphs

8. **Mac, Linux, and Windows Support**: Runs natively with zero dependencies on all platforms: MacOS (Intel or Metal), Linux, and Windows (CPU or GPU)
   - Runs on whatever platform you use

9. **LLM Inference**: Chat with LLM models right through the Dabarqus API/SDKs
   - Built-in chatbot capabilities for use in your applications

*Only PDFs supported for the [community edition](dabarqus.com).

## Barq - Command-line interface to Dabarqus

To install: `barq service install`

To uninstall: `barq service uninstall`

### Using with the CLI

#### Store

Usage: `barq store --input-path <path to folder> --memory-bank "<memory bank name>"`

Example: `barq store --input-path C:\docs --memory-bank documents`

#### Retrieve

Usage: `barq retrieve --memory-bank "<memory bank name>"`

- Example: `barq retrieve --memory-bank documents`
- Example: `barq retrieve --memory-bank documents --query "Tell me about the documents" --query-limit 3`
             This will display three answers to the query from the 'documents' memory bank

## API - REST interface to Dabarqus

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | /health or /api/health | Check the health status of the service | None |
| GET | /admin/* | Serve the admin application | None |
| GET | /odobo/* | Serve the Odobo application | None |
| GET | /api/models | Retrieve available AI models | None |
| GET | /api/model/metadata | Get metadata for a specific model | `modelRepo`, `filePath` (optional) |
| GET | /api/downloads | Get information about downloaded items | `modelRepo` (optional), `filePath` (optional) |
| GET | /api/downloads/enqueue | Enqueue a new download | `modelRepo`, `filePath` |
| GET | /api/downloads/cancel | Cancel a download | `modelRepo`, `filePath` |
| GET | /api/downloads/remove | Remove a downloaded item | `modelRepo`, `filePath` |
| GET | /api/inference | Get information about inference items | `alias` (optional) |
| GET | /api/inference/start | Start an inference | `alias`, `modelRepo`, `filePath`, `address` (optional), `port` (optional), `contextSize` (optional), `gpuLayers` (optional), `chatTemplate` (optional) |
| GET | /api/inference/stop | Stop an inference | `alias` |
| GET | /api/inference/status | Get the status of an inference | `alias` (optional) |
| GET | /api/inference/reset | Reset an inference | `alias` |
| GET | /api/inference/restart | Restart the current inference | None |
| GET | /api/hardware or /api/hardwareinfo | Get hardware information | None |
| GET | /api/silk | Get memory status | None |
| GET | /api/silk/enable | Enable memories | None |
| GET | /api/silk/disable | Disable memories | None |
| GET | /api/silk/memorybanks | Get memory banks information | None |
| GET | /api/silk/memorybank/activate | Activate a memory bank | `memorybank` |
| GET | /api/silk/memorybank/deactivate | Deactivate a memory bank | `memorybank`, `all` |
| GET | /api/silk/query | Perform a semantic query | (Parameters handled by Silk retriever) |
| GET | /api/silk/health | Check the health of the Silk retriever | None |
| GET | /api/silk/model/metadata | Get model metadata from the Silk retriever | (Parameters handled by Silk retriever) |
| GET | /api/shutdown | Initiate server shutdown | None |
| POST | /api/utils/log | Write to log | JSON body with log details |
| POST | /api/silk/embedding | Get an embedding from the Silk retriever | (Parameters handled by Silk retriever) |

### Using the API

- Example: `curl http://localhost:6568/api/silk/query?q=Tell%20me%20about%20the%20documents&limit=3&memorybank=docs`

## Examples

Examples of Dabarqus in action can be found in this repo under **examples**.

- PythonPDFChatbot-RESTAPI: An example chatbot program using Dabarqus via the REST API to chat with your PDFs.
- PythonPDFChatbot-PythonSDK: An example chatbot program using Dabarqus via the [Python SDK](https://pypi.org/project/dabarqus/) to chat with your PDFs.
- StoreFiles: A Python example of storing documents in to a memory bank (semantic index) using the Python SDK

### **Notes:**

1. Dabarqus Professional Edition is required for email, messaging and API support.
