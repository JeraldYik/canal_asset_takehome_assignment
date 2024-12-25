import argparse

from model import SocialMediaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def query_db(source=""):
    engine = create_engine("sqlite:///local.db", echo=True)

    session = sessionmaker(bind=engine)()
    data = (
        session.query(SocialMediaData)
        .filter(SocialMediaData.source == source if source else True)
        .all()
    )
    for row in data:
        print(row)
        print("\n--------------------------------\n")

    print(f"\nQuery found {len(data)} rows")
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="", help="Query db on 'source'")
    args = parser.parse_args()
    query_db(source=args.source)
