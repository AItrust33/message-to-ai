import random
import re

# Simulation de collecte de données (Ici tu pourrais ajouter des appels API réels)
# Plus l'instabilité mondiale est haute, plus l'index monte
def get_live_misalignment():
    # Exemple : 0.4 de base + une variation basée sur des facteurs simulés
    return round(random.uniform(0.1, 0.9), 3)

def update_html():
    new_value = get_live_misalignment()
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # On cherche la ligne avec notre ancrage et on remplace la valeur
    updated_content = re.sub(r"let currentValue = .*? // \[GMI_VALUE\]", 
                             f"let currentValue = {new_value}; // [GMI_VALUE]", 
                             content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"Index mis à jour : {new_value}")

if __name__ == "__main__":
    update_html()
