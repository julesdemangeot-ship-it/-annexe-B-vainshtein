# Annexe B — Mécanisme de Vainshtein

Vérification numérique de l'annexe B (Propositions B.4–B.5) du manuscrit
Elasto-Gravity : profil radial du champ scalaire, rayon de Vainshtein, et
écart post-newtonien `|γ − 1|` confronté à la borne Cassini.

## ⚠️ Statut : travail en cours — résultats non validés

Ce dépôt contient un **outil de reproduction numérique**, pas une validation
physique. Deux paramètres du modèle ne sont pas encore fermés, et les
résultats affichés par le script en dépendent sur plusieurs ordres de
grandeur.

| Paramètre | Valeur utilisée | Statut | Source |
|---|---|---|---|
| `α = 2κ` | 2.0 | à confirmer | B.2.x (non tracé) |
| `Λ` | 1.76×10⁻²² GeV | dérivation vérifiée | Λ³ = M_Pl H₀², recalculé dans le script |
| `β` | balayé (voir plus bas) | NON SOURCÉ | B.1.x — ψ₀ manquant |
| `M_*` | M_Pl = 2.435×10¹⁸ GeV | approximation | suppose ξψ₀² ≪ M_Pl² |

### Statut des valeurs de Λ

Trois valeurs circulent. Le script ne code aucune d'elles en dur : il
recalcule Λ depuis M_Pl et H₀ à chaque exécution.

| Valeur | Origine | Statut |
|---|---|---|
| 1.76×10⁻²² GeV | recalcul de Λ³ = M_Pl H₀² | **dérivation vérifiée** |
| 5.13×10⁻³⁴ GeV | script antérieur | incompatible avec cette relation — corrigé |
| 10⁻³ GeV | table de `Elasto_Gravity_Jd.tex` | à interpréter (même paramètre ?) |

**À vérifier en priorité.** Établir si le Λ de la table désigne bien le
même paramètre que celui du terme cubique de (B.3.6) — même
normalisation, même dimension, après d'éventuelles redéfinitions de
champ. L'action des fichiers `.tex` fait apparaître Λ dans
`-(1/Λ³)(∂ψ)²□ψ`, au même endroit structurel que (B.3.6), ce qui est un
indice mais non une preuve : une constante absorbée reste possible et
devrait alors être documentée explicitement.

### Domaine de validité et contrainte sur β

La formule `|γ − 1| = ε·(r/r_V)^{3/2}` n'est valide que pour `ε ≡ (β·M_Pl)² ≤ 1`.
Ce garde-fou est la seule contrainte active sur β :

| Condition | Valeur de β | Conséquence |
|---|---|---|
| Seuil perturbatif (ε ≤ 1) | β ≤ 4.107×10⁻¹⁹ GeV⁻¹ | **seule contrainte valide** |
| Borne Cassini (\|γ−1\| ≤ 2.3×10⁻⁵) | β ≤ 1.042×10⁻¹⁴ GeV⁻¹ | hors domaine (ε ≈ 6×10⁸) — non exploitable |

Dans le domaine valide (β ≤ 1/M_Pl), on obtient à la frontière :
r_V ≈ 152 pc et |γ − 1| ≈ 5.7×10⁻¹² à 1 UA — **6 ordres en dessous de Cassini**.
Cassini n'impose aucune contrainte sur β ; seul ε ≤ 1 le fait.

Le résultat `|γ − 1| = 0.68` pour β = 10⁻¹¹ GeV⁻¹ (anciennement affiché)
et la conclusion « exclu par Cassini » qui s'ensuivait décrivaient le
paramètre bouché-trou hors domaine perturbatif (ε ≈ 5.9×10¹⁴ >> 1), pas le
modèle. Voir `CHANGELOG.md` pour le détail de l'erreur et sa reconstruction.

L'erreur sur Λ (5.13×10⁻³⁴ GeV au lieu de 1.76×10⁻²² GeV) est conservée
en mémoire dans le script via le test `t6` et dans ce tableau :

| Grandeur | Λ = 5.13×10⁻³⁴ GeV | Λ = 1.76×10⁻²² GeV |
|---|---|---|
| r_V (Soleil, β = 10⁻¹¹) | 4.7×10³² m | 1.4×10²¹ m (44 kpc) |
| Correction nécessaire | valeur erronée | dérivation vérifiée |

## Contenu

```
scripts/ppn_check.py    # moteur de calcul (unités naturelles homogènes)
tests/test_ppn.py       # 9 tests d'invariants (9/9 doit passer)
examples/jupiter_orbit.py  # simulation orbitale (hors annexe B)
```

## Formules implémentées

Rayon de Vainshtein, première intégrale de l'équation maîtresse (B.4.2) :

```
r_V³ = α β M / (4π Λ³)
```

Écart post-newtonien en régime écranté (B.5.4) :

```
|γ − 1| = O(ε) · (r / r_V)^{3/2}     avec  ε ≡ β² M_*²
```

L'exposant 3/2 provient de la racine du discriminant de (B.4.1) ; il est
indépendant de la normalisation du terme cubique. Seul le préfacteur
numérique de `r_V` dépend de la convention retenue pour α.

## Utilisation

```bash
python3 scripts/ppn_check.py          # rapport avec balayage en β
python3 tests/test_ppn.py             # 9 tests (code 0 si tout passe)
python3 examples/jupiter_orbit.py --save fig.png   # simulation orbitale
```

## Prochaines étapes

- [ ] **Sourcer `β` depuis B.1.x** (`β ≡ 2ξψ₀/M_*²` — la valeur de ψ₀ manque). Question à trancher : le modèle prédit-il β ~ 1/M_Pl ? Si oui, l'annexe B passe Cassini avec 6 ordres de marge et la conclusion est à réécrire.
- [ ] Établir si le Λ de la table du manuscrit est le même paramètre que celui de (B.3.6)
- [ ] Confirmer `α = 2κ` depuis la construction galiléonne (B.2.x)
- [ ] Fixer le cadre (Jordan ou Einstein) des équations linéarisées (B.5.1)

## Licence

MIT
