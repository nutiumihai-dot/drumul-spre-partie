# Summit Building

Aplicație web instalabilă (PWA) pentru jurnal de antrenament, alimentație, greutate și pași, cu planuri generate și ajustate de un antrenor AI.

- Codul de aici nu conține date personale. Datele stau într-un repo privat separat, accesat prin GitHub API cu un token fine-grained introdus pe fiecare dispozitiv (salvat local, în browser).
- Fiecare salvare devine un commit în repo-ul de date. Salvările făcute offline stau la coadă și pleacă la revenirea conexiunii.
- `sw.js` servește aplicația network-first, ca update-urile să apară la următoarea deschidere, și din cache când nu e internet.
- Iconițele se generează cu `python tools/make_icons.py .`.
