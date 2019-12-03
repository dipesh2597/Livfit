from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . forms import CaloriesCalculatorForm, IngredientForm, MealForm
from django.contrib import messages
from Users.models import Profile
from . models import Dietplan, Meal, Ingredient

# Create your views here.
@login_required
def caloriescalculator(request):
    if request.method == 'POST':
        c_form = CaloriesCalculatorForm(request.POST, instance=request.user.profile)
        if c_form.is_valid():
            gender = c_form.cleaned_data.get('gender')
            age = c_form.cleaned_data.get('age')
            height = c_form.cleaned_data.get('height')
            weight = c_form.cleaned_data.get('weight')
            job = c_form.cleaned_data.get('job')
            goal_weight = c_form.cleaned_data.get('goal_weight')
            goal_time_period = c_form.cleaned_data.get('goal_time_period')
            c_form.save()

            height = float(height) * 30.48
            if gender == 'M':
                total_calories = round((weight * 10) + (float(height) * 6.25) - (age * 5) + 5)
            else:
                total_calories = round((weight * 10) + (float(height) * 6.25) - (age * 5) - 161)
            if job == 'L':
                total_calories = round(total_calories * 1.1)
            elif job == 'M':
                total_calories = round(total_calories * 1.3)
            elif job == 'V':
                total_calories = round(total_calories * 1.5)
            else:
                total_calories = round(total_calories * 1.7)

            gw = goal_weight - weight
            weight_per_week = gw / goal_time_period
            cal_per_day = round(weight_per_week * 500)

            total_calories += cal_per_day
            bmi = weight/(height*height)


            instance = c_form.save(commit=False)
            instance.total_calories = total_calories
            instance.bmi = bmi
            instance.save()


            if gw < 0:
                carbs = round(0.40 * total_calories / 4)
                protons = round(0.40 * total_calories / 4)
                fats = round(0.20 * total_calories / 9)
            else:
                carbs = round(0.45 * total_calories / 4)
                protons = round(0.30 * total_calories / 4)
                fats = round(0.25 * total_calories / 9)

            # will print success message by a variable {{ message }} in html
            messages.success(request, f'TARGET DAILY CALORIES INTAKE: { total_calories } Kcal')
            messages.info(
                request, f'carbs : {carbs} gm, protiens: {protons} gm, fats : {fats} gm perday.')
            return redirect('get-dietplan')
    else:
        c_form = CaloriesCalculatorForm(instance=request.user.profile)
    context = {
        'c_form': c_form
    }
    return render(request, 'dietplan/dietplan.html', context)


@login_required
def getdietplan(request):
    return render(request, 'dietplan/getdietplan.html')


@staff_member_required
def ingredient(request):
    if request.method == 'POST':
        i_form = IngredientForm(request.POST)
        i_form.save()
        c = i_form.cleaned_data.get('carbs')
        p = i_form.cleaned_data.get('protein')
        f = i_form.cleaned_data.get('fat')
        cal = (c * 4) + (p * 4) + (f * 9)
        print(cal)
        instance = i_form.save(commit=False)
        instance.ingredient_calories = cal
        instance.save()

        # will print success message by a variable {{ message }} in html
        messages.success(request, f'ingredient saved successfully')
        return redirect('ingredient')

    else:
        i_form = IngredientForm(request.POST)

    context = {
        'i_form': i_form
    }
    return render(request, 'dietplan/i_form.html', context)


@staff_member_required
def meal(request):

    if request.method == 'POST':
        m_form = MealForm(request.POST)
        m_form.save()
        set1 = m_form.cleaned_data.get('ingredients')
        set2 = Ingredient.objects.all()
        calories = 0
        carbs = 0
        protein = 0
        fat = 0
        k = 0
        quantity = m_form.cleaned_data.get('quantity')
        q = quantity.split(',')
        for i in range(0, len(set1)):
            a = set1[i]
            for b in set2:
                if a == b:
                    cal = a.ingredient_calories*int(q[k])
                    c = a.carbs*int(q[k])
                    p = a.protein*int(q[k])
                    f = a.fat*int(q[k])
                    k = k+1
                    carbs = carbs + c
                    protein = protein + p
                    fat = fat + f
                    calories = calories + cal
        instance = m_form.save(commit=False)
        instance.meal_calories = calories
        instance.meal_carbs = carbs
        instance.meal_protein = protein
        instance.meal_fat = fat
        instance.save()
        # will print success message by a variable {{ message }} in html
        messages.success(request, f'meal saved successfully')
        return redirect('meal')

    else:
        m_form = MealForm(request.POST)

    context = {
        'm_form': m_form
    }
    return render(request, 'dietplan/m_form.html', context)


def vegdietplan(request):
    p = Profile.objects.get(id=request.user.id)
    cal = p.total_calories
    b_cal = round(cal*(1/5))
    print(b_cal)
    m = Meal.objects.all()  # getting all meal name in a list
    breakfast = ''
    for i in range(0, len(m)-1):
        if m[i].veg == True and m[i].breakfast == True:
            a = m[i].meal_calories
            if b_cal-50 < a < b_cal+50:
                result = ''
                result = f'{result}, {m[i].meal_name}'
                breakfast += result
            else:
                for j in range(i+1, len(m)):
                    if m[j].veg is True and m[j].breakfast is True:
                        b = m[j].meal_calories
                        if b_cal - 50 < a+b < b_cal + 50:
                            result = f'{m[i].meal_name}'
                            result += f', {m[j].meal_name}'
                            if breakfast != '':
                                breakfast += f'/ {result}'
                            breakfast += f'{result}'
    print(breakfast)
    messages.success(request, f'{ breakfast }', extra_tags='b')
    d = Dietplan.objects.get(id=request.user.id)
    #d.breakfast.add(breakfast)
    d.save()

    s_cal = round(cal * (3/20))

# getting all meal name in a list
    snacks = []
    for i in range(0, len(m) - 1):
        if m[i].veg == True and m[i].snacks == True:
            a = m[i].meal_calories
            if s_cal - 50 < a < s_cal + 50:
                result = []
                result.append(m[i].meal_name)
                snacks.append(result)
            else:
                for j in range(i + 1, len(m)):
                    if m[j].veg == True and m[j].snacks == True:
                        b = m[j].meal_calories
                        if s_cal - 50 < a + b < s_cal + 50:
                            result = []
                            result.append(str(m[i]),)
                            result.append(str(m[j]),)
                            snacks.append(result)

    b = ''
    for x in snacks:
        for y in x:
            if y == x[len(x)-1]:
                b += f'{y}'
                break
            b += f'{y}, '
        if x == snacks[len(snacks)-1]:
            break
        b += f'/ '
    messages.success(request, f'{ b }', extra_tags='s1')
    messages.success(request, f'{ b }', extra_tags='s2')

    l_cal = round(cal * (3/10))
  # getting all meal name in a list
    lunch = []
    for i in range(0, len(m) - 1):
        if m[i].veg == True and m[i].lunch == True:
            a = m[i].meal_calories
            if l_cal - 50 < a < l_cal + 50:
                result = []
                result.append(m[i].meal_name)
                lunch.append(result)
            else:
                for j in range(i + 1, len(m)):
                    if m[j].veg == True and m[j].lunch == True:
                        b = m[j].meal_calories
                        if l_cal - 50 < a + b < l_cal + 50:
                            result = []
                            result.append(str(m[i]), )
                            result.append(str(m[j]), )
                            lunch.append(result)
    b = ''
    for x in lunch:
        for y in x:
            if y == x[len(x)-1]:
                b += f'{y}'
                break
            b += f'{y}, '
        if x == lunch[len(lunch)-1]:
            break
        b += f'/ '

    messages.success(request, f'{ b }', extra_tags='l')
    #d = Dietplan.objects.get(id = request.user.id)
    #d.dietplan_name = 'abc'
    # d.breakfast.set(','.join(breakfast))
    # d.save()

    d_cal = round(cal * (1 / 5))

    dinner = []
    for i in range(0, len(m) - 1):
        if m[i].veg == True and m[i].dinner == True:
            a = m[i].meal_calories
            if d_cal - 50 < a < d_cal + 50:
                result = []
                result.append(m[i].meal_name)
                dinner.append(result)
            else:
                for j in range(i + 1, len(m)):
                    if m[j].veg == True and m[j].dinner == True:
                        b = m[j].meal_calories
                        if d_cal - 50 < a + b < d_cal + 50:
                            result = []
                            result.append(str(m[i]), )
                            result.append(str(m[j]), )
                            dinner.append(result)

    b = ''
    for x in dinner:
        for y in x:
            if y == x[len(x)-1]:
                b += f'{y}'
                break
            b += f'{y}, '
        if x == dinner[len(dinner)-1]:
            break
        b += f'/ '

    messages.success(request, f'{ dinner }', extra_tags='d')

    return render(request, 'dietplan/vegdietplan.html')


def non_vegdietplan(request):
    p = Profile.objects.get(id=request.user.id)
    cal = p.total_calories
    b_cal = round(cal*(1/5))

    m = Meal.objects.all()  # getting all meal name in a list
    breakfast = []
    for i in range(0, len(m)-1):
        if m[i].breakfast == True:
            a = m[i].meal_calories
            if b_cal-50 < a < b_cal+50:
                result = []
                result.append(m[i].meal_name)
                breakfast.append(result)
            else:
                for j in range(i+1, len(m)):
                    if m[j].breakfast is True:
                        b = m[j].meal_calories
                        if b_cal - 50 < a+b < b_cal + 50:
                            result = []
                            result.append(str(m[i]),)
                            result.append(str(m[j]),)
                            breakfast.append(result)
    b = ''
    for x in breakfast:
        for y in x:
            if y == x[len(x)-1]:
                b += f'{y}'
                break
            b += f'{y}, '
        if x == breakfast[len(breakfast)-1]:
            break
        b += f'/ '

    messages.success(request, f'{ b }', extra_tags='b1')

    s_cal = round(cal * (3/20))

 # getting all meal name in a list
    snacks = []
    for i in range(0, len(m) - 1):
        if m[i].snacks == True:
            a = m[i].meal_calories
            if s_cal - 50 < a < s_cal + 50:
                result = []
                result.append(m[i].meal_name)
                snacks.append(result)
            else:
                for j in range(i + 1, len(m)):
                    if m[j].snacks == True:
                        b = m[j].meal_calories
                        if s_cal - 50 < a + b < s_cal + 50:
                            result = []
                            result.append(str(m[i]), )
                            result.append(str(m[j]), )
                            snacks.append(result)

    b = ''
    for x in snacks:
        for y in x:
            if y == x[len(x)-1]:
                b += f'{y}'
                break
            b += f'{y}, '
        if x == snacks[len(snacks)-1]:
            break
        b += f'/ '

    messages.success(request, f'{ b }', extra_tags='s1')
    messages.success(request, f'{ b }', extra_tags='s2')

    l_cal = round(cal * (3/10))
  # getting all meal name in a list
    lunch = []
    for i in range(0, len(m) - 1):
        if m[i].lunch == True:
            a = m[i].meal_calories
            if l_cal - 50 < a < l_cal + 50:
                result = []
                result.append(m[i].meal_name)
                lunch.append(result)
            else:
                for j in range(i + 1, len(m)):
                    if m[j].lunch == True:
                        b = m[j].meal_calories
                        if l_cal - 50 < a + b < l_cal + 50:
                            result = []
                            result.append(str(m[i]), )
                            result.append(str(m[j]), )
                            lunch.append(result)

    b = ''
    for x in lunch:
        for y in x:
            if y == x[len(x)-1]:
                b += f'{y}'
                break
            b += f'{y}, '
        if x == lunch[len(lunch)-1]:
            break
        b += f'/ '

    messages.success(request, f'{ b }', extra_tags='l')
    #d = Dietplan.objects.get(id = request.user.id)
    #d.dietplan_name = 'abc'
    # d.breakfast.set(','.join(breakfast))
    # d.save()

    d_cal = round(cal * (1 / 5))

    dinner = []
    for i in range(0, len(m) - 1):
        if m[i].dinner == True:
            a = m[i].meal_calories
            if d_cal - 50 < a < d_cal + 50:
                result = []
                result.append(m[i].meal_name)
                dinner.append(result)
            else:
                for j in range(i + 1, len(m)):
                    if m[j].dinner == True:
                        b = m[j].meal_calories
                        if d_cal - 50 < a + b < d_cal + 50:
                            result = []
                            result.append(str(m[i]), )
                            result.append(str(m[j]), )
                            dinner.append(result)

    b = ''
    for x in dinner:
        for y in x:
            if y == x[len(x)-1]:
                b += f'{y}'
                break
            b += f'{y}, '
        if x == dinner[len(dinner)-1]:
            break
        b += f'/ '

    messages.success(request, f'{ b }', extra_tags='d')

    return render(request, 'dietplan/vegdietplan.html')
