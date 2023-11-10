def animal_search(query):
    from animals.models import Animal

    Animal.objects.filter(name__icontains=query)
