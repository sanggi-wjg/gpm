import aiohttp
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.core.config import get_config_settings
from app.exceptions.user_exception import BadCredentials
from app.schemas.auth_schema import GithubToken

settings = get_config_settings()


class GitHubAPI:
    url_post_access_token = "https://github.com/login/oauth/access_token"
    url_get_user_info = "https://api.github.com/user"

    async def request_access_token(self, code: str, state: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self.url_post_access_token,
                    data=jsonable_encoder({
                        'client_id': settings.github_client_id,
                        'client_secret': settings.github_secret,
                        'code': code,
                    }),
                    headers={"Accept": "application/json"}) as response:
                if response.status != status.HTTP_200_OK:
                    raise BadCredentials()

                return GithubToken(**await response.json(), state=state)

    async def request_user_info(self, github_token: GithubToken):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.url_get_user_info,
                    headers={
                        'Accept': 'application/vnd.github+json',
                        'Authorization': f"{github_token.token_type} {github_token.access_token}"
                    }) as response:
                if response.status != status.HTTP_200_OK:
                    raise BadCredentials()

                return await response.json()
