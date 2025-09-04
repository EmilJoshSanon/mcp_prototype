from fastapi import FastAPI
import requests
from pydantic import BaseModel

app = FastAPI(title="Pokémon Basic Info Tool", openapi_url="/openapi.json")

class PokemonBasicInput(BaseModel):
    name: str

class PokemonBasicOutput(BaseModel):
    id: int
    height: int
    weight: int
    types: list[str]

@app.post("/get_pokemon_basic", response_model=PokemonBasicOutput)
def get_pokemon_basic(input: PokemonBasicInput):
    """Fetch basic info for a Pokémon from PokeAPI."""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{input.name.lower()}")
    if response.status_code != 200:
        raise ValueError("Pokémon not found")
    data = response.json()
    types = [t['type']['name'] for t in data['types']]
    return {"id": data['id'], "height": data['height'], "weight": data['weight'], "types": types}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)