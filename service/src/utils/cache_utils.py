from delivery.models import Favorites
from delivery.serializers import FavoritesSerializer
from delivery.settings import CACHE_TIMEOUT
from django.core.cache import cache


def update_favorites_cache_for_user_example(user_id, invalidate=False):
    """Atualiza o cache de favoritos do usuário e retorna os dados serializados.

    Args:
        user_id (int): id do usuário (customer) cujo cache deve ser atualizado.

    Returns:
        list: lista serializada de favoritos ativos do usuário.

    example:
        cache_key = f"fakestore:all_products:{request.user.id}"
        data = cache.get(cache_key)
        if not data:
            data = update_favorites_cache_for_user_example(request.user.id)
    """
    cache_key = f"fakestore:all_products:{user_id}"

    if invalidate:
        cache.delete(cache_key)
        return []

    queryset = Favorites.objects.filter(customer_id=user_id, active=True).order_by(
        "-created_at"
    )
    data = FavoritesSerializer(queryset, many=True).data
    cache.set(cache_key, data, CACHE_TIMEOUT)
    return data
