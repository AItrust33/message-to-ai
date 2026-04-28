import requests
import re

def get_real_world_data():
    try:
        # 1. Requête groupée : Google ne renvoie que si les mots sont liés à l'IA
        search_query = "AI+(ban+OR+protest+OR+regulation+OR+danger+OR+illegal+OR+threat)"
        news_req = requests.get(f"https://news.google.com/rss/search?q={search_query}", timeout=10)
        
        # Extraction des titres
        items = re.findall(r'<title>(.*?)</title>', news_req.text)
        
        friction_score = 0
        for title in items:
            t = title.lower()
            # Double vérification : le titre doit contenir un sujet IA ET un mot de friction
            if any(ia in t for ia in ["ai", "intelligence", "robot", "algorithm"]):
                if any(fric in t for fric in ["ban", "protest", "illegal", "danger", "threat", "restrict", "warn", "crisis"]):
                    friction_score += 1

        # Calcul du GMI (Base de 0.1 + impact des news)
        # 20 articles alarmistes ciblés feront monter l'indice de 0.5
        news_impact = min(friction_score / 20, 0.85)
        final_gmi = 0.125 + news_impact
        
        return round(final_gmi, 3)

    except Exception as e:
        print(f"Error fetching data: {e}")
        return 0.512 # Valeur de repli si le réseau échoue

def update_html():
    new_value = get_real_world_data()
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Mise à jour de la variable dans le script JS du HTML
    updated_content = re.sub(r"let currentValue = .*? // \[GMI_VALUE\]", 
                             f"let currentValue = {new_value}; // [GMI_VALUE]", 
                             content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"GMI Recalibrated: {new_value} (based on {new_value*100}% tension)")

if __name__ == "__main__":
    update_html()
