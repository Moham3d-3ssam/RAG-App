from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory


app = FastAPI()

@app.on_event("startup")
async def startup_dp_client():
  settings = get_settings()
  app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
  app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
  
  llm_provider_factory = LLMProviderFactory(settings)
  
  # generation client
  app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
  app.generation_client.set_generation_model(model_id=settings.GENERATION_MODE_ID)
  
  # embedding client
  app.generation_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
  app.generation_client.set_embedding_model(model_id=settings.EMBEDDING_MODE_ID,
                                            embedding_size=settings.EMBEDDING_MODE_SIZE)

@app.on_event("shutdown")
async def shutdown_df_client():
  app.mongo_conn.close()

app.include_router(base.base_router)
app.include_router(data.data_router)
