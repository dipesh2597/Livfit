from django.contrib import admin
from django.contrib.auth.models import User
from . models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender', 'age', 'weight', 'height', 'job', 'goal_weight',
                    'goal_time_period',  'bmi', 'total_calories', 'date')
    readonly_fields = ('id', 'gender', 'age', 'weight', 'height', 'job',
                       'goal_weight', 'goal_time_period', 'total_calories', 'date')


admin.site.register(Profile, ProfileAdmin)
