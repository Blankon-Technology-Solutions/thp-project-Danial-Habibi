from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

class TokenAuthBackend:
    async def authenticate(self, request, token=None):
        if token:
            User = get_user_model()
            user = await sync_to_async(User.objects.get)(auth_token=token)
            return user if user else None
        return None
