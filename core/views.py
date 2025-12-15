from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.translation import gettext as _


def register(request):
    """تسجيل مستخدم جديد"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('تم إنشاء الحساب بنجاح'))
            return redirect('home')
    else:
        form = UserCreationForm()
    
    # إضافة classes للحقول
    for field in form.fields.values():
        field.widget.attrs['class'] = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500'
    
    return render(request, 'auth/register.html', {'form': form})

