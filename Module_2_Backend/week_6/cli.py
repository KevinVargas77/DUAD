import argparse
from config import engine, SessionLocal
from models import Base
from managers import UserManager, CarManager, AddressManager
from seeds import seed_with_faker

def print_user_assets(session, user_id):
    user = session.get(UserManager.model_class, user_id)
    if not user:
        print(f"User id={user_id} not found")
        return
    print(f"User: {user.name} (id={user.id})")
    print("Cars:")
    if hasattr(user, 'cars') and user.cars:
        for c in user.cars:
            print(f"  - {c.make} {c.model} ({c.year}) | VIN: {c.vin}")
    else:
        print("  (no cars)")
    print("Addresses:")
    if hasattr(user, 'addresses') and user.addresses:
        for a in user.addresses:
            parts = [a.street, a.city, a.state or None, a.country]
            pretty = ", ".join([p for p in parts if p])
            print(f"  - {pretty}")
    else:
        print("  (no addresses)")

def main():
    Base.metadata.create_all(engine)
    parser = argparse.ArgumentParser(description="SQLAlchemy ORM CLI")
    parser.add_argument("--seed", action="store_true", help="Seed database with Faker")
    parser.add_argument("--list", choices=["users", "cars", "addresses"], help="List entity")
    parser.add_argument("--print-assets", type=int, metavar="USER_ID", help="Print cars and addresses of a user")
    args = parser.parse_args()

    user_mgr = UserManager()
    car_mgr = CarManager()
    addr_mgr = AddressManager()

    if args.seed:
        seed_with_faker()

    if args.list == "users":
        for u in user_mgr.list_users():
            print(u)
    elif args.list == "cars":
        for c in car_mgr.list_cars():
            print(c)
    elif args.list == "addresses":
        for a in addr_mgr.list_addresses():
            print(a)

    if args.print_assets is not None:
        # Print assets using a session context
        with SessionLocal() as session:
            print_user_assets(session, args.print_assets)

if __name__ == "__main__":
    main()