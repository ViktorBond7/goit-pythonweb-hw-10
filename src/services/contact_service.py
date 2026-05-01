# from sqlalchemy.orm import Session
from src.models.contact import Contact
from src.repositories import contact_repo
from fastapi import HTTPException, status
from src.schemas.contact import ContactRequest, ContactUpdateRequest
from datetime import date, timedelta
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_contacts(
    user: User,
    session: AsyncSession,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    
) -> list[Contact]:
    return await contact_repo.get_all_contacts(user, session, first_name, last_name, email)


async def get_upcoming_birthdays(session: AsyncSession, days: int = 7, user: User = None) -> list[Contact]:
    today = date.today()
    end_date = today + timedelta(days=days)
    contacts = await contact_repo.get_all_contacts(user, session)

    upcoming_contacts: list[Contact] = []
    for contact in contacts:
        next_birthday = contact.birthday.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        if today <= next_birthday <= end_date:
            upcoming_contacts.append(contact)

    return upcoming_contacts


async def create_contact(session: AsyncSession, contact: ContactRequest, user: User) -> Contact:
    db_contact = await contact_repo.get_contact_by_email(session, contact.email, user)
    if db_contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contact with email {contact.email} already exists.",
        )
    
    return await contact_repo.create_contact(session, contact, user)


async def get_contact_by_id(session: AsyncSession, contact_id: int, user: User) -> Contact | None:
    db_contact = await contact_repo.get_contact_by_id(session, contact_id, user)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return db_contact


async def update_contact(
    session: AsyncSession, db_contact: Contact, contact: ContactUpdateRequest, user: User
) -> Contact:
    update_data = contact.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != db_contact.email and db_contact.user_id == user.id:
        existing_contact = await contact_repo.get_contact_by_email(
            session, update_data["email"], user
        )
        if existing_contact and existing_contact.id != db_contact.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contact with email {update_data['email']} already exists.",
            )

    for field, value in update_data.items():
        setattr(db_contact, field, value)

    return await contact_repo.update_contact(session, db_contact, user)


async def delete_contact(session: AsyncSession, db_contact_id: int, user: User) -> None:
    
    db_contact = await contact_repo.get_contact_by_id(session, db_contact_id, user)
   
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    await contact_repo.delete_contact(session, db_contact_id, user)
