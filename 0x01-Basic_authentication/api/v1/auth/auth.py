#!/usr/bin/env python3
"""
Authentication module for the API
This module provides the base Auth class for handling API authentication.
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """
    Auth class to manage API authentication
    This class provides methods to handle authentication requirements,
    process authorization headers, and manage user authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            path (str): Url path to be checked
            excluded_paths (List[str]): List of paths that
            don't need authentication
        Returns:
            True if authentication is required, False otherwise
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with '/' for consistent comparison
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            # Remove trailing slash if present
            excluded_path = excluded_path.rstrip('/')

            # If excluded_path ends with *, it's a wildcard pattern
            if excluded_path.endswith('*'):
                pattern = '^' + excluded_path[:-1] + '.*$'
                if re.match(pattern, path):
                    return False
            elif path == excluded_path + '/':
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from a request object

        Args:
            request: Flask request object

        Returns:
            str: The value of the Authorization header if present,
            None otherwise

        This method extracts the Authorization header from
        the given request object.
        If the request is None or the header is not present, it returns None.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current authenticated User based on the request

        Args:
            request: Flask request object

        Returns:
            TypeVar('User'): The authenticated User instance or None

        This method is meant to be overridden by authentication-specific
        subclasses.
        In its base form, it always returns None.
        """
        return None
