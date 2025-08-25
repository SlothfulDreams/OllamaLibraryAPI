# Ollama Library API

A RESTful API for fetching and searching Ollama models from the official Ollama library. This API scrapes the Ollama website to provide structured access to model information including descriptions, capabilities, sizes, and statistics.

## Why This API?

While exploring the Ollama ecosystem, I couldn't find a proper API to programmatically access the Ollama library and retrieve model information. I built this simple API to solve this issue :)

- Browse all available models
- Search models by name, capability, or parameter size
- Get detailed model information including descriptions, statistics, and capabilities
- Integrate Ollama model discovery into their applications

## Table of Contents

- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Response Schema](#response-schema)
- [Example Responses](#example-responses)
- [Error Handling](#error-handling)
- [Running the API](#running-the-api)

## Getting Started

### Installation

1. Clone the repository
2. Install dependencies using UV or pip:

   ```bash
   uv sync
   ```

### Running the Server

Start the FastAPI development server:

```bash
uv run fastAPI dev
```

The API will be available at `http://localhost:8000`

## FastAPI automatically generates interactive API documentation: 
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`


## Notes
- The API scrapes data from `https://ollama.com/library` in real-time
- Response times depend on the Ollama website's availability and performance
- Model data is fetched fresh on each request (no caching implemented)
- All endpoints are now fully functional and bug-free!

## API Endpoints

| Method | Endpoint                   | Description                         | Parameters            |
| ------ | -------------------------- | ----------------------------------- | --------------------- |
| GET    | `/`                        | Welcome message                     | None                  |
| GET    | `/get_models`              | Get all models as Model objects     | None                  |
| GET    | `/get_models_json`         | Get all models as JSON dictionaries | None                  |
| GET    | `/get_model_by_name`       | Get a specific model by name        | `name` (string)       |
| GET    | `/get_model_by_capability` | Get models filtered by capability   | `capability` (string) |
| GET    | `/get_models_size`         | Get models filtered by size         | `size` (string)       |

### Base URL

```
http://localhost:8000
```

### Detailed Endpoint Documentation

#### `GET /`

Returns a welcome message.

**Response:**

```
"API for fetching Ollama Models!"
```

#### `GET /get_models`

Retrieves all available Ollama models as Model objects.

**Response:** Array of Model objects

#### `GET /get_models_json`

Retrieves all available Ollama models as JSON dictionaries.

**Response:** Array of JSON objects with model data

#### `GET /get_model_by_name?name={model_name}`

Retrieves a specific model by its exact name (case-insensitive).

**Parameters:**

- `name` (string, required): The exact name of the model to search for

**Response:** Single Model object or `null` if not found

**Example:**

```
GET /get_model_by_name?name=llama2
```

#### `GET /get_model_by_capability?capability={capability}`

Retrieves all models that have the specified capability.

**Parameters:**

- `capability` (string, required): The capability to filter by (case-insensitive)

**Response:** Array of Model objects matching the capability

**Example:**

```
GET /get_model_by_capability?capability=chat
```

#### `GET /get_models_size?size={size}`

Retrieves all models that have the specified size parameter.

**Parameters:**

- `size` (string, required): The size parameter to filter by (case-insensitive)

**Response:** Array of Model objects matching the size

**Example:**

```
GET /get_models_size?size=7b
```

## Response Schema

### Model Object Structure

```json
{
  "title": "string", // Model name
  "description": "string", // Model description
  "sizes": ["string"], // Available parameter sizes (e.g., ["7b", "13b"])
  "capabilities": ["string"], // Model capabilities (e.g., ["chat", "code"])
  "pulls": "string", // Number of pulls/downloads
  "tags": "string", // Number of tags/versions
  "updated": "string" // Last updated timestamp
}
```

### Field Descriptions

- **title**: The official name of the model
- **description**: A brief description of the model's purpose and capabilities
- **sizes**: Array of available parameter sizes (e.g., "7b", "13b", "70b")
- **capabilities**: Array of model capabilities (e.g., "chat", "code", "vision")
- **pulls**: String representation of download count
- **tags**: String representation of available tags/versions
- **updated**: Human-readable last updated time

## Example Responses

### Get All Models JSON

```json
[
  {
    "title": "llama2",
    "description": "Llama 2 is a collection of foundation language models ranging from 7B to 70B parameters.",
    "sizes": ["7b", "13b", "70b"],
    "capabilities": ["chat", "text"],
    "pulls": "5.2M",
    "tags": "12",
    "updated": "2 months ago"
  },
  {
    "title": "codellama",
    "description": "Code Llama is a collection of foundation language models for code.",
    "sizes": ["7b", "13b", "34b"],
    "capabilities": ["code", "instruct"],
    "pulls": "2.1M",
    "tags": "8",
    "updated": "3 weeks ago"
  }
]
```

### Get Model by Name

```json
{
  "title": "llama2",
  "description": "Llama 2 is a collection of foundation language models ranging from 7B to 70B parameters.",
  "sizes": ["7b", "13b", "70b"],
  "capabilities": ["chat", "text"],
  "pulls": "5.2M",
  "tags": "12",
  "updated": "2 months ago"
}
```

### Model Not Found

```json
null
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Request successful
- `422 Unprocessable Entity` - Invalid parameters (handled by FastAPI)
- `500 Internal Server Error` - Server error during scraping




