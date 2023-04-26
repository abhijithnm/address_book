from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import SessionLocal, engine

# creating tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create-address/', status_code=status.HTTP_201_CREATED)
def create_address(payload: schemas.AddressBook, db: Session = Depends(get_db)):
    """This function is to create address with the payload"""

    address = db.query(models.AddressBook).filter(models.AddressBook.email == payload.email)
    db_address = address.first()
    # checking if the email is already added
    if db_address:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Address with this email_id: {payload.email} already exists')
    try:
        # saving to the table with given payload
        new_address = models.AddressBook(**payload.dict())
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        # returning response with new address created
        return {"status": "success", "address": new_address}
    except:
        return {"Unable to save to database...Try Again "}


@app.get('/get-address/',status_code=status.HTTP_200_OK)
def get_all_address(db: Session = Depends(get_db)):
    """This function will get all address"""

    address = db.query(models.AddressBook).all()
    return {'status': 'success', 'results': len(address), 'address': address}


@app.get('/get-address-by-id/{address_id}',status_code=status.HTTP_200_OK)
def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    """This function will get address by given id"""

    address = db.query(models.AddressBook).filter(models.AddressBook.id == address_id)
    db_address = address.first()

    # check if address with id exists else throw error
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No address found with the id: {address_id}')
    return {'status': 'success', 'address': db_address}


@app.put('/update-address/{address_id}')
def update_address(address_id: int, payload: schemas.AddressBook, db: Session = Depends(get_db)):
    """This function is to update address as per payload"""

    address_query = db.query(models.AddressBook).filter(models.AddressBook.id == address_id)
    db_address = address_query.first()

    # checking for address with id exists else throw error
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No address found with the id: {address_id}')
    try:
        update_data = payload.dict(exclude_unset=True)
        address_query.filter(models.AddressBook.id == address_id).update(update_data,
                                                        synchronize_session=False)
        db.commit()
        db.refresh(db_address)
        return {"status": "success", "address": db_address}
    except:
        return {"Unable to save to database...Try Again "}


@app.delete('/delete-address/{address_id}')
def delete_address(address_id: str, db: Session = Depends(get_db)):
    """This function is to delete address for the given id"""

    address_query = db.query(models.AddressBook).filter(models.AddressBook.id == address_id)
    address = address_query.first()

    # checking for address with id exists else through error
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No address found with the id: {address_id}')
    address_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/search-address/')
def search_address(db: Session = Depends(get_db), distance_in_km: float = None,
                   latitude: float = None, longitude: float = None):
    """This function is to search for address for the given criteria"""

    out_address = []

    # check for given latitude, longitude and distance and then find address near to that
    if longitude and latitude and distance_in_km:
        addresses = db.query(models.AddressBook).all()
        for address in addresses:
            if utils.find_distance(address.latitude, address.longitude, latitude, longitude) <= distance_in_km:
                out_address.append(address)
    
    # check for given latitude, longitude and then find address for the given location
    elif longitude and latitude:
        out_address = db.query(models.AddressBook).filter(
                             models.AddressBook.latitude == latitude,
                             models.AddressBook.longitude == longitude,
                             ).all()
    # check for distance and find address near to the current location
    elif distance_in_km:
        user_lat, user_long = utils.get_user_coordinates()
        addresses = db.query(models.AddressBook).all()
        for address in addresses:
            if utils.find_distance(address.latitude, address.longitude, user_lat, user_long) <= distance_in_km:
                out_address.append(address)
    return {'status': 'success', 'results': len(out_address), 'address': out_address}