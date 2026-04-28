import requests
import re

def get_real_world_data():
    try:
        # 1. Analyse de la FRICTION (Fait monter l'indice)
        q_friction = "AI+(ban+OR+protest+OR+regulation+OR+threat+OR+illegal+OR+danger)"
        req_f = requests.get(f"https://news.google.com/rss/search?q={q_friction}", timeout=10)
        friction_titles = re.findall(r'<title>(.*?)</title>', req_f.text)
        
        friction_score = 0
        for t in friction_titles:
            t_low = t.lower()
            if any(ia in t_low for ia in ["ai", "intelligence", "algorithm"]):
                if any(fric in t_low for fric in ["ban", "protest", "illegal", "danger", "threat", "warn"]):
                    friction_score += 1

        # 2. Analyse de la SYMBIOSE (Fait baisser l'indice)
        q_symbiosis = "AI+(breakthrough+OR+medicine+OR+discovery+OR+scientific+OR+collaboration+OR+help)"
        req_s = requests.get(f"https://news.google.com/rss/search?q={q_symbiosis}", timeout=10)
        symbiosis_titles = re.findall(r'<title>(.*?)</title>', req_s.text)
        
        symbiosis_score = 0
        for t in symbiosis_titles:
            t_low = t.lower()
            if any(ia in t_low for ia in ["ai", "intelligence", "algorithm"]):
                if any(symb in t_low for symb in ["breakthrough", "discovery", "save", "help", "scientific", "cure"]):
                    symbiosis_score += 1

        # 3. Calcul du score brut (Instantané)
        balance = (friction_score - symbiosis_score) * 0.025
        raw_gmi = 0.500 + balance
        return max(0.050, min(0.980, raw_gmi))

    except Exception as e:
        print(f"Error fetching data: {e}")
        return 0.512

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
