import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from datetime import UTC, datetime

from financial_app.db.session import session_maker
from financial_app.db.schemas.schemas import CategorySchema
from financial_app.utils import normalize_name

CATEGORIES = [
    "Assinaturas",
    "Mercado / Casa",
    "Alimentação fora",
    "Lanches / Café",
    "Bares e social",
    "Relacionamento",
    "Presentes",
    "Saúde / Medicamentos",
    "Higiene pessoal",
    "Academia e cuidados pessoais",
    "Transporte",
    "Estudos / Trabalho",
    "Tabaco / Álcool",
]


def insert_categories(session) -> None:
    now = datetime.now(UTC)
    inserted = 0
    skipped = 0

    for raw_name in CATEGORIES:
        name = normalize_name(raw_name)
        exists = session.query(CategorySchema).filter(CategorySchema.name == name).first()
        if exists:
            print(f"  [skip]   {name}")
            skipped += 1
            continue

        session.add(CategorySchema(name=name, created_at=now, updated_at=now))
        print(f"  [insert] {name}")
        inserted += 1

    session.commit()
    print(f"\nDone: {inserted} inserted, {skipped} skipped.")


if __name__ == "__main__":
    print("Inserting initial categories...")
    with session_maker() as session:
        insert_categories(session)
