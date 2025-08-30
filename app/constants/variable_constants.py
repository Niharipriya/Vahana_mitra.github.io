"""
    This module stores all constant field names used across the project.  
    Keeping them in one place ensures consistency and reduces the risk of typos. 
"""

class User_conts:
    ID: str = 'user_id'
    FULLNAME: str = 'user_fullname'
    PHONE: str = 'user_phone'
    EMAIL: str = 'user_email'
    PASSWORD: str = 'user_password'

    CREATED_TIME: str = 'user_created_time'
    UPDATED_TIME: str = 'user_updated_time'
    STATUS: str = 'user_status'

class Truck_conts:
    """ 
        Constants for truck-related fields.
        Covers details about the truck, its owner, and driver.
    """
    ID: str = 'truck_id'
    CURRENT_LOCATION: str = 'truck_current_location'
    
    # Vehicle Information
    VEHICLE_REGISTRATION_NUMBER: str = 'vehicle_registration_number'
    VEHICLE_MODEL_NAME: str = 'vehicle_model_name'
    VEHICLE_TYPE: str = 'vehicle_type'
    VEHICLE_CAPACITY: str = 'vehicle_capacity'
    VEHICLE_INSURANCE: str = 'vheicle_insurance' 
    VEHICLE_PERMIT: str = 'vehical_permit'

    # Truck Owner Information
    OWNER_NAME: str = 'truck_owner_name'
    OWNER_PHONE: str = 'truck_owner_phone'
    OWNER_AADHAAR: str = 'truck_owner_aadhaar'
    OWNER_PAN: str = 'truck_owner_pan'

    # Truck Driver Information
    DRIVER_NAME: str = 'truck_driver_name'
    DRIVER_PHONE: str = 'truck_driver_phone'
    DRIVER_AADHAAR: str = 'truck_driver_aadhar'
    DRIVER_LICENSE: str = 'truck_driver_license'

class Load_conts:
    """
        Constants for load/shipment-related fields.
        Includes pickup, drop, and cargo details.
    """
    ID: str = 'load_id'
    CURRENT_LOCATION: str = 'load_current_location'
    
    #pickup details
    PICKUP_LOCATION: str = 'pickup_location'
    PICKUP_DATETIME: str = 'pickup_datetime'
    PICKUP_CONTACT_NAME: str = 'pickup_contact_name' 
    PICKUP_CONTACT_PHONE: str = 'pickup_contact_phone'

    #drop details
    DROP_LOCATION: str = 'drop_location'
    DROP_DATETIME: str = 'drop_datetime'
    DROP_CONTACT_NAME: str = 'drop_contact_name'
    DROP_CONTACT_PHONE: str = 'drop_contact_phone'

    #load details
    LOAD_WEIGHT: str = 'load_weight'
    LOAD_TYPE: str = 'load_type'
    LOAD_DETAILS: str = 'load_details'

    CREATED_TIME: str = 'load_created_time'
    UPDATED_TIME: str = 'load_updated_time'