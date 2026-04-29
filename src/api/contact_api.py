from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.schemas.contact import ContactResponse, ContactRequest, ContactUpdateRequest
from src.db.session import open_session
from src.services import contact_service

router = APIRouter()


# Get all or search contacts from db
@router.get("/contacts/", response_model=list[ContactResponse])
def get_all_or_search_contacts(
    first_name: str | None = Query(default=None),
    last_name: str | None = Query(default=None),
    email: str | None = Query(default=None),
    session: Session = Depends(open_session),
):
    contacts = contact_service.get_all_contacts(session, first_name, last_name, email)
    return [ContactResponse.model_validate(c) for c in contacts]


# Create new contact
@router.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactRequest, session: Session = Depends(open_session)):
    new_contact = contact_service.create_contact(session, contact)
    return ContactResponse.model_validate(new_contact)


# Get upcoming birthdays
@router.get("/contacts/birthdays/upcoming", response_model=list[ContactResponse])
def get_upcoming_birthdays(session: Session = Depends(open_session)):
    contacts = contact_service.get_upcoming_birthdays(session)
    return [ContactResponse.model_validate(c) for c in contacts]


# Get contact by id
@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact_by_id(contact_id: int, session: Session = Depends(open_session)):
    contact = contact_service.get_contact_by_id(session, contact_id)
    return ContactResponse.model_validate(contact)


@router.patch("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact: ContactUpdateRequest,
    session: Session = Depends(open_session),
):
    db_contact = contact_service.get_contact_by_id(session, contact_id)
    updated_contact = contact_service.update_contact(session, db_contact, contact)
    return ContactResponse.model_validate(updated_contact)


@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, session: Session = Depends(open_session)):
    db_contact = contact_service.get_contact_by_id(session, contact_id)
    contact_service.delete_contact(session, db_contact)
    return {"message": f'Contact with id "{contact_id}" deleted successfully'}
