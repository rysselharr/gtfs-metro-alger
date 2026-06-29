import os
import csv
import zipfile

OUTPUT_DIR = "gtfs_transit_alger_v4"
ZIP_FILENAME = "gtfs_alger_transit_v4.zip"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_gtfs_file(filename, headers, rows):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"[OK] {filename} ({len(rows)} lignes)")

# ── STATIONS ─────────────────────────────────────────────────────────────────
# Source : carte officielle Ligne 1 Métro d'Alger
# Ligne principale : Place des Martyrs → El Harrach Centre (16 stations)
# Branche : bifurcation à Hai El Badr → Ain Naadja (3 stations supplémentaires)

MAIN_LINE = [
    ["ST_PLACE_DES_MARTYRS",     "Place des Martyrs",          "36.7847",  "3.0621",  "0"],
    ["ST_ALI_BOUMENJEL",         "Ali Boumenjel",              "36.7800",  "3.0610",  "0"],  
    ["ST_TAFOURAH_GRANDE_POSTE", "Tafourah - Grande Poste",    "36.7725",  "3.0583",  "0"],
    ["ST_KHELIFA_BOUKHALFA",     "Khelifa Boukhalfa",          "36.7651",  "3.0519",  "0"],
    ["ST_1ER_MAI",               "1er Mai",                    "36.7533",  "3.0475",  "0"],
    ["ST_AISSAT_IDIR",           "Aissat Idir",                "36.7505",  "3.0522",  "0"],
    ["ST_HAMMA",                 "Hamma",                      "36.7468",  "3.0611",  "0"],
    ["ST_JARDIN_ESSAI",          "Jardin d'Essai du Hamma",    "36.7432",  "3.0678",  "0"],
    ["ST_LES_FUSILLES",          "Les Fusillés",               "36.7388",  "3.0651",  "0"],
    ["ST_CITE_AMIROUCHE",        "Cité Amirouche",             "36.7341",  "3.0712",  "0"],
    ["ST_CITE_MER_SOLEIL",       "Cité Mer et Soleil",         "36.7298",  "3.0789",  "0"],
    ["ST_HAI_EL_BADR",           "Haï El Badr",                "36.7195",  "3.0906",  "0"],  # ← bifurcation
    ["ST_BACHDJARAH_TENNIS",     "Bachdjarah - Tennis",        "36.7201",  "3.1051",  "0"],
    ["ST_BACHDJARAH",            "Bachdjarah",                 "36.7208",  "3.1178",  "0"],
    ["ST_EL_HARRACH_GARE",       "El Harrach Gare",            "36.7211",  "3.1289",  "0"],
    ["ST_EL_HARRACH_CENTRE",     "El Harrach Centre",          "36.7212",  "3.1322",  "0"],
]

# Stations de la branche Ain Naadja (après bifurcation à Hai El Badr)
BRANCH_ONLY = [
    ["ST_HAITE_DES_ATELIERS", "Haïte des Ateliers", "36.7130",  "3.0820",  "0"],  
    ["ST_GUE_DE_CONSTANTINE", "Gué de Constantine", "36.7095",  "3.0750",  "0"],  
    ["ST_AIN_NAADJA",         "Ain Naadja",         "36.7050",  "3.0670",  "0"],  
]

# Branche complète : Place des Martyrs → … → Hai El Badr → Ain Naadja
# Les 12 premières stations sont communes avec la ligne principale (indices 0-11)
BRANCH_AIN_NAADJA = MAIN_LINE[:12] + BRANCH_ONLY

ALL_STOPS = MAIN_LINE + BRANCH_ONLY  # pas de doublons : BRANCH_ONLY = stations exclusives à la branche

# ── INTERVALS (minutes entre stations) ───────────────────────────────────────
# Ligne principale : 16 stations → 15 intervalles
INTERVALS_MAIN   = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2]
# Branche Ain Naadja : 15 stations (12 communes + 3 branche) → 14 intervalles
INTERVALS_BRANCH = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]

def build_stop_times(trip_id, stops, intervals, start_hour=5, start_min=0):
    rows = []
    current_min = start_min
    for i, stop in enumerate(stops):
        h = start_hour + current_min // 60
        m = current_min % 60
        arr = f"{h:02d}:{m:02d}:00"
        dep = arr if (i == 0 or i == len(stops) - 1) else f"{h:02d}:{m:02d}:30"
        rows.append([trip_id, arr, dep, stop[0], str(i + 1)])
        if i < len(intervals):
            current_min += intervals[i]
    return rows

def build_shapes():
    rows = []
    for seq, stop in enumerate(MAIN_LINE):
        rows.append(["SH_MAIN_ALLER",   stop[2], stop[3], str(seq)])
    for seq, stop in enumerate(reversed(MAIN_LINE)):
        rows.append(["SH_MAIN_RETOUR",  stop[2], stop[3], str(seq)])
    for seq, stop in enumerate(BRANCH_AIN_NAADJA):
        rows.append(["SH_BRANCH_ALLER", stop[2], stop[3], str(seq)])
    for seq, stop in enumerate(reversed(BRANCH_AIN_NAADJA)):
        rows.append(["SH_BRANCH_RETOUR",stop[2], stop[3], str(seq)])
    return rows

# ── ÉCRITURE DES FICHIERS GTFS ───────────────────────────────────────────────

write_gtfs_file("agency.txt",
    ["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang"],
    [["EMA", "Entreprise Métro d'Alger", "https://metro-eldjazair.dz/", "Africa/Algiers", "fr"]])

write_gtfs_file("feed_info.txt",
    ["feed_publisher_name", "feed_publisher_url", "feed_lang",
     "feed_start_date", "feed_end_date", "feed_version", "feed_contact_email"],
    [["Entreprise Métro d'Alger", "https://metro-eldjazair.dz/", "fr",
      "20260101", "20261231", "2026.4", "contact@metro-eldjazair.dz"]])

write_gtfs_file("calendar.txt",
    ["service_id", "monday", "tuesday", "wednesday", "thursday",
     "friday", "saturday", "sunday", "start_date", "end_date"],
    [["DAILY_SERVICE", "1", "1", "1", "1", "1", "1", "1", "20260101", "20261231"]])

write_gtfs_file("routes.txt",
    ["route_id", "agency_id", "route_short_name", "route_long_name",
     "route_type", "route_color", "route_text_color"],
    [["M1", "EMA", "1", "Ligne 1 : Place des Martyrs ↔ El Harrach Centre / Ain Naadja",
      "1", "0072BC", "FFFFFF"]])

write_gtfs_file("stops.txt",
    ["stop_id", "stop_name", "stop_lat", "stop_lon", "location_type"],
    ALL_STOPS)

write_gtfs_file("trips.txt",
    ["route_id", "service_id", "trip_id", "direction_id", "shape_id"],
    [
        ["M1", "DAILY_SERVICE", "TR_MARTYRS_HARRACH",   "0", "SH_MAIN_ALLER"],
        ["M1", "DAILY_SERVICE", "TR_HARRACH_MARTYRS",   "1", "SH_MAIN_RETOUR"],
        ["M1", "DAILY_SERVICE", "TR_MARTYRS_AINNAADJA", "0", "SH_BRANCH_ALLER"],
        ["M1", "DAILY_SERVICE", "TR_AINNAADJA_MARTYRS", "1", "SH_BRANCH_RETOUR"],
    ])

st_main_aller  = build_stop_times("TR_MARTYRS_HARRACH",   MAIN_LINE,                          INTERVALS_MAIN)
st_main_retour = build_stop_times("TR_HARRACH_MARTYRS",   list(reversed(MAIN_LINE)),           INTERVALS_MAIN)
st_ain_aller   = build_stop_times("TR_MARTYRS_AINNAADJA", BRANCH_AIN_NAADJA,                  INTERVALS_BRANCH)
st_ain_retour  = build_stop_times("TR_AINNAADJA_MARTYRS", list(reversed(BRANCH_AIN_NAADJA)),  INTERVALS_BRANCH)

write_gtfs_file("stop_times.txt",
    ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"],
    st_main_aller + st_main_retour + st_ain_aller + st_ain_retour)

write_gtfs_file("frequencies.txt",
    ["trip_id", "start_time", "end_time", "headway_secs"],
    [
        ["TR_MARTYRS_HARRACH",   "05:00:00", "23:00:00", "240"],
        ["TR_HARRACH_MARTYRS",   "05:00:00", "23:00:00", "240"],
        ["TR_MARTYRS_AINNAADJA", "05:00:00", "23:00:00", "240"],
        ["TR_AINNAADJA_MARTYRS", "05:00:00", "23:00:00", "240"],
    ])

write_gtfs_file("transfers.txt",
    ["from_stop_id", "to_stop_id", "transfer_type", "min_transfer_time"],
    [
        ["ST_LES_FUSILLES", "ST_LES_FUSILLES", "2", "0"],  # Télécabine
        ["ST_CITE_AMIROUCHE","ST_CITE_AMIROUCHE","2","0"],  # Tramway
        ["ST_HAI_EL_BADR",  "ST_HAI_EL_BADR",  "2", "0"],  # bifurcation branche
    ])

write_gtfs_file("shapes.txt",
    ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"],
    build_shapes())

GTFS_FILES = [
    "agency.txt", "calendar.txt", "feed_info.txt", "frequencies.txt",
    "routes.txt", "shapes.txt", "stop_times.txt", "stops.txt",
    "transfers.txt", "trips.txt"
]

with zipfile.ZipFile(ZIP_FILENAME, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in GTFS_FILES:
        z.write(os.path.join(OUTPUT_DIR, f), arcname=f)

print(f"\n[SUCCÈS] ZIP prêt : '{ZIP_FILENAME}'")
print(f"  Stations totales : {len(ALL_STOPS)}")
print(f"    • Ligne principale (Martyrs ↔ El Harrach Centre) : {len(MAIN_LINE)} stations")
print(f"    • Branche exclusive (Hai El Badr → Ain Naadja)  : {len(BRANCH_ONLY)} stations")
print(f"  Shapes   : 4 (aller + retour × 2 branches)")
print(f"  Fichiers dans le ZIP : {len(GTFS_FILES)}")
print(f"\n  Corrections apportées vs v3 :")
print(f"    + Ali Boumenjel ajoutée (manquante)")
print(f"    + Haïte des Ateliers ajoutée (manquante)")
print(f"    + Gué de Constantine ajoutée (manquante)")
print(f"    - Ruisseau supprimée (absente de la carte officielle)")
print(f"    ~ INTERVALS_MAIN mis à jour : 15 intervalles pour 16 stations")
print(f"    ~ INTERVALS_BRANCH mis à jour : 14 intervalles pour 15 stations")
