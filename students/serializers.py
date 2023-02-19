from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")


    def validate(self, attrs):
        students_on_course = Student.objects.filter(course__name=attrs['name'])

        if 'students' in attrs:
            students_count_in_data = len(attrs['students'])

            if len(students_on_course) > 5 or (students_count_in_data) > 5:
                raise ValidationError('Допускается не более 5 студентов на курсе')

        return attrs


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


