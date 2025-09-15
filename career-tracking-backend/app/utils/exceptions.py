from fastapi import HTTPException, status


class CareerTrackingException(Exception):
    """Base exception for Career Tracking application"""
    pass


class UserNotFoundException(CareerTrackingException):
    """Raised when user is not found"""
    pass


class InvalidCredentialsException(CareerTrackingException):
    """Raised when authentication credentials are invalid"""
    pass


class DuplicateEmailException(CareerTrackingException):
    """Raised when trying to register with an existing email"""
    pass


class AptitudeTestNotFoundException(CareerTrackingException):
    """Raised when aptitude test is not found"""
    pass


class CollegeNotFoundException(CareerTrackingException):
    """Raised when college is not found"""
    pass


def create_http_exception(status_code: int, detail: str) -> HTTPException:
    """Helper function to create HTTP exceptions"""
    return HTTPException(status_code=status_code, detail=detail)