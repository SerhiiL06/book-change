from .models import UserFollowing


def is_object_owner(user_1, user_2):
    return user_1 == user_2


def is_following(user, follower):
    return UserFollowing.objects.filter(user_id=follower, followers_id=user).first()
