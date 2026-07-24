# backend/sandbox/test_students.py
"""CRUD test functions on `students` table — Work #4"""
import asyncio
import sys
from pathlib import Path

from sqlalchemy import text

# Add 'backend' (parent of this sandbox/ dir) to the path so 'db' resolves
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import engine


async def create_table():
    async with engine.begin() as conn:
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER NOT NULL,
                major VARCHAR(100) NOT NULL
            )
        """))
    print("[OK] table 'students' created")


async def insert_data():
    async with engine.begin() as conn:
        await conn.execute(text("""
            INSERT INTO students (name, age, major)
            VALUES (:name, :age, :major)
        """), [
            {"name": "Temo", "age": 21, "major": "Computer Engineering"},
            {"name": "Ball", "age": 22, "major": "Data Science"},
        ])
    print("[OK] inserted 2 rows")


async def read_data():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT * FROM students"))
        rows = result.fetchall()
        for row in rows:
            print(row)
    return rows


async def update_data():
    async with engine.begin() as conn:
        await conn.execute(text("""
            UPDATE students SET age = :age WHERE name = :name
        """), {"age": 23, "name": "Temo"})
    print("[OK] updated Temo's age -> 23")


async def delete_data():
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM students WHERE name = :name"), {"name": "Ball"})
    print("[OK] deleted row where name = Ball")


async def delete_table():
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS students"))
    print("[OK] table 'students' dropped")


async def main():
    await create_table()
    await insert_data()
    print("--- after insert ---")
    await read_data()

    await update_data()
    print("--- after update ---")
    await read_data()

    await delete_data()
    print("--- after delete ---")
    await read_data()

    await delete_table()


if __name__ == "__main__":
    asyncio.run(main())