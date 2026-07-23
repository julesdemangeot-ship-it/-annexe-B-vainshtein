"""
Contrôle numérique de l'architecture B (Propositions B.4–B.5).

ATTENTION
---------
Outil de reproduction numérique, pas de validation physique.

Deux paramètres restent ouverts :
  - β n'est pas dérivé d'une ligne du manuscrit (B.1.x) ;
  - la valeur de Λ du terme cubique reste à réconcilier avec la table
    de paramètres du manuscrit (Λ = 1e-3 GeV), cf. README.

Aucune valeur de Λ n'est codée en dur : elle est recalculée depuis M_Pl
et H0, précisément pour qu'une erreur de dérivation ne puisse pas se
propager silencieusement (une valeur antérieure de 5.13e-34 GeV,
présentée comme issue de Λ³ = M_Pl H0², s'écartait de 11 ordres de
grandeur du résultat correct).
"""

import numpy as np

# ------------------------------------------------------------------
# Constantes fondamentales et conversions (ħ = c = 1)
# ------------------------------------------------------------------
HBARC      = 1.973269804e-16   # GeV·m
HBAR_GEV_S = 6.582119569e-25   # GeV·s
MPC_M      = 3.0856775815e22   # m par Mpc
PC_M       = 3.0856775815e16   # m par pc
AU_M       = 1.495978707e11    # m
GEV_TO_M   = HBARC             # 1 GeV^-1 -> m
M_TO_GEV_MASS = 7.571e53       # masse géométrisée (m) -> GeV

# ------------------------------------------------------------------
# Paramètres du modèle
# ------------------------------------------------------------------
ALPHA = 2.0        # = 2κ, coefficient galiléon      (à confirmer, B.2.x)
BETA  = 1.0e-11    # GeV^-1, couplage conforme       (PROVISOIRE, non sourcé)
M_PL  = 2.435e18   # GeV, masse de Planck réduite
H0_KM_S_MPC = 70.0 # km/s/Mpc

# ------------------------------------------------------------------
# Λ recalculé depuis Λ³ = M_Pl H0²  (jamais recopié)
# ------------------------------------------------------------------
H0_SI  = H0_KM_S_MPC * 1.0e3 / MPC_M          # s^-1
H0_GEV = H0_SI * HBAR_GEV_S                   # GeV
LAMBDA_GEV = (M_PL * H0_GEV**2)**(1.0 / 3.0)  # GeV
LAMBDA_M_INV = LAMBDA_GEV / HBARC             # m^-1

# ------------------------------------------------------------------
# Données astrophysiques et observationnelles
# ------------------------------------------------------------------
M_SUN_GEOM_M = 1.477e3                        # m (masse géométrisée)
M_SUN_GEV    = M_SUN_GEOM_M * M_TO_GEV_MASS   # GeV
BOUND_CASSINI = 2.3e-5
R_UNIVERS_OBSERVABLE_M = 4.4e26               # rayon comobile (~14.3 Gpc)

# ------------------------------------------------------------------
# Moteur de calcul
# ------------------------------------------------------------------
# (B.4.2)  r_V^3 = α β M / (4π Λ^3)
r_V_gev_inv = (ALPHA * BETA * M_SUN_GEV / (4.0 * np.pi * LAMBDA_GEV**3))**(1/3)
r_V_m = r_V_gev_inv * GEV_TO_M

epsilon = (BETA * M_PL)**2                    # ε ≡ β² M_*², avec M_* ≈ M_Pl
ratio_univ = r_V_m / R_UNIVERS_OBSERVABLE_M
ecrante = AU_M < r_V_m

# (B.5.4) : écranté -> O(ε)(r/r_V)^{3/2} ; non écranté -> O(ε)
if ecrante:
    delta_gamma = epsilon * (AU_M / r_V_m)**1.5
    regime = "écranté (r << r_V)"
else:
    delta_gamma = epsilon
    regime = "NON écranté (r >~ r_V) — la suppression Vainshtein ne joue pas"

# ------------------------------------------------------------------
# Rapport
# ------------------------------------------------------------------
print("=" * 68)
print("RAPPORT DE CONTRÔLE NUMÉRIQUE — ARCHITECTURE B")
print("=" * 68)
print(f"H0                  : {H0_KM_S_MPC:.1f} km/s/Mpc = {H0_GEV:.3e} GeV")
print(f"Λ (recalculé)       : {LAMBDA_GEV:.3e} GeV = {LAMBDA_M_INV:.3e} m^-1")
print(f"  longueur 1/Λ      : {HBARC / LAMBDA_GEV:.3e} m")
print(f"α                   : {ALPHA}          (à confirmer, B.2.x)")
print(f"β                   : {BETA:.2e} GeV^-1   (PROVISOIRE, non sourcé)")
print("-" * 68)
print(f"Rayon de Vainshtein : {r_V_m:.3e} m = {r_V_m / PC_M:.2f} pc")
print(f"r_V / R_univers     : {ratio_univ:.2e}")
print(f"Paramètre ε         : {epsilon:.3e}")
print(f"Régime à 1 UA       : {regime}")
print(f"Écart PPN |γ − 1|   : {delta_gamma:.3e}")
print(f"Borne Cassini       : < {BOUND_CASSINI:.1e}")
print("-" * 68)

if ratio_univ > 100:
    print("⚠️  ALERTE : r_V dépasse 100× le rayon de l'univers observable.")
    print("   Signale une erreur d'unité ou un paramètre inapproprié.")

print("⚠️  AVERTISSEMENT SCIENTIFIQUE")
print("β n'est pas dérivé du manuscrit : les valeurs de r_V, ε et |γ − 1|")
print("ci-dessus ne constituent pas une validation physique du modèle.")
print("La valeur de Λ retenue ici découle de Λ³ = M_Pl H0² ; elle reste à")
print("réconcilier avec Λ = 1e-3 GeV figurant dans la table du manuscrit.")
print("=" * 68)
