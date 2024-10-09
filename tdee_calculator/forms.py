from django import forms
from .models import UserData

class TDEEForm(forms.ModelForm):
    ACTIVITY_LEVEL_CHOICES = [
        (1.2, 'Ít vận động (ít hoặc không tập luyện)'),
        (1.375, 'Vận động nhẹ (tập luyện nhẹ nhàng 1-3 ngày/tuần)'),
        (1.55, 'Vận động vừa (tập luyện vừa phải 3-5 ngày/tuần)'),
        (1.725, 'Vận động nhiều (tập luyện nặng 6-7 ngày/tuần)'),
        (1.9, 'Rất năng động (tập luyện rất nặng, công việc thể lực)'),
    ]

    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES,
        label='Mức độ hoạt động'
    )

    GENDER_CHOICES = [
        ('Male', 'Nam'),
        ('Female', 'Nữ')
    ]

    GOAL_CHOICES = [
        ('maintain', 'Duy trì cân nặng'),
        ('lose', 'Giảm cân'),
        ('gain', 'Tăng cân'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Giới tính'
    )

    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        label='Mục tiêu'
    )

    class Meta:
        model = UserData
        fields = ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']
        labels = {
            'weight': 'Cân nặng (kg)',
            'height': 'Chiều cao (cm)',
            'age': 'Tuổi'
        }
