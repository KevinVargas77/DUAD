from models import User, Address, Car
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError, NoResultFound
from config import SessionLocal

class UserManager:
    model_class = User

    def create_user(self, name: str, email: str) -> User:
        with SessionLocal() as session:
            user = User(name=name, email=email)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def update_user(self, user_id: int, **fields) -> User:
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if not user:
                raise NoResultFound(f"User with id={user_id} not found")
            for k, v in fields.items():
                if hasattr(user, k) and k not in {"id", "created_at"}:
                    setattr(user, k, v)
            session.commit()
            session.refresh(user)
            return user

    def delete_user(self, user_id: int) -> None:
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if not user:
                raise NoResultFound(f"User with id={user_id} not found")
            session.delete(user)
            session.commit()

    def list_users(self) -> list[User]:
        with SessionLocal() as session:
            return list(session.scalars(select(User).order_by(User.id)))

    def get_users_with_more_than_one_car(self) -> list[User]:
        with SessionLocal() as session:
            stmt = (
                select(User)
                .join(User.cars)
                .group_by(User.id)
                .having(func.count(Car.id) > 1)
                .order_by(User.id)
            )
            return list(session.scalars(stmt))

class CarManager:
    model_class = Car

    def create_car(self, make: str, model: str, year: int, license_plate: str, owner_id: int) -> Car:
        with SessionLocal() as session:
            car = Car(make=make, model=model, year=year, license_plate=license_plate, owner_id=owner_id)
            session.add(car)
            session.commit()
            session.refresh(car)
            return car

    def update_car(self, car_id: int, **fields) -> Car:
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if not car:
                raise NoResultFound(f"Car with id={car_id} not found")
            for k, v in fields.items():
                if hasattr(car, k) and k not in {"id", "created_at"}:
                    setattr(car, k, v)
            session.commit()
            session.refresh(car)
            return car

    def delete_car(self, car_id: int) -> None:
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if not car:
                raise NoResultFound(f"Car with id={car_id} not found")
            session.delete(car)
            session.commit()

    def list_cars(self) -> list[Car]:
        with SessionLocal() as session:
            return list(session.scalars(select(Car).order_by(Car.id)))

    def assign_car_to_user(self, car_id: int, user_id: int) -> Car:
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if not car:
                raise NoResultFound(f"Car with id={car_id} not found")
            user = session.get(User, user_id)
            if not user:
                raise NoResultFound(f"User with id={user_id} not found")
            car.user = user
            session.commit()
            session.refresh(car)
            return car

    def get_cars_without_user(self) -> list[Car]:
        with SessionLocal() as session:
            stmt = select(Car).where(Car.user_id.is_(None)).order_by(Car.id)
            return list(session.scalars(stmt))

class AddressManager:
    model_class = Address

    def create_address(self, user_id: int, street: str, city: str, state: str = None, zip_code: str = None) -> Address:
        with SessionLocal() as session:
            if not session.get(User, user_id):
                raise NoResultFound(f"User with id={user_id} not found")
            address = Address(user_id=user_id, street=street, city=city, state=state, zip_code=zip_code)
            session.add(address)
            session.commit()
            session.refresh(address)
            return address

    def update_address(self, address_id: int, **fields) -> Address:
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if not address:
                raise NoResultFound(f"Address with id={address_id} not found")
            for k, v in fields.items():
                if hasattr(address, k) and k not in {"id", "user_id", "created_at"}:
                    setattr(address, k, v)
            session.commit()
            session.refresh(address)
            return address

    def delete_address(self, address_id: int) -> None:
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if not address:
                raise NoResultFound(f"Address with id={address_id} not found")
            session.delete(address)
            session.commit()

    def list_addresses(self) -> list[Address]:
        with SessionLocal() as session:
            return list(session.scalars(select(Address).order_by(Address.id)))

    def search_addresses_by_substring(self, text: str) -> list[Address]:
        with SessionLocal() as session:
            pattern = f"%{text}%"
            stmt = select(Address).where(func.lower(Address.street).like(func.lower(pattern))).order_by(Address.id)
            return list(session.scalars(stmt))