#!/usr/bin/env python3
"""
Authentication module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            path (str): Url path to be checked
            excluded_paths (List[str]): List of paths that don't
            need authentication
        Returns:
            True if authentication is required, False otherwise
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with '/' for consistent comparison
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            # Ensure excluded_path ends with '/' and has a wildcard
            excluded_path = excluded_path.rstrip('/') + '/*'
            if path.startswith(excluded_path[:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header from a request object
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object
        """
        return None
