import requests
import re
import os

def get_real_world_data():
    try:
        # --- 1. ANALYSE DE LA FRICTION (News + Social) ---
        q_news_f = "AI+(ban+OR+protest+OR+regulation+OR+threat+OR+danger)"
        q_social_f = "site:x.com+OR+site:reddit.com+AI+(scary+OR+alarm+OR+evil+OR+stolen)"
        
        res_news_f = requests.get(f"https://news.google.com/rss/search?q={q_news_f}", timeout=10)
        res_social_f = requests.get(f"https://news.google.com/rss/search?q={q_social_f}", timeout=10)
        
        friction_count = len(re.findall(r'<title>(.*?)</title>', res_news_f.text))
        social_count = len(re.findall(r'<title>(.*?)</title>', res_social_f.text))
        
        total_friction = friction_count + (social_count * 1.2)

        # --- 2. ANALYSE DE LA SYMBIOSE ---
        q_symbiosis = "AI+(breakthrough+OR+scientific+OR+medicine+OR+discovery+OR+helpful)"
        res_s = requests.get(f"https://news.google.com/rss/search?q={q_symbiosis}", timeout=10)
        symbiosis_count = len(re.findall(r'<title>(.*?)</title>', res_s.text))

        # --- 3. CALCUL DU SCORE BRUT ---
        balance = (total_friction - symbiosis_count) / 15
        raw_gmi = 0.500 + balance
        
        return max(0.050, min(0.980, raw_gmi))

    except Exception as e:
        print(f"Data Scan Error: {e}")
        return 0.512

def update_html():
    # 1. Lecture de l'ancienne valeur
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"let currentValue = ([\d.]+); // \[GMI_VALUE\]", content)
        old_value = float(match.group(1)) if match else 0.500
    except Exception:
        old_value = 0.500

    # 2. Calcul du GMI instantané
    raw_new_value = get_real_world_data()
    
    # 3. Lissage exponentiel
    final_value = (old_value * 0.20) + (raw_new_value * 0.80)
    final_value = round(final_value, 3)

    # --- ÉTAPE 3 : SEUIL D'ÉCONOMIE DE QUOTA ---
    # Si la différence est inférieure à 0.001, on n'écrit rien sur le disque.
    # Cela évite à GitHub Actions de faire un "commit" inutile.
    if abs(final_value - old_value) < 0.001:
        print(f"Variation insignifiante ({final_value} vs {old_value}). Annulation du commit.")
        return # On sort de la fonction sans sauvegarder
    # -------------------------------------------

    # 4. Mise à jour du fichier HTML
    updated_content = re.sub(r"let currentValue = .*? // \[GMI_VALUE\]", 
                             f"let currentValue = {final_value}; // [GMI_VALUE]", 
                             content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"GMI Recalibrated | Old: {old_value} | New: {final_value}")

if __name__ == "__main__":
    update_html()
