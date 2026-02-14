from fastapi import APIRouter
from psycopg import Connection
from app.database import get_connection
from app.schemas import ContactCreate, ContactResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(body: ContactCreate):
    conn: Connection = get_connection()
    try:
        with conn.transaction():
            cur = conn.execute(
                "INSERT INTO address_book (name, phone, email) VALUES (%s, %s, %s) RETURNING id, name, phone, email",
                (body.name, body.phone, body.email),
            )
            row = cur.fetchone()
            if row is None:
                raise RuntimeError("INSERT did not return a row")
    finally:
        conn.close()
    return ContactResponse(id=row[0], name=row[1], phone=row[2], email=row[3])

@router.get("/", response_model=list[ContactResponse])
def get_contacts():
    conn: Connection = get_connection()
    try:
        with conn.transaction():
            cur = conn.execute("SELECT id, name, phone, email FROM address_book")
            rows = cur.fetchall()
    finally:
        conn.close()
    return [ContactResponse(id=r[0], name=r[1], phone=r[2], email=r[3]) for r in rows]