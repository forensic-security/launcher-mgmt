from ._router import crud_router
from ..models.crm import Customer, CreateCustomer, UpdateCustomer


customer = crud_router(Customer, CreateCustomer, UpdateCustomer, delete=False)


@customer.get('/{customer_id}/installer')
async def get_customer_installer(customer_id: int):
    '''Returns the Launcher installer for a specific customer.
    '''
    raise NotImplementedError


@customer.get('/{customer_id}/devices')
async def get_customer_devices(customer_id: int):
    '''Returns the customer's devices.
    '''
    raise NotImplementedError


# @customer.get('/{customer_id}/applications')
# async def get_customer_applications(customer_id: int):
#     '''Returns the number of licenses per application for a specific
#     customer.
#     '''
#     raise NotImplementedError


# @customer.put('/{customer_id}/applications')
# async def set_customer_applications(customer_id: int):
#     '''Set the number of licenses per application for a specific
#     customer.
#     '''
#     raise NotImplementedError
