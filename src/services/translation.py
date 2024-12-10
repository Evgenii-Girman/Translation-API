import os
from transformers import MarianMTModel, MarianTokenizer, GenerationConfig
from fastapi import HTTPException
from threading import Lock
from src.services.config import settings
from src.services.logger import get_logger

# Global variables
model_cache = {}
model_lock = Lock()
MODEL_DIR = settings.MODEL_DIR
SUPPORTED_LANGUAGES = []
DEFAULT_PRECACHE_MODELS = settings.PRECACHE_MODELS.split(",")

logger = get_logger("translation_service")

def load_supported_languages():
    """
    Dynamically load supported language pairs based on Helsinki-NLP models.
    """
    global SUPPORTED_LANGUAGES
    available_models = [
        "en-de", "de-en", "en-fr", "fr-en", "en-es", "es-en", "en-ru", "ru-en",
        "en-it", "it-en", "en-zh", "zh-en", "en-ja", "ja-en", "en-nl", "nl-en"
    ]
    SUPPORTED_LANGUAGES = available_models


def pre_cache_models():
    """
    Preloads popular models to improve startup performance.
    """
    for model_key in DEFAULT_PRECACHE_MODELS:
        from_lang, to_lang = model_key.split("-")
        try:
            get_model(from_lang, to_lang)
        except Exception as e:
            logger.error(f"Failed to pre-cache model {model_key}: {e}")


def get_model(from_lang: str, to_lang: str):
    """
    Retrieves a translation model for the given language pair.
    Downloads it if not cached.
    """
    model_key = f"{from_lang}-{to_lang}"
    model_name = f"Helsinki-NLP/opus-mt-{model_key}"
    local_model_path = os.path.join(settings.MODEL_DIR, model_key)

    logger.info(f"Loading model for {from_lang}-{to_lang}")
    
    with model_lock:
        if not os.path.exists(local_model_path) or not os.listdir(local_model_path):
            logger.info(f"Downloading model {model_name}...")
            os.makedirs(local_model_path, exist_ok=True)
            try:
                model = MarianMTModel.from_pretrained(model_name)
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                model.save_pretrained(local_model_path)
                tokenizer.save_pretrained(local_model_path)
            except Exception as e:
                logger.error(f"Failed to load model for {from_lang}-{to_lang}: {e}")
                raise ValueError(f"Failed to load model {model_name}: {e}")
        else:
            logger.info(f"Loading model {model_name} from local cache...")
            try:
                model = MarianMTModel.from_pretrained(local_model_path)
                tokenizer = MarianTokenizer.from_pretrained(local_model_path)
            except Exception as e:
                logger.error(f"Failed to load model for {from_lang}-{to_lang}: {e}")
                raise ValueError(f"Failed to load model {model_name}: {e}")

        model_cache[model_key] = (model, tokenizer)

    return model_cache[model_key]



async def translate_text(request):
    """
    Translates text from one language to another.
    """
    if request.from_lang == request.to_lang:
        raise HTTPException(status_code=400, detail="Source and target languages must be different.")

    if f"{request.from_lang}-{request.to_lang}" not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language pair.")

    try:
        model, tokenizer = get_model(request.from_lang, request.to_lang)
        
        # Define generation configuration explicitly
        generation_config = GenerationConfig(
            max_length=512,
            num_beams=4,
            bad_words_ids=[[59513]],
        )
                
        tokens = tokenizer(request.text.strip(), return_tensors="pt", padding=True, truncation=True)
        translated_tokens = model.generate(**tokens, generation_config=generation_config)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return {"translated_text": translated_text}
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}")


def get_supported_languages():
    """
    Returns all supported language pairs.
    """
    return {"supported_languages": SUPPORTED_LANGUAGES}


# Load supported languages and pre-cache models on startup
load_supported_languages()
pre_cache_models()
