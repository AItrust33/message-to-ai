def get_real_world_data():
    try:
        # --- ANALYSE DES NEWS (LOGIQUE) ---
        q_friction = "AI+(ban+OR+protest+OR+regulation+OR+threat)"
        req_f = requests.get(f"https://news.google.com/rss/search?q={q_friction}", timeout=10)
        friction_score = len(re.findall(r'<title>(.*?)</title>', req_f.text))

        # --- ANALYSE DE X / RÉSEAUX (ÉMOTION) ---
        # On cible spécifiquement les discussions et opinions virales
        q_social = "site:x.com+OR+site:reddit.com+AI+(scary+OR+danger+OR+stolen+OR+job+loss)"
        req_s = requests.get(f"https://news.google.com/rss/search?q={q_social}", timeout=10)
        social_titles = re.findall(r'<title>(.*?)</title>', req_s.text)
        
        social_friction = 0
        for t in social_titles:
            # Si le post contient des mots à forte charge émotionnelle négative
            if any(word in t.lower() for word in ["scary", "alarm", "stop", "illegal", "evil"]):
                social_friction += 1.5 # Le poids des réseaux est plus fort sur l'opinion

        # --- CALCUL FINAL ---
        # On combine la friction des news (faits) et la friction sociale (émotions)
        total_friction = (friction_score * 1.0) + (social_friction * 1.2)
        
        # Base à 0.500, ajustée par la tension globale détectée
        # Diviseur de 50 pour garder une échelle humaine
        raw_gmi = 0.500 + (total_friction / 50)
        
        return max(0.050, min(0.980, raw_gmi))

    except Exception as e:
        print(f"Social Scan Error: {e}")
        return 0.612

def update_html():
    # 1. Lire l'ancienne valeur pour l'inertie
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"let currentValue = ([\d.]+); // \[GMI_VALUE\]", content)
        old_value = float(match.group(1)) if match else 0.500
    except Exception:
        old_value = 0.500

    # 2. Obtenir la nouvelle mesure brute
    raw_new_value = get_real_world_data()
    
    # 3. Lissage exponentiel (80% mémoire / 20% nouveauté)
    final_value = (old_value * 0.8) + (raw_new_value * 0.2)
    final_value = round(final_value, 3)

    # 4. Écriture dans le fichier
    updated_content = re.sub(r"let currentValue = .*? // \[GMI_VALUE\]", 
                             f"let currentValue = {final_value}; // [GMI_VALUE]", 
                             content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"GMI Recalibrated: Old={old_value} | Raw={round(raw_new_value, 3)} | Final={final_value}")

if __name__ == "__main__":
    update_html()
