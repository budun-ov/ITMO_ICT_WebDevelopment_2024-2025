from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Race, Racer, Comment, Result, RaceRegistration
from .forms import UserRegistrationForm, RacerProfileForm

def home(request):
    return render(request, 'races/home.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = RacerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Registration successful!')
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Registration failed. Check your inputs.')
    else:
        user_form = UserRegistrationForm()
        profile_form = RacerProfileForm()
    return render(request, 'races/register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_profile(request):
    racer = get_object_or_404(Racer, user=request.user)

    # Получаем предстоящие и прошедшие гонки для текущего профиля
    upcoming_races = racer.registered_races.filter(is_completed=False)
    past_races = racer.registered_races.filter(is_completed=True)

    return render(request, 'races/profile.html', {
        'racer': racer,
        'upcoming_races': upcoming_races,
        'past_races': past_races,
    })


@login_required
def edit_profile(request):
    racer = get_object_or_404(Racer, user=request.user)

    if request.method == 'POST':
        form = RacerProfileForm(request.POST, request.FILES, instance=racer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = RacerProfileForm(instance=racer)

    return render(request, 'races/edit_profile.html', {'form': form})

def other_profile(request, racer_id):
    racer = get_object_or_404(Racer, pk=racer_id)
    return render(request, 'races/other_profile.html', {'racer': racer})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'races/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    racer = get_object_or_404(Racer, user=request.user)

    # Проверка возраста
    user_age = (datetime.now().date() - racer.birth_date).days // 365
    if user_age < race.age_limit:
        messages.error(request, f"You must be at least {race.age_limit} years old to register.")
        return redirect('race_detail', race_id=race.id)

    # Проверка класса гонки
    if racer.class_type != race.race_class:
        messages.error(request, f"This race is for {race.get_race_class_display()} class only.")
        return redirect('race_detail', race_id=race.id)

    # Проверка на повторную регистрацию
    if RaceRegistration.objects.filter(race=race, racer=racer).exists():
        messages.error(request, "You are already registered for this race.")
        return redirect('race_detail', race_id=race.id)

    # Регистрация гонщика на гонку
    RaceRegistration.objects.create(race=race, racer=racer)

    # Также добавляем гонщика в ManyToManyField
    race.registered_racers.add(racer)

    messages.success(request, f"You have successfully registered for {race.name}!")
    return redirect('race_detail', race_id=race.id)

@login_required
def cancel_register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    racer = get_object_or_404(Racer, user=request.user)

    # Проверка на наличие регистрации
    registration = RaceRegistration.objects.filter(race=race, racer=racer).first()
    if not registration:
        messages.error(request, "You are not registered for this race.")
        return redirect('race_detail', race_id=race.id)

    # Удаление записи о регистрации
    registration.delete()

    # Удаление гонщика из ManyToManyField
    race.registered_racers.remove(racer)

    messages.success(request, f"You have successfully canceled your registration for {race.name}.")

    # Перенаправление на предыдущую страницу или страницу гонки, если HTTP_REFERER не существует
    referer_url = request.META.get('HTTP_REFERER', None)
    if referer_url:
        return redirect(referer_url)
    else:
        return redirect('race_detail', race_id=race.id)



def race_list(request, race_type):
    if race_type == 'upcoming':
        races = Race.objects.filter(date__gte=datetime.now()).order_by('date')
    elif race_type == 'past':
        races = Race.objects.filter(date__lt=datetime.now()).order_by('-date')
    else:
        races = Race.objects.none()  # Если тип гонки не распознан

    paginator = Paginator(races, 10)  # 10 гонок на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'races/race_list.html', {'page_obj': page_obj, 'race_type': race_type})

def race_detail(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    questions = Comment.objects.filter(race=race, comment_type='question').order_by('-created_at')
    reviews = Comment.objects.filter(race=race, comment_type='review').order_by('-created_at')
    collaboration = Comment.objects.filter(race=race, comment_type='collaboration').order_by('-created_at')

    # Получаем результаты гонки, отсортированные по времени
    results = Result.objects.filter(race=race).order_by('result_time')

    # Средний рейтинг
    average_rating = 0
    if reviews.exists():
        total_rating = sum([review.rating for review in reviews])
        average_rating = total_rating / reviews.count()
    else:
        average_rating = None

    # Проверка, зарегистрирован ли гонщик на гонку
    is_registered = race.registered_racers.filter(id=request.user.racer.id).exists()

    return render(request, 'races/race_detail.html', {
        'user': request.user,
        'is_registered': is_registered,
        'race': race,
        'results': results,
        'questions': questions,
        'reviews': reviews,
        'collaboration': collaboration,
        'average_rating': average_rating,
    })


@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, pk=race_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        comment_type = request.POST.get('comment_type')

        # Проверка на корректность текста комментария
        if not content or content.strip() == "":
            messages.error(request, "Comment text cannot be empty.")
            return redirect('race_detail', race_id=race.id)

        # Проверка на корректность типа комментария
        valid_comment_types = ['question', 'review', 'collaboration']
        if comment_type not in valid_comment_types:
            messages.error(request, "Invalid comment type.")
            return redirect('race_detail', race_id=race.id)

        # Обработка типов комментариев
        if comment_type == 'question':
            # Создаем вопрос
            Comment.objects.create(
                commenter=request.user,
                race=race,
                content=content,
                comment_type='question'
            )
        elif comment_type == 'review':
            # Проверяем, завершена ли гонка
            if not race.is_completed:
                messages.error(request, "You can only leave a review for completed races.")
                return redirect('race_detail', race_id=race.id)

            # Проверяем, участвовал ли пользователь в гонке
            racer_results = Result.objects.filter(race=race, racer__user=request.user)
            if not racer_results.exists():
                messages.error(request, "You can only leave a review if you participated in this race.")
                return redirect('race_detail', race_id=race.id)

            # Проверяем, оставлял ли пользователь уже review
            existing_review = Comment.objects.filter(
                commenter=request.user,
                race=race,
                comment_type='review'
            )
            if existing_review.exists():
                messages.error(request, "You have already left a review for this race.")
                return redirect('race_detail', race_id=race.id)

            # Проверка рейтинга
            rating = request.POST.get('rating')
            try:
                rating = int(rating)
                if rating < 1 or rating > 10:
                    raise ValueError
            except (TypeError, ValueError):
                messages.error(request, "Rating must be a number between 1 and 10.")
                return redirect('race_detail', race_id=race.id)

            # Создаем отзыв
            Comment.objects.create(
                commenter=request.user,
                race=race,
                content=content,
                rating=rating,
                comment_type='review'
            )
        elif comment_type == 'collaboration':
            # Создаем запрос на сотрудничество
            Comment.objects.create(
                commenter=request.user,
                race=race,
                content=content,
                comment_type='collaboration'
            )

        messages.success(request, "Your comment has been added!")
        return redirect('race_detail', race_id=race.id)

    # Если запрос не POST, перенаправляем на домашнюю страницу
    return redirect('home')

