# CHANGELOG

## [Unreleased] — restructuration complète

### Contexte

Ce dépôt vérifie numériquement l'annexe B (Propositions B.4–B.5) d'un manuscrit
de gravité modifiée : rayon de Vainshtein et écart post-newtonien `|γ − 1|`
confronté à la borne Cassini (2.3×10⁻⁵).

---

### Tâche 1 — Nettoyage et arborescence

**Supprimés** (doublons octet-pour-octet ou hors sujet) :

- `Ppn Check` — copie identique de `ppn_check.py`
- `README2` — copie identique de `README.md`
- `annexe-B-vainshtein-patch.zip` — archive à la racine

**Déplacés / renommés** :

| Ancien chemin | Nouveau chemin |
|---|---|
| `ppn_check.py` | `scripts/ppn_check.py` |
| `Test ppn` | `tests/test_ppn.py` |
| `jupiter_simulation.py` | `examples/jupiter_orbit.py` |

Le fichier `Test ppn` (avec espace, sans extension) rendait impossible
`python3 test_ppn.py` annoncé dans sa propre docstring.

---

### Tâche 2 — Garde-fou sur ε (défaut principal)

`|γ − 1| = O(ε)·(r/r_V)^{3/2}` est un **développement perturbatif en
`ε ≡ β²M_*²`** qui n'a de sens que pour ε ≲ 1.

Avec la valeur de test `β = 1×10⁻¹¹ GeV⁻¹`, on obtenait ε = 5.9×10¹⁴.
Le script affichait pourtant `|γ − 1| = 0.68` et concluait « exclu par
Cassini » — conclusion tirée d'une formule hors domaine.

**Correctif** : extraction dans `ecart_ppn(beta, r_m, ...)` renvoyant
`(|γ − 1|, régime, valide)` avec `valide = (ε ≤ 1 + 1e‑9)`. Le rapport
n'émet aucun verdict Cassini quand `valide` est faux ; il affiche
`epsilon>1 : NON EXPLOITABLE`.

La tolérance 1e‑9 est prévue pour que `β = 1/M_Pl` (ε = 1 exact en
mathématique) ne soit pas rejeté par un arrondi float64.

---

### Tâche 3 — Balayage en β au lieu d'une valeur unique

`β` n'est pas dérivé du manuscrit. Le script affiche désormais un tableau
balayant β, avec pour chaque valeur : `β`, `β·M_Pl`, `r_V`, `ε`,
`|γ − 1|`, verdict.

Ajout de `beta_max_cassini()` : inversion analytique de la loi de puissance
`|γ − 1| = K·β^{3/2}` (en régime écranté, `r_V ∝ β^{1/3}`).

**Résultat** : c'est `ε < 1` qui contraint β le plus sévèrement, pas Cassini
(4.5 ordres de différence : β_pert ≈ 4.1×10⁻¹⁹ contre β_Cas ≈ 1.0×10⁻¹⁴).

---

### Tâche 4 — Réparation de `t2` (test sans pouvoir discriminant)

Le test `t2_limite_alpha_nul` évaluait à `r = 1e6·r_V(α)`. Comme
`r_V ∝ α^{1/3}`, le point d'évaluation suivait α : l'écart valait ~10⁻¹⁶
**pour tout α**, y compris α = 1×10¹². Le test passait mais ne testait pas
la limite α → 0.

**Correctif** : évaluation au rayon fixe `r = r_V(α=1)`.  
À ce rayon, `Y/Y_lin = 2/(√(1+4α)+1)`, soit un écart en O(α) aux petits α.

**Contrôle négatif ajouté** : vérification que le test échoue bien à α = 1
(écart ≈ 38 %), prouvant qu'il est réellement discriminant.

---

### Tâche 5 — Correction de la docstring de `t3`

La docstring affirmait qu'à `r = r_V` les deux termes de (B.4.1) étaient
« égaux », alors que l'assertion vérifie un rapport de `(√5−1)/2 ≈ 0.618`.
L'assertion est juste, le commentaire était faux. Le commentaire a été corrigé.

---

### Tâche 6 — Trois nouveaux tests

- **t7** — loi de puissance `|γ − 1| ∝ β^{3/2}` en régime écranté ;
  justifie l'inversion analytique de `beta_max_cassini()`.
- **t8** — le drapeau de validité bascule bien à ε = 1 :
  `β = 1/M_Pl` est accepté, `β = 1e-11` est rejeté.
- **t9** — `beta_max_cassini()` sature exactement la borne Cassini à 1 ppm ;
  `β = 1/M_Pl` passe Cassini avec `|γ − 1| ≈ 5.7×10⁻¹²`.

Le fichier de tests renvoie un code de sortie non nul en cas d'échec
(exploitable en CI).

---

### Tâche 7 — Mise à jour du README

#### Erreur documentée : la valeur « β ≲ 10⁻²³ GeV⁻¹ »

Le README précédent affirmait :

> β ≲ 10⁻²³ GeV⁻¹ (soit β·M_Pl ≲ 10⁻⁵) rend le modèle compatible [avec Cassini].

Cette valeur résultait d'un calcul posant `|γ − 1| = β·M_Pl`, omettant à la
fois le carré (`ε = (β·M_Pl)²`) et le facteur d'écrantage `(r/r_V)^{3/2}`.
Ce raccourci donne `β·M_Pl = 2.30×10⁻⁵`, c'est-à-dire la borne Cassini
elle-même arrondie en « ≲ 10⁻⁵ ». C'est une erreur, pas une convention.

La valeur `10⁻²³` est retirée du README et remplacée par le tableau des
deux seuils corrects. L'ancienne valeur de 0.68 pour `|γ − 1|` (paramètre
bouché-trou hors domaine perturbatif) est également retirée.

---

### Tâche 8 — Corrections de `examples/jupiter_orbit.py`

- **Diagnostic d'énergie** : l'ancienne version évaluait l'énergie cinétique
  avec la vitesse post-mise-à-jour mais la distance pré-mise-à-jour (décalage
  d'un demi-pas Euler-Cromer), gonflant la dérive affichée. Corrigé : énergie
  évaluée au même instant (vitesse et position cohérentes).
- **Titre** : l'orbite était circulaire (v_init = v_circ théorique au rayon
  du demi-grand axe), pas l'orbite elliptique de Jupiter (e = 0.0489). Le titre
  le dit maintenant explicitement.
- **Option `--save fichier.png`** : ajoutée pour exécution sans affichage
  (environnements headless, CI).
