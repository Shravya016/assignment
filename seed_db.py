from app.db.seed import seed_database

if __name__ == "__main__":
    print("Seeding database...")
    seed_database()
    print("Done!") 