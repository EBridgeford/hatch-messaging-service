from sqlalchemy.orm import Session

from app.schemas.users import User


def get_or_create_users_by_emails(db: Session, emails: list[str]) -> list[int]:
    # Get existing users
    existing_users = db.query(User).filter(User.email.in_(emails)).all()
    existing_emails = {user.email for user in existing_users}
    email_to_user_id = {user.email: user.id for user in existing_users}

    # Create missing users
    missing_emails = [email for email in emails if email not in existing_emails]
    created_emails = []

    for email in missing_emails:
        user = User(email=email)
        db.add(user)
        db.flush()  # Get ID without committing
        email_to_user_id[email] = user.id
        created_emails.append(email)

    db.commit()
    return list(email_to_user_id.values())


def get_or_create_users_by_phones(db: Session, phones: list[str]) -> list[int]:
    # Get existing users
    existing_users = db.query(User).filter(User.phone.in_(phones)).all()
    existing_phones = {user.phone for user in existing_users}
    phone_to_user_id = {user.phone: user.id for user in existing_users}

    # Create missing users
    missing_phones = [phone for phone in phones if phone not in existing_phones]
    created_phones = []

    for phone in missing_phones:
        user = User(phone=phone)
        db.add(user)
        db.flush()  # Get ID without committing
        phone_to_user_id[phone] = user.id
        created_phones.append(phone)

    db.commit()
    return list(phone_to_user_id.values())
