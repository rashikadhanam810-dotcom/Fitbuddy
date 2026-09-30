from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    user_id = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    weight = Column(String(20))
    goal = Column(String(100))
    intensity = Column(String(50))

    original_plan = Column(Text)
    updated_plan = Column(Text, nullable=True)

    nutrition_tip = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


# --------------------------------
# SAVE OR UPDATE USER
# --------------------------------
def save_user(username, user_id, age, weight, goal, intensity):

    db = SessionLocal()

    # Check whether the user already exists
    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:

        # Update existing user
        user.username = username
        user.age = age
        user.weight = str(weight)
        user.goal = goal
        user.intensity = intensity

        db.commit()
        db.refresh(user)
        db.close()

        return user

    # Create new user
    user = User(
        username=username,
        user_id=user_id,
        age=age,
        weight=str(weight),
        goal=goal,
        intensity=intensity
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return user


# --------------------------------
# SAVE WORKOUT PLAN
# --------------------------------
def save_plan(user_id, workout_plan, nutrition_tip):

    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:
        user.original_plan = workout_plan
        user.nutrition_tip = nutrition_tip
        db.commit()

    db.close()


# --------------------------------
# UPDATE WORKOUT PLAN
# --------------------------------
def update_plan(user_id, updated_plan):

    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:
        user.updated_plan = updated_plan
        db.commit()

    db.close()


# --------------------------------
# GET ONE USER
# --------------------------------
def get_user(user_id):

    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    db.close()

    return user


# --------------------------------
# GET ALL USERS
# --------------------------------
def get_all_users():

    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users


# --------------------------------
# DELETE USER
# --------------------------------
def delete_user(user_id):

    db = SessionLocal()

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:
        db.delete(user)
        db.commit()

    db.close()