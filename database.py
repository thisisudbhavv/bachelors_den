import os

from sqlalchemy import create_engine, text

db_conn_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_conn_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_homes():
  with engine.connect() as conn:
    result = conn.execute(text("select * from homes"))
    homes = []
    for row in result.all():
      homes.append(dict(row._mapping))
    return homes


def load_home(id):
  with engine.connect() as conn:
    result = conn.execute(text("select * from homes where id = :id"),
                          {"id": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    return dict(rows[0]._mapping)


def add_application(home_id, application):
  with engine.connect() as conn:
    query = text(
        "INSERT INTO applications (home_id, name, phone_number, email, details, people, aadhar_link) VALUES (:home_id, :name, :phone_number, :email, :details, :people, :aadhar_link)"
    )

    conn.execute(
        query, {
            "home_id": home_id,
            "name": application["name"],
            "phone_number": application["phone_number"],
            "email": application["email"],
            "details": application["details"],
            "people": application["people"],
            "aadhar_link": application["aadhar_link"]
        })