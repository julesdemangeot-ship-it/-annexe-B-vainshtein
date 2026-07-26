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
HBARC         = 1.973269804e-16   # GeV·m
HBAR_GEV_S    = 6.582119569e-25   # GeV·s
MPC_M         = 3.0856775815e22   # m par Mpc
PC_M          = 3.0856775815e16   # m par pc
AU_M          = 1.495978707e11    # m
GEV_TO_M      = HBARC             # 1 GeV^-1 → m
M_TO_GEV_MASS = 7.571e53          # masse géométrisée (m) → GeV

# ------------------------------------------------------------------
# Paramètres du modèle
# ------------------------------------------------------------------
ALPHA = 2.0         # = 2κ, coefficient galiléon      (à confirmer, B.2.x)
BETA  = 1.0e-11     # GeV^-1, couplage conforme       (PROVISOIRE, non sourcé)
M_PL  = 2.435e18    # GeV, masse de Planck réduite
H0_KM_S_MPC = 70.0  # km/s/Mpc

# ------------------------------------------------------------------
# Λ recalculé depuis Λ³ = M_Pl H0²  (jamais recopié)
# ------------------------------------------------------------------
H0_SI      = H0_KM_S_MPC * 1.0e3 / MPC_M          # s^-1
H0_GEV     = H0_SI * HBAR_GEV_S                    # GeV
LAMBDA_GEV = (M_PL * H0_GEV**2)**(1.0 / 3.0)       # GeV

# ------------------------------------------------------------------
# Données astrophysiques et observationnelles
# ------------------------------------------------------------------
M_SUN_GEOM_M  = 1.477e3                        # m (masse géométrisée)
M_SUN_GEV     = M_SUN_GEOM_M * M_TO_GEV_MASS   # GeV
BOUND_CASSINI = 2.3e-5


# ------------------------------------------------------------------
# Fonctions de calcul
# ------------------------------------------------------------------

def r_vainshtein_m(beta, alpha=ALPHA, M_gev=M_SUN_GEV, lam=LAMBDA_GEV):
    """
    Rayon de Vainshtein en mètres.

    (B.4.2)  r_V^3 = α β M / (4π Λ^3)
    """
    r_V_gev_inv = (alpha * beta * M_gev / (4.0 * np.pi * lam**3))**(1.0 / 3.0)
    return r_V_gev_inv * HBARC


def ecart_ppn(beta, r_m, alpha=ALPHA, M_gev=M_SUN_GEV, lam=LAMBDA_GEV, M_pl=M_PL):
    """
    Calcule l'écart post-newtonien |γ − 1|.

    Paramètres
    ----------
    beta  : couplage conforme (GeV^-1)
    r_m   : distance d'évaluation (m)

    Retourne
    --------
    (delta, regime, valide)
      delta  : |γ − 1|  (valeur formelle, ne pas interpréter si valide=False)
      regime : chaîne décrivant le régime d'écrantage
      valide : True seulement si ε = (β M_*)² ≤ 1+1e-9
               Le développement perturbatif n'a de sens que pour ε ≲ 1.
               Une tolérance de 1e-9 est prévue pour le bord exact ε = 1
               (β = 1/M_Pl) afin d'éviter un rejet par arrondi float64.
    """
    eps    = (beta * M_pl)**2
    valide = eps <= 1.0 + 1e-9

    rv = r_vainshtein_m(beta, alpha, M_gev, lam)
    if r_m < rv:
        delta  = eps * (r_m / rv)**1.5
        regime = "écranté (r << r_V)"
    else:
        delta  = eps
        regime = "NON écranté (r >~ r_V)"

    return delta, regime, valide


def beta_max_cassini(alpha=ALPHA, M_gev=M_SUN_GEV, lam=LAMBDA_GEV,
                     r_m=AU_M, M_pl=M_PL, bound=BOUND_CASSINI):
    """
    Valeur maximale de β compatible avec la borne Cassini, en régime écranté.

    En régime écranté :
        |γ − 1| = ε · (r/r_V)^{3/2}   avec ε = (β M_pl)²

    Comme r_V ∝ β^{1/3}, on a (r/r_V)^{3/2} ∝ β^{-1/2},
    d'où |γ − 1| = K · β^{3/2}  (loi de puissance).

    En posant K · β^{3/2} = bound, on obtient β = (bound/K)^{2/3}.

    C = r_V(β=1) en mètres, K = M_pl² · (r/C)^{3/2}.
    """
    C = (alpha * M_gev / (4.0 * np.pi * lam**3))**(1.0 / 3.0) * HBARC
    K = M_pl**2 * (r_m / C)**1.5
    return (bound / K)**(2.0 / 3.0)


# ------------------------------------------------------------------
# Rapport
# ------------------------------------------------------------------
if __name__ == "__main__":
    LAMBDA_M_INV = LAMBDA_GEV / HBARC   # m^-1

    print("=" * 68)
    print("RAPPORT DE CONTRÔLE NUMÉRIQUE — ARCHITECTURE B")
    print("=" * 68)
    print(f"H0                  : {H0_KM_S_MPC:.1f} km/s/Mpc = {H0_GEV:.3e} GeV")
    print(f"Λ (recalculé)       : {LAMBDA_GEV:.3e} GeV = {LAMBDA_M_INV:.3e} m^-1")
    print(f"  longueur 1/Λ      : {HBARC / LAMBDA_GEV:.3e} m")
    print(f"α                   : {ALPHA}          (à confirmer, B.2.x)")
    print(f"β (valeur test)     : {BETA:.2e} GeV^-1   (PROVISOIRE, non sourcé)")
    print("-" * 68)

    # Seuil perturbatif (seule contrainte valide sur β)
    beta_pert = 1.0 / M_PL
    rv_mpl    = r_vainshtein_m(beta_pert)
    dg_mpl, _, _ = ecart_ppn(beta_pert, AU_M)

    print(f"Seuil perturbatif   : β ≤ {beta_pert:.3e} GeV^-1  (ε ≤ 1)")
    print(f"  Dans ce domaine : |γ − 1| ≤ {dg_mpl:.3e}  (à β = 1/M_Pl, r = 1 UA)")
    print(f"  Marge Cassini   : {BOUND_CASSINI / dg_mpl:.1e}× — Cassini n'impose"
          f" aucune contrainte sur β, seul ε ≤ 1 le fait.")
    print(f"r_V à β = 1/M_Pl   : {rv_mpl / PC_M:.1f} pc")
    print("-" * 68)

    # Balayage en β
    print()
    print("Balayage en β :")
    print(f"{'β (GeV^-1)':>14}  {'β·M_Pl':>10}  {'r_V (pc)':>10}  "
          f"{'ε':>10}  {'|γ−1|':>12}  {'verdict':}")
    print("-" * 80)

    betas = [
        ("1/M_Pl",        1.0 / M_PL),
        ("10^-18",        1e-18),
        ("10^-17",        1e-17),
        ("10^-16",        1e-16),
        ("10^-15",        1e-15),
        ("10^-14",        1e-14),
        ("10^-13",        1e-13),
        ("10^-12",        1e-12),
        ("10^-11 (test)", BETA),
    ]

    for label, b in betas:
        rv  = r_vainshtein_m(b)
        eps = (b * M_PL)**2
        dg, regime, valide = ecart_ppn(b, AU_M)
        if not valide:
            verdict = "epsilon>1 : NON EXPLOITABLE"
            dg_str  = "—"
        elif dg < BOUND_CASSINI:
            verdict = "passe Cassini"
            dg_str  = f"{dg:.3e}"
        else:
            verdict = "EXCLU Cassini"
            dg_str  = f"{dg:.3e}"
        row = (f"  {b:.3e}  {b * M_PL:>10.3e}  {rv / PC_M:>10.2f}  "
               f"{eps:>10.2e}  {dg_str:>12}  {verdict}")
        print(row)

    print()
    print("⚠️  AVERTISSEMENT SCIENTIFIQUE")
    print("β n'est pas dérivé du manuscrit : les valeurs de r_V, ε et |γ − 1|")
    print("ci-dessus ne constituent pas une validation physique du modèle.")
    print("La valeur de Λ retenue ici découle de Λ³ = M_Pl H0² ; elle reste à")
    print("réconcilier avec Λ = 1e-3 GeV figurant dans la table du manuscrit.")
    print("=" * 68)
