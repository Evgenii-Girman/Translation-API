from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, example="Hello, how are you?")
    from_lang: str = Field(..., regex="^[a-z]{2}(-[a-z]{2})?$", example="en")
    to_lang: str = Field(..., regex="^[a-z]{2}(-[a-z]{2})?$", example="fr")
