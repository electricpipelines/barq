# Dabarqus

[![Dabarqus Build and Release](https://github.com/electricpipelines/dabarqus/actions/workflows/build-and-release.yaml/badge.svg)](https://github.com/electricpipelines/dabarqus/actions/workflows/build-and-release.yaml)

The application has three components: a backend service (called Dabarqus) that runs as an OS service at startup, a command line interface (called barq) for developers, and an Electron UI (called ODOBO) for end users.

- Dabarqus is the engine of the application. barq and ODOBO access it via a REST API.
- Dabarqus is installed as a Windows, Linux or MacOS service that runs at all times.
- barq is installed alongside Dabarqus, and is placed in the system PATH for easy access from a command line.
- ODOBO is installed as a desktop application on Windows and MacOS.

## Barq

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

## API

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
