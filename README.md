# Dabarqus

[![Dabarqus Build and Release](https://github.com/electricpipelines/dabarqus/actions/workflows/build-and-release.yaml/badge.svg)](https://github.com/electricpipelines/dabarqus/actions/workflows/build-and-release.yaml)

**Dabarqus** is a revolutionary all-in-one RAG (Retrieval-Augmented Generation) solution designed for developers who prioritize privacy, performance, and ease of deployment.

In our experience with custom RAG solutions, we\'ve encountered three major challenges:

1. Ensuring data privacy and control
1. Simplifying setup across different environments
1. Integrating RAG capabilities seamlessly with LLMs

**Dabarqus addresses these challenges head-on:**

1. **Local and Private**: Dabarqus runs entirely on your own hardware - be it a PC, laptop, server, or owned-cloud infrastructure. Your data never leaves your control.
1. **Zero Dependencies**: Dabarqus is a standalone C++ application with everything built-in. No external dependencies, no installation complexities.
1. **Easy Integration**: Dabarqus features a REST API with JSON output, facilitating smooth integration with existing systems and LLMs.

**Key features of Dabarqus:**

1. **Comprehensive Solution**: Dabarqus integrates all essential components for RAG in one package:

    - **Vector database** for efficient storage and retrieval
    - **Embedding model** for converting text to vector representations
    - **Ingestion and retrieval** utilities for seamless data management
    - **Built-in chatbot** accessible via browser

1. **Database API Functionality**: It operates similarly to a database API, simplifying integration and usage.
1. **Intelligent Querying**: Send queries or chat inputs to receive relevant documents, ranked by relevance to your input.
1. **Enhanced AI Compatibility**: The search results can be easily used with various AI models to generate more informed responses.
1. **Cross-Platform Compatibility**: Dabarqus runs as an OS service, ensuring seamless operation across Windows, Linux, and macOS.

For developers, we\'ve also created `barq`, a command-line interface that interacts with Dabarqus via a REST API, providing a familiar and efficient tool for integration and management.

Dabarqus streamlines the RAG implementation process, offering a robust, flexible, and user-friendly solution that prioritizes data privacy and eliminates dependency issues. Whether you\'re working on a small-scale project or a large enterprise solution, Dabarqus provides the tools you need for efficient knowledge storage and retrieval, all while keeping your data secure and under your control.

## Architecture

The application has three components: a backend service (called Dabarqus) that runs as an OS service at startup, a command line interface (called barq) for developers, and an Electron UI (called ODOBO) for end users.

- Dabarqus is the engine of the application. barq and ODOBO access it via a REST API.
- Dabarqus is installed as a Windows, Linux or MacOS service that runs at all times.
- barq is installed alongside Dabarqus, and is placed in the system PATH for easy access from a command line.
- ODOBO is installed as a desktop application on Windows and MacOS.

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
             will display three answers to the query from the 'documents' memory bank

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
| GET | /api/silk/query | Perform a semantic query | (Parameters handled by Silk retriever) |
| GET | /api/silk/health | Check the health of the Silk retriever | None |
| GET | /api/silk/model/metadata | Get model metadata from the Silk retriever | (Parameters handled by Silk retriever) |
| GET | /api/shutdown | Initiate server shutdown | None |
| POST | /api/utils/log | Write to log | JSON body with log details |
| POST | /api/silk/embedding | Get an embedding from the Silk retriever | (Parameters handled by Silk retriever) |

### Using the API

- Example: `curl http://localhost:6568/api/silk/query?q=Tell%20me%20about%20the%20documents&limit=3&memorybank=docs`
