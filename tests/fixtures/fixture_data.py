import pytest

# from src.config import settings
from src.events.models import Event


@pytest.fixture
def event_1():
    """Тестовые данные для мероприятия 1."""
    return Event.objects.create(
        name="Название 1",
        description="description_1",
        # members='',
        event_type="event_type_1",
        event_price=100,
        # start_date='',
        # end_date='',
        city="Москва",
        # image='',
        min_age=10,
        max_age=20,
        min_count_members=5,
        max_count_members=10,
    )


# @pytest.fixture
# def event_2():
#     return Event.objects.create(title='Группа 2', slug='group_2')


# @pytest.fixture
# def post(user, group_1):
#     return Post.objects.create(
#         text='Тестовый пост 1', author=user, group=group_1
#     )


# @pytest.fixture
# def post_2(user, group_1):
#     return Post.objects.create(
#         text='Тестовый пост 12342341', author=user, group=group_1
#     )


# @pytest.fixture
# def comment_1_post(post, user):
#     return Comment.objects.create(author=user, post=post, text='Коммент 1')


# @pytest.fixture
# def comment_2_post(post, another_user):
#     return Comment.objects.create(
#         author=another_user, post=post, text='Коммент 2'
#     )


# @pytest.fixture
# def another_post(another_user, group_2):
#     return Post.objects.create(
#         text='Тестовый пост 2', author=another_user, group=group_2
#     )


# @pytest.fixture
# def comment_1_another_post(another_post, user):
#     return Comment.objects.create(
#         author=user, post=another_post, text='Коммент 12'
#     )


# @pytest.fixture
# def follow_1(user, another_user):
#     return Follow.objects.create(user=user, following=another_user)


# @pytest.fixture
# def follow_2(user_2, user):
#     return Follow.objects.create(user=user_2, following=user)


# @pytest.fixture
# def follow_3(user_2, another_user):
#     return Follow.objects.create(user=user_2, following=another_user)


# @pytest.fixture
# def follow_4(another_user, user):
#     return Follow.objects.create(user=another_user, following=user)


# @pytest.fixture
# def follow_5(user_2, user):
#     return Follow.objects.create(user=user, following=user_2)
