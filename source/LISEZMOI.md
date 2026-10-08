# Source du générateur de lettres d'expertise

- `tool.src.html` : la page (formulaire + aperçu + génération du Word), avec `__TEMPLATE_B64__` à la place du gabarit.
- `template.docx` : gabarit Word tokenisé (`{{CHAMP}}`, blocs `<!--IF:X-->…<!--ENDIF:X-->`), construit à partir de « Modèle AI.docx » par `build_template.py`.
- `build_site.py` : produit `../index.html` (site GitHub Pages) à partir de `tool.src.html` + `template.docx`.
- `build.py` : produit la version artefact Claude.
Les chemins dans les scripts pointent vers l'espace de travail de la session d'origine (/home/claude/fosse) : à ajuster si on les relance ailleurs.
