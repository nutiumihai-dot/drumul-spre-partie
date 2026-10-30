# Summit Building

Aplicație web instalabilă (PWA) pentru jurnal de antrenament, alimentație, greutate și pași, cu planuri generate și ajustate de un antrenor AI.

- Codul de aici nu conține date personale. Datele stau într-un repo privat separat, accesat prin GitHub API cu un token fine-grained introdus pe fiecare dispozitiv (salvat local, în browser).
- Modificările stau pe dispozitiv până la „Trimite notițele”; atunci pleacă toate într-un singur commit (Git Data API), după o fereastră de verificare. Funcționează și offline, cu trimitere la revenirea conexiunii.
- Pozele merg pe ramura `poze` a repo-ului de date, ca antrenorul să le poată șterge definitiv după 7 zile fără să rescrie istoricul jurnalului.
- „Antrenor fără PC” construiește un pachet de context pentru Claude de pe telefon și importă răspunsul JSON (validat) ca un commit `Antrenor: manual`.
- Pe dispozitiv se păstrează doar ultimele ~3 luni; lunile vechi se aduc la cerere pentru grafice.
- `sw.js` servește aplicația network-first, ca update-urile să apară la următoarea deschidere, și din cache când nu e internet.
- Iconițele se generează cu `python tools/make_icons.py .`.
