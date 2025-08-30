from faker import Faker
import random
from managers import UserManager, AddressManager, CarManager
from models import Base
from config import engine, SessionLocal

def seed_with_faker(session, n_users=20, seed=123):
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)

    user_manager = UserManager(session)
    address_manager = AddressManager(session)
    car_manager = CarManager(session)

    from sqlalchemy.exc import IntegrityError

    car_data = {
        "Toyota": ["Corolla", "Camry", "Hilux", "RAV4", "Yaris", "Prado"],
        "Ford": ["Focus", "Fiesta", "Mustang", "Explorer", "F-150", "Escape"],
        "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Fit"],
        "Chevrolet": ["Impala", "Cruze", "Silverado", "Tahoe", "Aveo"],
        "BMW": ["X5", "X3", "Serie 3", "Serie 5", "Z4"],
        "Audi": ["A4", "A3", "Q5", "Q7", "TT"],
        "Nissan": ["Sentra", "Altima", "Versa", "Frontier", "X-Trail"],
        "Hyundai": ["Elantra", "Tucson", "Santa Fe", "Accent"],
        "Kia": ["Rio", "Sportage", "Sorento", "Optima"],
        "Mercedes-Benz": ["Clase C", "Clase E", "GLA", "GLE"]
    }

    for _ in range(n_users):
        name = fake.name()
        # Generate email based on name
        name_parts = name.lower().replace("'", "").split()
        if len(name_parts) >= 2:
            email_base = f"{name_parts[0]}.{name_parts[-1]}"
        else:
            email_base = name_parts[0]
        # Add a random number to ensure uniqueness
        email = f"{email_base}{random.randint(1,9999)}@example.com"
        try:
            user = user_manager.create_user(name=name, email=email)
        except IntegrityError:
            session.rollback()
            continue

        # Create 1-3 addresses per user
        for _ in range(random.randint(1, 3)):
            street = fake.street_address()
            city = fake.city()
            state = fake.state()
            zip_code = fake.zipcode()
            address_manager.create_address(
                street=street,
                city=city,
                state=state,
                zip_code=zip_code,
                user_id=user.id
            )

        # Create 1-2 cars per user
        for _ in range(random.randint(1, 2)):
            while True:
                make = random.choice(list(car_data.keys()))
                model = random.choice(car_data[make])
                year = random.randint(1995, 2023)
                license_plate = fake.license_plate()
                try:
                    car_manager.create_car(
                        make=make,
                        model=model,
                        year=year,
                        license_plate=license_plate,
                        owner_id=user.id
                    )
                    break
                except IntegrityError:
                    session.rollback()
                    continue

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        seed_with_faker(session)