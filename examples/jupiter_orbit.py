"""
Simulation d'une orbite circulaire au demi-grand axe de Jupiter.

Note : l'orbite est circulaire (vitesse initiale = vitesse circulaire théorique
à ce rayon), pas l'orbite elliptique de Jupiter (e = 0.0489).

Utilisation
-----------
    python3 examples/jupiter_orbit.py            # affiche la figure
    python3 examples/jupiter_orbit.py --save fig.png   # sauvegarde sans afficher
"""

import argparse
import numpy as np

# Analyser les arguments AVANT d'importer pyplot afin de pouvoir choisir
# le backend matplotlib sans affichage si --save est demandé.
_parser = argparse.ArgumentParser(
    description="Simulation orbite circulaire au rayon de Jupiter"
)
_parser.add_argument("--save", metavar="FICHIER", default=None,
                     help="Sauvegarde la figure dans FICHIER sans afficher")
_args = _parser.parse_args()

import matplotlib
if _args.save:
    matplotlib.use('Agg')   # backend sans fenêtre — doit précéder pyplot
import matplotlib.pyplot as plt

# ==========================================
# CONSTANTES PHYSIQUES ET PARAMÈTRES
# ==========================================
G         = 6.67430e-11    # Constante gravitationnelle (m^3 kg^-1 s^-2)
M_SOLEIL  = 1.989e30       # Masse du Soleil (kg)

# Données orbitales — orbite CIRCULAIRE au demi-grand axe de Jupiter
r_jupiter = 778.5e9        # Demi-grand axe (m)
# Vitesse circulaire théorique (pas la vitesse orbitale moyenne de Jupiter)
v_circ    = np.sqrt(G * M_SOLEIL / r_jupiter)

# Paramètres de simulation temporelle
dt         = 86400                                    # Pas de temps : 1 jour (s)
T_orbital  = 2 * np.pi * np.sqrt(r_jupiter**3 / (G * M_SOLEIL))
steps      = int(np.ceil(T_orbital / dt))            # Couvre exactement une période

# ==========================================
# INITIALISATION DES VECTEURS (Position & Vitesse)
# ==========================================
position = np.array([r_jupiter, 0.0], dtype=float)
vitesse  = np.array([0.0, v_circ],   dtype=float)

# Listes pour stocker la trajectoire et l'énergie
trajectoire_x = [position[0]]
trajectoire_y = [position[1]]
energies      = []

# ==========================================
# BOUCLE DE SIMULATION (Méthode d'Euler-Cromer)
# Diagnostic d'énergie évalué AVANT la mise à jour de position,
# c'est-à-dire au même instant que la vitesse déjà actualisée.
# ==========================================
for _ in range(steps):
    r_distance  = np.linalg.norm(position)
    acceleration = -(G * M_SOLEIL / r_distance**3) * position

    # Mise à jour de la vitesse (Euler-Cromer : vitesse d'abord)
    vitesse  += acceleration * dt

    # Diagnostic : énergie mécanique — vitesse et position évaluées au même instant
    v_norm  = np.linalg.norm(vitesse)
    e_meca  = 0.5 * v_norm**2 - (G * M_SOLEIL / r_distance)
    energies.append(e_meca)

    # Mise à jour de la position avec la vitesse déjà actualisée
    position += vitesse * dt

    trajectoire_x.append(position[0])
    trajectoire_y.append(position[1])

energies = np.array(energies)

# ==========================================
# AFFICHAGE GRAPHIQUE
# ==========================================
UA    = 1.496e11
x_ua  = np.array(trajectoire_x) / UA
y_ua  = np.array(trajectoire_y) / UA

plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 1. Trajectoire spatiale
ax1.plot(x_ua, y_ua, color='orange', linestyle='--',
         label='Orbite circulaire (r = a_Jupiter)')
ax1.plot(0, 0, marker='o', markersize=12, color='yellow', label='Soleil')
ax1.plot(x_ua[0],  y_ua[0],  marker='o', markersize=5,
         color='green', label='Départ (t=0)')
ax1.plot(x_ua[-1], y_ua[-1], marker='x', markersize=7,
         color='cyan',  label='Arrivée (t=1 orbite)')
ax1.set_title(f"Orbite circulaire au rayon de Jupiter ({steps} jours)", fontsize=11)
ax1.set_xlabel("X (UA)")
ax1.set_ylabel("Y (UA)")
ax1.axhline(0, color='gray', linewidth=0.5, linestyle=':')
ax1.axvline(0, color='gray', linewidth=0.5, linestyle=':')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=9)
ax1.axis('equal')

# 2. Diagnostic d'énergie (Stabilité de l'intégrateur)
jours = np.arange(steps)
ax2.plot(jours, (energies - energies[0]) / np.abs(energies[0]), color='magenta')
ax2.set_title("Dérive relative de l'énergie mécanique", fontsize=11)
ax2.set_xlabel("Temps (jours)")
ax2.set_ylabel("ΔE / E_0")
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# ==========================================
# SAUVEGARDE OU AFFICHAGE
# ==========================================
if _args.save:
    fig.savefig(_args.save, dpi=150)
    print(f"Figure sauvegardée : {_args.save}")
else:
    plt.show()

