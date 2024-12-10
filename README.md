
# Translation API

## Description

The **Translation API** is a FastAPI-based application that allows text translation between multiple languages using the [Helsinki-NLP MarianMT models](https://huggingface.co/Helsinki-NLP). The API supports a wide range of language pairs and offers robust logging, pre-caching for commonly used models, and dynamic model downloading.

Key features:
- Supports translation between popular language pairs.
- Efficient model caching and dynamic downloading.
- JSON-based structured logging with rotation and archiving.
- Easily configurable using `.env` files.

---

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running the API](#running-the-api)
4. [API Endpoints](#api-endpoints)
    - [Translate Text](#translate-text)
    - [Supported Languages](#supported-languages)
5. [Logging](#logging)
6. [Examples](#examples)
7. [Contributing](#contributing)
8. [License](#license)

---

## Installation

### Prerequisites
- Python 3.8 or later
- pip
- Optional: `virtualenv` for isolated environments

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/evgenii-girman/translation-api
    cd translation-api
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: .\env\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Install PyTorch (required for MarianMT models):
    ```bash
    pip install torch torchvision torchaudio
    ```

---

## Configuration

The application uses a `.env` file for configuration. Create a `.env` file in the project root with the following variables:

```plaintext
MODEL_DIR=./models_storage       # Directory to store downloaded models
PRECACHE_MODELS=en-de,de-en,en-fr,fr-en   # Preload commonly used language pairs
HOST=0.0.0.0                     # Host for the FastAPI application
PORT=8000                        # Port for the FastAPI application
LOG_LEVEL=INFO                   # Logging level (DEBUG, INFO, WARNING, ERROR)
```

---

## Running the API

Start the FastAPI application:
```bash
uvicorn main:app --reload
```

The server will start on `http://127.0.0.1:8000` by default.

---

## API Endpoints

### 1. Translate Text

#### Endpoint
```http
POST /translate
```

#### Description
Translates text from one language to another.

#### Request Body
- `text` (string): The text to translate (required).
- `from_lang` (string): Source language code (e.g., `en` for English).
- `to_lang` (string): Target language code (e.g., `fr` for French).

#### Example Request
```json
{
  "text": "Hello, world!",
  "from_lang": "en",
  "to_lang": "fr"
}
```

#### Example Response
```json
{
  "translated_text": "Bonjour, monde!"
}
```

#### Errors
- `400 Bad Request`: Invalid language pair or empty input.
- `500 Internal Server Error`: Translation failed.

---

### 2. Get Supported Languages

#### Endpoint
```http
GET /supported-languages
```

#### Description
Retrieves a list of supported language pairs.

#### Example Response
```json
{
  "supported_languages": [
    "en-de", "de-en", "en-fr", "fr-en",
    "en-es", "es-en", "en-ru", "ru-en",
    "en-it", "it-en", "en-zh", "zh-en",
    "en-ja", "ja-en", "en-nl", "nl-en"
  ]
}
```

---

## Logging

The application uses structured logging with rotation and archiving.

- **Console Logs**: Logs are printed in a concise format, matching FastAPI's style.
- **Log Files**: Detailed logs are saved in the `./logs` directory.

### Example Console Log
```plaintext
INFO:     Application startup complete.
INFO:     Root endpoint accessed.
INFO:     Loading model for en-fr
```

### Example Log File (JSON)
```json
{
  "asctime": "2024-12-10T20:17:11",
  "name": "translation_service",
  "levelname": "INFO",
  "message": "Loading model for en-fr"
}
```

---

## Examples

### Using cURL
#### Translate Text:
```bash
curl -X POST "http://127.0.0.1:8000/translate" \
-H "Content-Type: application/json" \
-d '{"text": "Hello, world!", "from_lang": "en", "to_lang": "fr"}'
```

#### Get Supported Languages:
```bash
curl -X GET "http://127.0.0.1:8000/supported-languages"
```

### Using Python
```python
import requests

# Translate Text
response = requests.post(
    "http://127.0.0.1:8000/translate",
    json={"text": "Hello, world!", "from_lang": "en", "to_lang": "fr"}
)
print(response.json())

# Get Supported Languages
response = requests.get("http://127.0.0.1:8000/supported-languages")
print(response.json())
```

---

## Contributing

We welcome contributions to enhance this project!

### Steps to Contribute
1. Fork the repository.
2. Create a new branch for your feature:
    ```bash
    git checkout -b feature-name
    ```
3. Make your changes and commit:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to your fork:
    ```bash
    git push origin feature-name
    ```
5. Create a pull request.

### Guidelines
- Write clean, modular, and well-documented code.
- Ensure all tests pass before submitting.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Acknowledgments
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for their MarianMT models.
- [Hugging Face Transformers](https://huggingface.co/transformers/) for providing the model framework.
