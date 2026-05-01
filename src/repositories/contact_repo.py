# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.contact import Contact
from src.models.user import User
from sqlalchemy import select


async def get_all_contacts(
    user: User,
    session: AsyncSession,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None
    
) -> list[Contact]:
    # query = session.query(Contact)
    stmt= select(Contact).filter(Contact.user_id == user.id)

    if first_name:
        stmt = stmt.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        stmt = stmt.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))

    result = await session.execute(stmt)
    return result.scalars().all()
async def create_contact(session: AsyncSession, contact: Contact, user: User) -> Contact:
    new_contact = Contact(**contact.model_dump(), user_id=user.id)
    session.add(new_contact)
    await session.commit()
    await session.refresh(new_contact)
    print(f"Created contact: {new_contact}")
    return new_contact


async def get_contact_by_id(session: AsyncSession, contact_id: int, user: User) -> Contact | None:
    print(f"Getting contact by id8787878787787878: {contact_id} for user: {user.id}")
    stmt = select(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_contact_by_email(session: AsyncSession, email: str, user: User) -> Contact | None:
    stmt = select(Contact).filter(Contact.email == email, Contact.user_id == user.id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def update_contact(session: AsyncSession, db_contact: Contact, user: User) -> Contact:
    if db_contact.user_id != user.id:
        return None
    session.add(db_contact)
    await session.commit()
    await session.refresh(db_contact)
    return db_contact


async def delete_contact(session: AsyncSession, db_contact_id: int, user: User) -> None:
    db_contact = await get_contact_by_id(session, db_contact_id, user)
    print(f"Deleting contact1111111111111111111111: {db_contact}")
    if db_contact and db_contact.user_id == user.id:
        await session.delete(db_contact)
        await session.commit()