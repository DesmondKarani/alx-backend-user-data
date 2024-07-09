#!/usr/bin/env python3
"""
This module contains the BasicAuth class for handling basic
authentication in the API.
It includes methods for extracting and decoding Base64 authorization headers,
as well as verifying user credentials.
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class to manage API authentication using
    Basic Authentication.

    This class provides methods to handle Base64 encoding/decoding of
    authorization headers, extracting user credentials, and verifying
    those credentials against stored user data.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """
        Extracts the Base64 part of the Authorization header for
        Basic Authentication.

        Args:
            authorization_header (str): The full authorization
            header string.

        Returns:
            str: The Base64 encoded part of the header,
            or None if the header is invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """
        Decodes the Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded
            authorization header.

        Returns:
            str: The decoded header as a UTF-8 string,
            or None if decoding fails.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """
        Extracts user credentials from the decoded Base64 authorization
        header.

        Args:
            decoded_base64_authorization_header (str):
            The decoded Base64 header.

        Returns:
            Tuple[str, str]: A tuple containing the email and password,
            or (None, None) if extraction fails.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        Returns the User instance based on email and password.

        This method searches for a user by email and verifies the password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if authentication is successful,
            or None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.

        This method extracts the authorization header from the request,
        decodes it, extracts the user credentials,
        and returns the corresponding User object.

        Args:
            request: The request object containing the authorization header.

        Returns:
            User: The User instance if authentication is successful,
            or None otherwise.
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        user_credentials = self.extract_user_credentials(decoded_auth)
        if user_credentials is None:
            return None

        user_email, user_pwd = user_credentials
        return self.user_object_from_credentials(user_email, user_pwd)

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """
        Extracts user credentials from the decoded Base64 authorization header
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        # Split at the first occurrence of ':'
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)
