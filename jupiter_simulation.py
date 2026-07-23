import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION DU STYLE (Avant toute création de figure)
# ==========================================
plt.style.use('dark_background')

# ==========================================
# CONSTANTES PHYSIQUES ET PARAMÈTRES
# ==========================================
G = 6.67430e-11          # Constante gravitationnelle (m^3 kg^-1 s^-2)
M_SOLEIL = 1.989e30      # Masse du Soleil (kg)

# Données orbitales de Jupiter
r_jupiter = 778.5e9      # Demi-grand axe en mètres
v_jupiter = 13.07e3      # Vitesse orbitale moyenne en m/s

# Paramètres de simulation temporelle (Calcul dynamique de la période)
dt = 86400               # Pas de temps : 1 jour en secondes
T_orbital = 2 * np.pi * np.sqrt(r_jupiter**3 / (G * M_SOLEIL))
steps = int(np.ceil(T_orbital / dt))  # Couvre exactement une période orbitale

# ==========================================
# INITIALISATION DES VECTEURS (Position & Vitesse)
# ==========================================
position = np.array([r_jupiter, 0.0], dtype=float)
vitesse = np.array([0.0, v_jupiter], dtype=float)

# Listes pour stocker la trajectoire et l'énergie
trajectoire_x = [position[0]]
trajectoire_y = [position[1]]
energies = []

# ==========================================
# BOUCLE DE SIMULATION (Méthode d'Euler-Cromer)
# ==========================================
for _ in range(steps):
    r_distance = np.linalg.norm(position)
    
    # Force gravitationnelle
    acceleration = - (G * M_SOLEIL / r_distance**3) * position
    
    # Mise à jour de la vitesse et de la position
    vitesse += acceleration * dt
    position += vitesse * dt
    
    # Enregistrement pour le tracé de la trajectoire
    trajectoire_x.append(position[0])
    trajectoire_y.append(position[1])
    
    # Diagnostic : Énergie mécanique par unité de masse
    v_norm = np.linalg.norm(vitesse)
    e_meca = 0.5 * v_norm**2 - (G * M_SOLEIL / r_distance)
    energies.append(e_meca)

# Conversion explicite en tableau NumPy pour sécuriser les opérations vectorielles
energies = np.array(energies)

# ==========================================
# AFFICHAGE GRAPHIQUE (Double fenêtre)
# ==========================================
UA = 1.496e11
x_ua = np.array(trajectoire_x) / UA
y_ua = np.array(trajectoire_y) / UA

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 1. Trajectoire spatiale
ax1.plot(x_ua, y_ua, color='orange', linestyle='--', label='Orbite de Jupiter')
ax1.plot(0, 0, marker='o', markersize=12, color='yellow', label='Soleil')
ax1.plot(x_ua[0], y_ua[0], marker='o', markersize=5, color='green', label='Départ (t=0)')
ax1.plot(x_ua[-1], y_ua[-1], marker='x', markersize=7, color='cyan', label='Arrivée (t=1 orbite)')

ax1.set_title(f"Trajectoire orbitale ({steps} jours)", fontsize=11)
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
plt.show()
