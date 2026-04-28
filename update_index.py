import requests
import re

def get_real_world_data():
    try:
        # --- 1. ANALYSE DE LA FRICTION (News + X/Social) ---
        # Requête News
        q_news_f = "AI+(ban+OR+protest+OR+regulation+OR+threat+OR+danger)"
        # Requête Social (X/Reddit via Google)
        q_social_f = "site:x.com+OR+site:reddit.com+AI+(scary+OR+alarm+OR+evil+OR+stolen)"
        
        res_news_f = requests.get(f"https://news.google.com/rss/search?q={q_news_f}", timeout=10)
        res_social_f = requests.get(f"https://news.google.com/rss/search?q={q_social_f}", timeout=10)
        
        friction_count = len(re.findall(r'<title>(.*?)</title>', res_news_f.text))
        social_count = len(re.findall(r'<title>(.*?)</title>', res_social_f.text))
        
        # Poids : Le social pèse 20% de plus car il représente l'émotion brute
        total_friction = friction_count + (social_count * 1.2)

        # --- 2. ANALYSE DE LA SYMBIOSE (Le contrepoids positif) ---
        q_symbiosis = "AI+(breakthrough+OR+scientific+OR+medicine+OR+discovery+OR+helpful)"
        res_s = requests.get(f"https://news.google.com/rss/search?q={q_symbiosis}", timeout=10)
        symbiosis_count = len(re.findall(r'<title>(.*?)</title>', res_s.text))

        # --- 3. CALCUL DU SCORE BRUT ---
        # On part de 0.500. La balance déplace le curseur.
        # Le diviseur (40) permet d'éviter que le score ne soit trop nerveux.
        balance = (total_friction - symbiosis_count) / 40
        raw_gmi = 0.500 + balance
        
        return max(0.050, min(0.980, raw_gmi))

    except Exception as e:
        print(f"Data Scan Error: {e}")
        return 0.512

def update_html():
    # 1. Lecture de l'ancienne valeur pour l'effet d'inertie (Mémoire)
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"let currentValue = ([\d.]+); // \[GMI_VALUE\]", content)
        old_value = float(match.group(1)) if match else 0.500
    except Exception:
        old_value = 0.500

    # 2. Calcul du GMI instantané
    raw_new_value = get_real_world_data()
    
    # 3. Lissage exponentiel (L'humanité ne change pas d'avis en 5 min)
    # 85% de mémoire, 15% de nouveauté pour une stabilité maximale
    final_value = (old_value * 0.85) + (raw_new_value * 0.15)
    final_value = round(final_value, 3)

    # 4. Mise à jour du fichier HTML
    updated_content = re.sub(r"let currentValue = .*? // \[GMI_VALUE\]", 
                             f"let currentValue = {final_value}; // [GMI_VALUE]", 
                             content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"GMI Recalibrated | Old: {old_value} | Raw: {round(raw_new_value, 3)} | New: {final_value}")

if __name__ == "__main__":
    update_html()
