import fastapi  import FastAPI
from openai_server.apis.elements_api  import router as ElementsApiRouter 
app =FastAPI(
app = FastAPI(
    title="MiC4.0 Element API Cluster special foundation",
    description="MIC4.0 - Cluster Special foundations - Element-Interfaces definition",
    version="3.0.0 // 10.06.2024",
)
app.include_router(ElementsApiRouter)
