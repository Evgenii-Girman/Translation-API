import uvicorn
from fastapi import FastAPI
from src.services.translation import translate_text, get_supported_languages
from src.models.translation_request import TranslationRequest
from src.services.logger import get_logger
from src.services.config import settings

logger = get_logger("translation_api")

# Initialize FastAPI
app = FastAPI(
    title="Language Translation API",
    description="Translate text between languages using MarianMT models.",
    version="2.0.0",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown complete.")

@app.post("/translate", summary="Translate Text")
async def translate_text_endpoint(request: TranslationRequest):
    """
    Translate text from one language to another.
    """
    return await translate_text(request)

@app.get("/supported-languages", summary="Get Supported Language Pairs")
async def supported_languages_endpoint():
    """
    Retrieve all supported language pairs.
    """
    return get_supported_languages()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
