from django.conf import settings
from django.core.mail import send_mail
from django_elasticsearch_dsl.search import Search


# def animal_search(query):
#         s = Search(index='animals_index')
#         s = s.query("multi_match", query=query, fields=["name", "content", "species"])

#         response = s.execute()

#         # Обработка результатов
#         animals = [{'name': hit.name, 'content': hit.content, "species": hit.species} for hit in response.hits]

#         return animals


# EMAIL
def send_form_email(user_email):
    subjects = f"Анкета создана, {user_email}! Скоро вам позвонит специалист "
    message = f"Поздравляем вас!"
    send_mail(
        subject=subjects,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
