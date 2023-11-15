def animal_search(query):
    from animals.models import Animals

    Animals.objects.filter(name__icontains=query)
