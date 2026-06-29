import re
from typing import Any, Dict, List

import requests


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def login(self, email: str, password: str) -> str:
        """
        Logs in via API POST /api/login and returns the JWT token.
        """
        url = f"{self.base_url}/api/login"
        payload = {"email": email, "password": password}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["jwt"]

    def get_session_cookies(self, email: str, password: str) -> List[Dict[str, Any]]:
        """
        Logs in via Devise HTML POST /users/sign_in to obtain session cookies
        which can be injected into the browser context.
        """
        sign_in_url = f"{self.base_url}/users/sign_in"
        r_get = self.session.get(sign_in_url)
        r_get.raise_for_status()

        # Extract CSRF token
        match = re.search(r'name="authenticity_token"\s+value="([^"]+)"', r_get.text)
        if not match:
            match = re.search(r'value="([^"]+)"\s+name="authenticity_token"', r_get.text)
        csrf_token = match.group(1) if match else None

        if not csrf_token:
            match_meta = re.search(r'name="csrf-token"\s+content="([^"]+)"', r_get.text)
            csrf_token = match_meta.group(1) if match_meta else None

        if not csrf_token:
            raise ValueError("Could not find authenticity token (CSRF token) on sign_in page")

        # POST /users/sign_in
        payload = {
            "authenticity_token": csrf_token,
            "user[email]": email,
            "user[password]": password,
            "user[remember_me]": "1",
            "commit": "Sign in",
        }
        r_post = self.session.post(sign_in_url, data=payload, allow_redirects=False)
        r_post.raise_for_status()

        # Format cookies for Playwright
        cookies = []
        for cookie in self.session.cookies:
            domain = cookie.domain if cookie.domain else "app.testomat.io"

            # Determine HttpOnly using public methods or dynamic lookup to avoid IDE warnings
            is_httponly = False
            if cookie.has_nonstandard_attr("HttpOnly") or cookie.has_nonstandard_attr("httponly"):
                is_httponly = True
            else:
                rest = getattr(cookie, "_rest", {})
                for k in rest.keys():
                    if k.lower() == "httponly":
                        is_httponly = True
                        break

            cookies.append(
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": domain,
                    "path": cookie.path if cookie.path else "/",
                    "httpOnly": is_httponly,
                    "secure": cookie.secure,
                }
            )

        return cookies
