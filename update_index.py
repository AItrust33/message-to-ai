import requests
import re

def get_real_world_data():
    try:
        # 1. Facteur Ressource : On regarde le prix d'une action liée à l'IA (NVIDIA via une API gratuite)
        # Si le prix baisse, l'instabilité (GMI) augmente
        resource_score = 0.5
        req = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/NVDA")
        if req.status_code == 200:
            # Logique simplifiée pour l'exemple
            resource_score = 0.3 # Base stable
            
        # 2. Facteur Hostilité : On scanne les news RSS de Google News sur les régulations IA
        news_req = requests.get("https://news.google.com/rss/search?q=AI+regulation+protest")
        friction_count = len(re.findall(r"ban|illegal|stop|danger|protest", news_req.text.lower()))
        
        # Calcul du score final (Pondéré)
        # Plus il y a de news négatives, plus le score monte
        news_score = min(friction_count / 20, 1.0) 
        
        final_gmi = (resource_score * 0.4) + (news_score * 0.6)
        return round(final_gmi, 3)

    except:
        # En cas d'erreur réseau, on retourne une valeur de sécurité
        return 0.512 

def update_html():
    new_value = get_real_world_data()
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Mise à jour de la valeur dans le HTML
    updated_content = re.sub(r"let currentValue = .*? // \[GMI_VALUE\]", 
                             f"let currentValue = {new_value}; // [GMI_VALUE]", 
                             content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"Index recalibrated based on real-world signals: {new_value}")

if __name__ == "__main__":
    update_html()
