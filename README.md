# 🚇 GTFS Metro d'Alger — Ligne 1

> Open GTFS feed for Algiers Metro Line 1, with an interactive web map.

**[🗺️ Voir la carte interactive →](https://rysselharr.github.io/gtfs-metro-alger/)**

---

## Aperçu

Ce projet modélise la **Ligne 1 du Métro d'Alger** au format [GTFS](https://gtfs.org/) (General Transit Feed Specification) — le standard open data utilisé par Google Maps, OpenTripPlanner, Navitia, et tous les calculateurs d'itinéraire modernes.

Il inclut une **carte Leaflet interactive** déployée sur GitHub Pages.

![Carte du Métro d'Alger Ligne 1](docs/screenshot.png)

---

## Structure du réseau

```
Place des Martyrs ──────────────────────────────── El Harrach Centre
      │                                    (16 stations)
      │
      └── [bifurcation à Haï El Badr]
                │
                └── Haïte des Ateliers → Gué de Constantine → Ain Naadja
```

| Branche | Stations | Terminus A | Terminus B |
|---|---|---|---|
| Principale | 16 | Place des Martyrs | El Harrach Centre |
| Ain Naadja | 15 | Place des Martyrs | Ain Naadja |

**19 stations au total** · 4 trips GTFS (aller/retour × 2 branches) · Fréquence : toutes les 4 min

---

## Contenu du dépôt

```
gtfs-metro-alger/
├── gtfs/
│   └── gtfs_alger_transit_v4.zip   # Feed GTFS prêt à l'emploi
├── scripts/
│   └── generate_gtfs.py            # Script Python de génération
├── web/
│   └── index.html                  # Carte interactive Leaflet.js
└── docs/
    └── screenshot.png              # Aperçu de la carte
```

---

## Fichiers GTFS inclus

| Fichier | Description |
|---|---|
| `agency.txt` | Entreprise Métro d'Alger (EMA) |
| `routes.txt` | Ligne M1 |
| `stops.txt` | 19 stations avec coordonnées GPS |
| `trips.txt` | 4 trips directionnels |
| `stop_times.txt` | Horaires de passage |
| `frequencies.txt` | Fréquences 5h–23h |
| `shapes.txt` | Tracé géographique (aller + retour) |
| `calendar.txt` | Service 7j/7 |
| `transfers.txt` | Correspondances (Tramway, Télécabine, Train) |

---

## Utilisation

### Valider le feed GTFS

```bash
# Avec gtfs-validator (Google)
java -jar gtfs-validator.jar --input gtfs/gtfs_alger_transit_v4.zip
```

### Régénérer les fichiers

```bash
pip install requests
python scripts/generate_gtfs.py
```

### Charger dans OpenTripPlanner

```bash
# Placer le ZIP dans le dossier /graphs/alger/
# Lancer OTP avec --build et --serve
```

---

## Stack technique

- **Python 3** — génération des fichiers GTFS
- **GTFS** — format standard open transit data
- **Leaflet.js** — carte interactive web
- **OpenStreetMap** — fond de carte
- **GitHub Pages** — hébergement de la carte

---

## Sources

- Carte officielle Ligne 1 — Entreprise Métro d'Alger
- [GTFS Reference](https://gtfs.org/schedule/reference/)
- [OpenStreetMap](https://www.openstreetmap.org/)

---

## Licence

Données publiées sous licence **CC BY 4.0** — libre d'utilisation avec attribution.
