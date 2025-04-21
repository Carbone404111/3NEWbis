from flask import Flask, render_template, request
from math import sqrt, pi
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Constantes
G = 6.674 * 10**-11
M = 5.972 * 10**24
R = 6.371 * 10**6  # rayon en mètres

@app.route('/', methods=['GET', 'POST'])
def index():
    result1 = ""
    result2 = ""
    result3 = ""
    image = None

    if request.method == 'POST':
        try:
            h_km = float(request.form['distance'])

            if h_km >= 326000 or h_km == 326000:
                result1 = "⚠️ Ce satellite est trop loin de la terre, il a dépassé le point Lagrange, et l'influence de la terre est négligeable."
                result2 = "Fais une recherche pour en savoir plus !"
                result3 = "Essaye une autre valeure..."
                return render_template('index.html', result1=result1, result2=result2, result3 = result3)
            if h_km <= 160 or h_km == 160:
                result1 = "⚠️ Ce satellite est trop proche de la terre, il peut exister brièvement, mais ce n’est pas une orbite stable.."
                result2 = "Fais une recherche pour en savoir plus !"
                result3 = "Essaye une autre valeure..."
                return render_template('index.html', result1=result1, result2=result2, result3=result3)

            r = R + (h_km * 1000)  # convertir h en mètres

            vitesse_orbitale = sqrt(G * M / r) * 3.6  # km/h
            T = 2 * pi * sqrt(r**3 / (G * M))

            temps_restant = T
            an = int(temps_restant // 31536000)
            temps_restant %= 31536000
            jour = int(temps_restant // 86400)
            temps_restant %= 86400
            heure = int(temps_restant // 3600)
            temps_restant %= 3600
            minute = int(temps_restant // 60)
            seconde = int(temps_restant % 60)

            vitesse_liberation = sqrt(2*G*M/r)

            result1 = f"🚀 Vitesse orbitale : {vitesse_orbitale:.2f} km/h"
            result2 = f"⏱️ Période orbitale : {an} an(s), {jour} jour(s), {heure}h {minute}min {seconde}s"
            result3 = f" Vitesse de libération : {vitesse_liberation:.2f} km/h"

            # Générer l’image
            R_terre = 6371
            r_satellite = R_terre + h_km

            fig, ax = plt.subplots(figsize=(6, 6))
            ax.set_aspect('equal')
            ax.add_artist(plt.Circle((0, 0), R_terre, color='deepskyblue', label="Terre"))
            orbite = plt.Circle((0, 0), r_satellite, color='gray', fill=False, linestyle='--', label="Orbite")
            ax.add_artist(orbite)
            ax.plot(r_satellite, 0, 'ro', label="Satellite")

            max_range = r_satellite + 1000
            ax.set_xlim(-max_range, max_range)
            ax.set_ylim(-max_range, max_range)
            ax.set_title("Orbite du satellite autour de la Terre")
            ax.set_xlabel("km")
            ax.set_ylabel("km")
            ax.legend(loc='upper right')
            ax.grid(True)

            image_path = os.path.join('static', 'image.png')
            plt.savefig(image_path)
            plt.close()
            image = 'image.png'

        except Exception as e:
            result1 = f"Erreur : {str(e)}"

    return render_template('index.html', result1=result1, result2=result2, image=image)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
