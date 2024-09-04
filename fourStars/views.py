from django.shortcuts import render, redirect
from django.db.models import Count, Prefetch, Q
from .models import Professor, Rating
from django.views.decorators.cache import cache_page
from .forms import UserRegistrationForm
from django.contrib.auth import login

@cache_page(60 * 15)
def home(request):
    return render(request, 'fourStars/home.html')

@cache_page(60 * 15)
def about(request):
    return render(request, 'fourStars/about.html')


def professors(request):
    search_query = request.GET.get('search', '')
    # Prefetch related ratings and courses to avoid multiple queries in the template
    professors = Professor.objects.prefetch_related('ratings', 'courses').all()
    
    if search_query:
        professors = professors.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(courses__name__icontains=search_query)
        ).distinct()
    
    professors_with_data = []
    for professor in professors:
        professors_with_data.append({
            'professor': professor,
            'average_rating': professor.average_rating,
            'ratings_count': professor.ratings.count(),
            'courses': professor.courses.all(),
        })

    return render(request, 'fourStars/professors.html', {'professors': professors_with_data, 'search_query': search_query})



 
def professor_view(request, professor_id=None):
    # Fetch professor with related courses and ratings in a single query
    professor = Professor.objects.prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.select_related('student')),
        'courses'
    ).get(id=professor_id)


    rating_distribution = (
        professor.ratings.values('rating')
        .annotate(count=Count('rating'))
        .order_by('-rating')
    )
    total_ratings = sum(item['count'] for item in rating_distribution) or 1

    # Calculate the distribution and percentage of each rating
    ratings_distribution = [
        {
            'stars': i,
            'percentage': next(
                (
                    (item['count'] / total_ratings) * 100
                    for item in rating_distribution
                    if item['rating'] == i
                ),
                0,
            ),
            'count': next(
                (item['count'] for item in rating_distribution if item['rating'] == i),
                0,
            ),
        }
        for i in range(5, 0, -1)
    ]


    # Ratings are already prefetched, so no additional queries needed
    ratings = professor.ratings.all()
    ratings_count = len(ratings)

    # Prepare the context with prefetched courses
    context = {
        'professor': professor,
        'ratings_distribution': ratings_distribution,
        'ratings': ratings,
        'ratings_count': ratings_count,
        'courses': professor.courses.all(),
    }

    return render(request, 'fourStars/professorView.html', context)

def signupScreen(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Opcional: Iniciar sesión automáticamente al registrarse
            return redirect('')  # Redirigir a una página de éxito o inicio
    else:
        form = UserRegistrationForm()

    return render(request, 'fourStars/signupScreen.html', {'form': form})