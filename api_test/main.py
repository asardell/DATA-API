"""API de test pour le chapitre 2 et le chapitre 3 de la formation DATA-API.

Lancement, depuis le dossier api_test :

    uvicorn main:app --reload

Documentation interactive : http://localhost:8000/docs

La base SQLite est recréée à chaque démarrage à partir de data/dpe_seed.csv,
pour que les exercices repartent toujours du même état.

Les mots de passe ci-dessous servent uniquement à la formation : ne jamais
les réutiliser pour un service réel.
"""

import csv
import os
import sqlite3
import time
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Response
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "dpe_test.sqlite"
SEED_PATH = BASE_DIR / "data" / "dpe_seed.csv"

# Token Bearer (routes POST, PUT, DELETE) et clé d'API (route /cle-api/...)
BEARER_TOKEN = os.environ.get("DATA_API_TOKEN", "token-formation-2026")
API_KEY = os.environ.get("DATA_API_KEY", "cle-formation-2026")


@contextmanager
def connexion():
    """Ouvre la base, valide les écritures à la sortie et ferme la connexion."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def initialiser_base():
    """Recrée la table dpe à partir du fichier de graine."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    with connexion() as conn:
        conn.execute(
            """
            CREATE TABLE dpe (
                numero_dpe TEXT PRIMARY KEY,
                date_reception_dpe TEXT NOT NULL,
                code_postal_ban TEXT NOT NULL,
                etiquette_dpe TEXT NOT NULL,
                surface_habitable_logement REAL
            )
            """
        )
        with open(SEED_PATH, encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                surface = ligne["surface_habitable_logement"] or None
                conn.execute(
                    "INSERT INTO dpe VALUES (?, ?, ?, ?, ?)",
                    (
                        ligne["numero_dpe"],
                        ligne["date_reception_dpe"],
                        ligne["code_postal_ban"],
                        ligne["etiquette_dpe"],
                        float(surface) if surface else None,
                    ),
                )


@asynccontextmanager
async def cycle_de_vie(app: FastAPI):
    initialiser_base()
    yield


app = FastAPI(
    title="API de test DATA-API",
    description="API locale pour tester GET, POST, PUT, DELETE, l'authentification et les erreurs.",
    version="1.0.0",
    lifespan=cycle_de_vie,
)


class DPEEntree(BaseModel):
    """Corps attendu pour créer ou remplacer un DPE."""

    numero_dpe: str = Field(min_length=5, max_length=20, examples=["2269E1179443X"])
    date_reception_dpe: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2026-01-06"])
    code_postal_ban: str = Field(pattern=r"^\d{5}$", examples=["69100"])
    etiquette_dpe: str = Field(pattern=r"^[A-G]$", examples=["D"])
    surface_habitable_logement: Optional[float] = Field(default=None, ge=0, examples=[62.7])


def verifier_bearer(authorization: Optional[str] = Header(default=None)):
    """Exige un en-tête Authorization: Bearer <token>."""
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )
    schema, _, token = authorization.partition(" ")
    if schema != "Bearer" or token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Token invalide")


def verifier_cle_api(x_api_key: Optional[str] = Header(default=None)):
    """Exige un en-tête X-API-Key valide."""
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Clé d'API manquante")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Clé d'API invalide")


def lire_dpe(conn, numero_dpe: str):
    ligne = conn.execute("SELECT * FROM dpe WHERE numero_dpe = ?", (numero_dpe,)).fetchone()
    if ligne is None:
        raise HTTPException(status_code=404, detail=f"DPE {numero_dpe} introuvable")
    return dict(ligne)


@app.get("/health", tags=["Test"])
def health():
    return {"status": "ok"}


@app.get("/dpe", tags=["DPE"])
def lister_dpe(
    etiquette: Optional[str] = Query(default=None, pattern=r"^[A-G]$"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """Liste les DPE, avec filtre optionnel sur l'étiquette et pagination."""
    with connexion() as conn:
        if etiquette:
            total = conn.execute(
                "SELECT COUNT(*) FROM dpe WHERE etiquette_dpe = ?", (etiquette,)
            ).fetchone()[0]
            lignes = conn.execute(
                "SELECT * FROM dpe WHERE etiquette_dpe = ? ORDER BY numero_dpe LIMIT ? OFFSET ?",
                (etiquette, limit, offset),
            ).fetchall()
        else:
            total = conn.execute("SELECT COUNT(*) FROM dpe").fetchone()[0]
            lignes = conn.execute(
                "SELECT * FROM dpe ORDER BY numero_dpe LIMIT ? OFFSET ?", (limit, offset)
            ).fetchall()
    return {"total": total, "limit": limit, "offset": offset, "results": [dict(l) for l in lignes]}


@app.get("/dpe/{numero_dpe}", tags=["DPE"])
def lire_un_dpe(numero_dpe: str):
    with connexion() as conn:
        return lire_dpe(conn, numero_dpe)


@app.post("/dpe", status_code=201, tags=["DPE"], dependencies=[Depends(verifier_bearer)])
def creer_dpe(dpe: DPEEntree):
    with connexion() as conn:
        existe = conn.execute(
            "SELECT 1 FROM dpe WHERE numero_dpe = ?", (dpe.numero_dpe,)
        ).fetchone()
        if existe:
            raise HTTPException(status_code=409, detail=f"DPE {dpe.numero_dpe} existe déjà")
        conn.execute(
            "INSERT INTO dpe VALUES (?, ?, ?, ?, ?)",
            (
                dpe.numero_dpe,
                dpe.date_reception_dpe,
                dpe.code_postal_ban,
                dpe.etiquette_dpe,
                dpe.surface_habitable_logement,
            ),
        )
        return lire_dpe(conn, dpe.numero_dpe)


@app.put("/dpe/{numero_dpe}", tags=["DPE"], dependencies=[Depends(verifier_bearer)])
def remplacer_dpe(numero_dpe: str, dpe: DPEEntree):
    if dpe.numero_dpe != numero_dpe:
        raise HTTPException(
            status_code=400,
            detail="numero_dpe du corps différent de celui de l'URL",
        )
    with connexion() as conn:
        lire_dpe(conn, numero_dpe)   # 404 si le DPE n'existe pas
        conn.execute(
            """
            UPDATE dpe
            SET date_reception_dpe = ?, code_postal_ban = ?,
                etiquette_dpe = ?, surface_habitable_logement = ?
            WHERE numero_dpe = ?
            """,
            (
                dpe.date_reception_dpe,
                dpe.code_postal_ban,
                dpe.etiquette_dpe,
                dpe.surface_habitable_logement,
                numero_dpe,
            ),
        )
        return lire_dpe(conn, numero_dpe)


@app.delete("/dpe/{numero_dpe}", status_code=204, tags=["DPE"], dependencies=[Depends(verifier_bearer)])
def supprimer_dpe(numero_dpe: str):
    with connexion() as conn:
        lire_dpe(conn, numero_dpe)   # 404 si le DPE n'existe pas
        conn.execute("DELETE FROM dpe WHERE numero_dpe = ?", (numero_dpe,))
    return Response(status_code=204)


@app.get("/cle-api/passoires", tags=["Authentification"], dependencies=[Depends(verifier_cle_api)])
def compter_passoires():
    """Compte les passoires énergétiques (étiquettes E, F, G). Protégé par clé d'API."""
    with connexion() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM dpe WHERE etiquette_dpe IN ('E', 'F', 'G')"
        ).fetchone()[0]
    return {"nb_passoires": total}


@app.get("/lent", tags=["Test"])
def reponse_lente(secondes: float = Query(default=3, ge=0, le=30)):
    """Attend le nombre de secondes demandé avant de répondre, pour tester les timeouts."""
    time.sleep(secondes)
    return {"attendu_secondes": secondes}
