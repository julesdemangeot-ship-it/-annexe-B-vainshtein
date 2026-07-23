"""
Tests d'invariants pour ppn_check.py — validation déterministe.

Ces tests vérifient la COHÉRENCE INTERNE des formules (B.4.1)–(B.5.4).
Ils ne valident NI la valeur de β (non sourcée), NI le choix de Λ.
Un script qui passe ces tests peut produire un chiffre faux si ses
paramètres d'entrée le sont.

Usage :  python3 tests/test_ppn.py
"""

import sys
import os
import numpy as np

# Rendre scripts/ importable sans installation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import ppn_check as ppn

HBARC      = 1.973269804e-16   # GeV·m
HBAR_GEV_S = 6.582119569e-25   # GeV·s
MPC_M      = 3.0856775815e22   # m par Mpc
M_PL       = 2.435e18          # GeV
TOL        = 1e-9


def Y_exact(r, alpha, beta, M, Lam):
    """Solution exacte (B.4.2), branche régulière à l'infini."""
    rV3 = alpha * beta * M / (4.0 * np.pi * Lam**3)
    x = 4.0 * rV3 / r**3
    # Forme stable : sqrt(1+x)-1 s'annule en float64 pour x < 1e-16.
    return (Lam**3 / (2.0 * alpha)) * x / (np.sqrt(1.0 + x) + 1.0)


def residu_B41(Y, r, alpha, beta, M, Lam):
    """Résidu de la première intégrale : doit être nul."""
    return Y + (alpha / Lam**3) * Y**2 - beta * M / (4.0 * np.pi * r**3)


def r_V(alpha, beta, M, Lam):
    return (alpha * beta * M / (4.0 * np.pi * Lam**3))**(1.0 / 3.0)


def lambda_cosmo(h0_km_s_mpc=70.0):
    """Λ recalculé depuis Λ³ = M_Pl H0², jamais recopié."""
    h0_gev = (h0_km_s_mpc * 1.0e3 / MPC_M) * HBAR_GEV_S
    return (M_PL * h0_gev**2)**(1.0 / 3.0)


# Jeu de paramètres arbitraire : les tests portent sur la STRUCTURE,
# pas sur des valeurs physiques particulières.
A, B, M, L = 2.0, 1.0e-11, 1.1182e57, 5.0e-30


def t1_solution_verifie_equation():
    """(B.4.2) doit annuler (B.4.1) sur plusieurs décades."""
    rv = r_V(A, B, M, L)
    for r in rv * np.logspace(-4, 4, 40):
        res = residu_B41(Y_exact(r, A, B, M, L), r, A, B, M, L)
        ech = B * M / (4.0 * np.pi * r**3)
        assert abs(res) / ech < TOL, f"résidu {res/ech:.2e} à r/r_V={r/rv:.1e}"


def t2_limite_alpha_nul():
    """α → 0 doit redonner le régime linéaire Y = βM/4πr³.

    Évalué au rayon fixe r = r_V(α=1), pour que le point d'évaluation
    ne suive pas α. On a Y/Y_lin = 2/(√(1+4α)+1), soit un écart en O(α).

    Contrôle négatif : à α = 1 l'écart vaut ~38 % — le test discrimine.
    """
    r_ref = r_V(1.0, B, M, L)   # rayon fixe, indépendant de α
    for a in [1e-6, 1e-9, 1e-12]:
        lin  = B * M / (4.0 * np.pi * r_ref**3)
        ecart = abs(Y_exact(r_ref, a, B, M, L) - lin) / lin
        assert ecart < 1e-3, f"α={a:.0e} : écart {ecart:.2e}"
    # Contrôle négatif : à α = 1 l'écart est ~38 %, le test doit échouer
    lin_ref       = B * M / (4.0 * np.pi * r_ref**3)
    ecart_alpha1  = abs(Y_exact(r_ref, 1.0, B, M, L) - lin_ref) / lin_ref
    assert ecart_alpha1 > 0.1, (
        f"α=1 : écart {ecart_alpha1:.2e} trop petit — "
        "le contrôle négatif n'est plus discriminant"
    )


def t3_transition_a_rV():
    """À r = r_V, le terme cubique vaut (√5−1)/2 fois le terme linéaire
    (convention 'matching' du point 6 ; rapport = 1/φ ≈ 0.618)."""
    rv = r_V(A, B, M, L)
    Y  = Y_exact(rv, A, B, M, L)
    lineaire, cubique = Y, (A / L**3) * Y**2
    # Y(r_V) = Λ³/2α (√5 − 1) ⇒ rapport = (√5−1)/2 = 1/φ
    rapport = cubique / lineaire
    attendu = (np.sqrt(5.0) - 1.0) / 2.0
    assert abs(rapport - attendu) < TOL, f"rapport {rapport:.6f}"


def t4_asymptotiques():
    """Préfacteur 1 des deux côtés de (B.4.3)."""
    rv = r_V(A, B, M, L)
    # Extérieur : φ' → βM/4πr²
    r   = 1e4 * rv
    ext = (r * Y_exact(r, A, B, M, L)) / (B * M / (4.0 * np.pi * r**2))
    assert abs(ext - 1.0) < 1e-3, f"extérieur : {ext:.6f}"
    # Intérieur : φ' → βM/4πr² (r/r_V)^{3/2}
    r   = 1e-6 * rv
    ref = (B * M / (4.0 * np.pi * r**2)) * (r / rv)**1.5
    inte = (r * Y_exact(r, A, B, M, L)) / ref
    assert abs(inte - 1.0) < 1e-3, f"intérieur : {inte:.6f}"


def t5_homogeneite():
    """Invariance d'échelle : (β,M,Λ) → (kβ, M, k^{1/3}Λ) laisse r_V fixe."""
    rv0 = r_V(A, B, M, L)
    for k in [1e-6, 1e3, 1e9]:
        rv = r_V(A, k * B, M, k**(1.0 / 3.0) * L)
        assert abs(rv - rv0) / rv0 < TOL, f"k={k:.0e}"


def t6_lambda_cosmologique():
    """Λ recalculé, pas recopié. Garde-fou contre l'erreur de 11 ordres."""
    lam = lambda_cosmo()
    assert 1.5e-22 < lam < 2.0e-22, f"Λ = {lam:.3e} GeV hors plage"
    faux = 5.13e-34
    assert lam / faux > 1e10, "la valeur erronée n'est plus écartée"


def t7_loi_puissance_beta():
    """En régime écranté ε < 1, |γ − 1| ∝ β^{3/2}.

    Justifie l'inversion analytique de beta_max_cassini().
    """
    beta1 = 1.0e-20   # ε = (1e-20 * 2.435e18)^2 ≈ 5.9e-4 << 1
    beta2 = 2.0e-20
    dg1, _, valide1 = ppn.ecart_ppn(beta1, ppn.AU_M)
    dg2, _, valide2 = ppn.ecart_ppn(beta2, ppn.AU_M)
    assert valide1 and valide2, "les deux bêta doivent être dans le domaine perturbatif"
    ratio   = dg2 / dg1
    attendu = (beta2 / beta1)**(3.0 / 2.0)   # 2^{3/2} = 2.828…
    assert abs(ratio / attendu - 1.0) < 1e-6, (
        f"ratio={ratio:.6f}, attendu={attendu:.6f}"
    )


def t8_drapeau_validite():
    """Le drapeau 'valide' bascule bien à ε = 1.

    - β = 1/M_Pl → ε = 1 exactement ; doit être accepté (tolérance float64).
    - β = 1e-11  → ε ≈ 5.9×10¹⁴ >> 1 ; doit être rejeté.
    """
    beta_marginal = 1.0 / ppn.M_PL
    _, _, valide_mpl = ppn.ecart_ppn(beta_marginal, ppn.AU_M)
    assert valide_mpl, "β=1/M_Pl doit être accepté (ε=1, tolérance flottante)"

    _, _, valide_gros = ppn.ecart_ppn(1e-11, ppn.AU_M)
    assert not valide_gros, "β=1e-11 doit être rejeté (ε >> 1)"


def t9_cassini_sans_contrainte():
    """Dans le domaine valide (ε ≤ 1), Cassini n'impose aucune contrainte sur β.

    À la frontière du domaine perturbatif β = 1/M_Pl (ε = 1) :
    - |γ − 1| ≤ BOUND_CASSINI par ≥ 6 ordres de grandeur ;
    - la marge est d'au moins 10⁶, confirmant que ε ≤ 1 est le seul seuil actif.
    """
    dg_mpl, _, valide_mpl = ppn.ecart_ppn(1.0 / ppn.M_PL, ppn.AU_M)
    assert valide_mpl, "β=1/M_Pl doit être dans le domaine perturbatif (ε=1)"
    assert dg_mpl < ppn.BOUND_CASSINI, (
        f"β=1/M_Pl devrait passer Cassini (|γ−1|={dg_mpl:.3e})"
    )
    marge = ppn.BOUND_CASSINI / dg_mpl
    assert marge > 1e6, (
        f"La marge Cassini dans le domaine valide doit dépasser 10^6 : {marge:.2e}"
    )


if __name__ == "__main__":
    tests = [
        ("solution vérifie (B.4.1)",      t1_solution_verifie_equation),
        ("limite α → 0 (rayon fixe)",     t2_limite_alpha_nul),
        ("transition à r_V",              t3_transition_a_rV),
        ("asymptotiques (B.4.3)",         t4_asymptotiques),
        ("homogénéité dimensionnelle",    t5_homogeneite),
        ("Λ recalculé",                   t6_lambda_cosmologique),
        ("loi |γ−1| ∝ β^{3/2}",          t7_loi_puissance_beta),
        ("drapeau validité ε ≤ 1",        t8_drapeau_validite),
        ("Cassini sans contrainte (ε≤1)", t9_cassini_sans_contrainte),
    ]
    echecs = 0
    for nom, f in tests:
        try:
            f()
            print(f"  OK   {nom}")
        except AssertionError as e:
            print(f"  ÉCHEC {nom} : {e}")
            echecs += 1
    total = len(tests)
    print(f"\n{total - echecs}/{total} tests passés")
    print("Rappel : cohérence interne uniquement — β reste non sourcé.")
    sys.exit(echecs)
