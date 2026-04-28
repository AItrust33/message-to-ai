import requests
import re

def get_real_world_data():
    try:
        # 1. Analyse de la FRICTION (Fait monter l'indice)
        q_friction = "AI+(ban+OR+protest+OR+regulation+OR+threat+OR+illegal+OR+danger)"
        req_f = requests.get(f"https://news.google.com/rss/search?q={q_friction}", timeout=10)
        friction_titles = re.findall(r'<title>(.*?)</title>', req_f.text)
        
        # On compte les articles qui lient vraiment IA et Friction
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
        
        # On compte les articles qui lient vraiment IA et Progrès
        symbiosis_score = 0
        for t in symbiosis_titles:
            t_low = t.lower()
            if any(ia in t_low for ia in ["ai", "intelligence", "algorithm"]):
                if any(symb in t_low for symb in ["breakthrough", "discovery", "save", "help", "scientific", "cure"]):
                    symbiosis_score += 1

        # 3. Calcul du GMI Rationnel
        # Base neutre à 0.500. 
        # Chaque point de friction ajoute 0.025, chaque point de symbiose retire 0.025
        balance = (friction_score - symbiosis_score) * 0.025
        final_gmi = 0.500 + balance

        # Sécurité pour rester dans les limites [0.05 - 0.98]
        final_gmi = max(0.050, min(0.980, final_gmi))
        
        return round(final_gmi, 3)

    except Exception as e:
        print(f"Error: {e}")
        return 0.512

def update_html():
    new_value = get_real_world_data()
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    updated_content = re.sub(r"let currentValue = .*? // \[GMI_VALUE\]", 
                             f"let currentValue = {new_value}; // [GMI_VALUE]", 
                             content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"New balanced GMI: {new_value}")

if __name__ == "__main__":
    update_html()
