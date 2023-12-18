def animal_search(query):
    from animals.models import Animals

    animals = Animals.objects.filter(name__icontains=query)
    return animals