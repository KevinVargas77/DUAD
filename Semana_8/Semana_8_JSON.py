import json


def load_pokemon(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_pokemon(filename, pokemons):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(pokemons, file, indent=2)


def create_new_pokemon():
    name = input("Nombre en inglés del Pokémon: ")
    types = input("Tipo(s) separados por coma: ").split(',')

    base = {}
    base["HP"] = int(input("HP: "))
    base["Attack"] = int(input("Attack: "))
    base["Defense"] = int(input("Defense: "))
    base["Sp. Attack"] = int(input("Sp. Attack: "))
    base["Sp. Defense"] = int(input("Sp. Defense: "))
    base["Speed"] = int(input("Speed: "))

    return {
        "name": {"english": name},
        "type": [t.strip() for t in types],
        "base": base
    }


def main():
    filename = "pokemons.json"
    pokemons = load_pokemon(filename)

    new_pokemon = create_new_pokemon()
    pokemons.append(new_pokemon)

    save_pokemon(filename, pokemons)
    print("¡Nuevo Pokémon agregado con éxito!")

if __name__ == "__main__":
    main()
