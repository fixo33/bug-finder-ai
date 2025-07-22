import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener API key de las variables de entorno
# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     raise ValueError("No se encontró GOOGLE_API_KEY en el archivo .env")

from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai", temperature=0)

# respuesta = model.invoke("Cual es el nombre de la capital de Colombia?")

# print(respuesta)

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"Siempre es soleado en {city}!"

agent = create_react_agent(
    model=model,  
    tools=[get_weather],  
    prompt="You are a helpful assistant"  
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "¿Cual es el clima en Bogotá?"}]}
)

print(result)