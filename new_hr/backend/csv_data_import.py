import base64
import csv
import logging
import os

import sqlalchemy
from models import Department, Employee, Position, SessionLocal, engine


def create_database_with_data():
    log = logging.getLogger("main")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    drop_table = os.getenv("DROP_TABLE", True)

    log.info("Reading csv file.....")
    with open("csv_data.csv", "r", encoding="utf-8-sig") as file_:
        csv_file = csv.DictReader(file_, delimiter=";")
        data = [row for row in csv_file]

    departments = set(row['department'] for row in data)
    log.info("Extracted departments: `%s`", departments)

    positions = set(row['position'] for row in data)
    log.info("Extracted Positions: `%s`", positions)

    db = SessionLocal()
    if drop_table:
        log.info("Dropping tables!")
        Employee.__table__.drop(engine)
        Department.__table__.drop(engine)
        Position.__table__.drop(engine)

    log.info("Creating tables.....")
    Department.__table__.create(bind=engine, checkfirst=True)
    Position.__table__.create(bind=engine, checkfirst=True)
    Employee.__table__.create(bind=engine, checkfirst=True)

    departments_dict = {}
    for idx, department in enumerate(departments):
        departments_dict[department] = idx + 1
        try:
            db.add(Department(name=department))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            print(f"Department with name `{department}` already exists!")

    positions_dict = {}
    for idx, position in enumerate(positions):
        positions_dict[position] = idx + 1
        try:
            db.add(Position(name=position))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            print(f"Position with name `{position}` already exists!")

    with open("img.png", "rb") as pic:
        b_64_img = base64.b64encode(pic.read())

    for row in data:
        log.info("Inserting `%s` into database...", row["display_name"])
        row["picture"] = b_64_img
        row["position_id"] = positions_dict.get(row["position"])
        row["department_id"] = departments_dict.get(row["department"])
        del row["position"]
        del row["department"]
        db.add(Employee(**row))
        db.commit()

        
if __name__ == "__main__":
    create_database_with_data()