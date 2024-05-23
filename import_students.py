# import os
# import django
# import csv
# import datetime

# # Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
# django.setup()

# from users.models import CustomUser, Student, Batch,Faculty
# from django.contrib.auth.models import Group
# from django.shortcuts import get_object_or_404

# def current_year():
#     return datetime.date.today().year

# def year_choices():
#     return [(r, r) for r in range(1980, current_year() + 1)]

# def import_students(csv_file):
#     try:
#         with open(csv_file, newline='', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             student_group, created = Group.objects.get_or_create(name='student')

#             faculty = get_object_or_404(Faculty, id=3)# for rhythm mam batch
#             print(faculty)

#             for row in reader:
#                 enrollment_number = row['Enrolment No']
#                 full_name = row['Student Name']
#                 first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')
#                 # print(first_name,last_name,)

#                 user, created = CustomUser.objects.get_or_create(
#                     username=f"{first_name}{enrollment_number[:3]}",
#                     defaults={
#                         'first_name': first_name,
#                         'last_name': last_name,
#                         'password': f"{first_name[0]}{enrollment_number}",  # you may want to set a default password
#                     }
#                 )
#                 print(f"user {user} created successfully ")
#                 if created:
#                     user.groups.add(student_group)
#                     print(f"{user} added to {student_group} successfully")


#                 # Assuming you have a way to determine batch_year, semester, section, shift
#                 batch_year = 2024  # Replace with your logic
#                 semester = 6       # Replace with your logic
#                 section = 'A'      # Replace with your logic
#                 shift = 'Morning'  # Replace with your logic

#                 batch, created = Batch.objects.get_or_create(
#                     year=batch_year,
#                     section=section,
#                     shift=1,  # Replace with appropriate logic to get the correct shift
#                     course='bca',  # Replace with appropriate logic to get the correct course
#                     assigned_to=faculty
#                 )

#                 print(f"Batch {batch} Created successfully")

#                 student, created = Student.objects.get_or_create(
#                     user=user,
#                     defaults={
#                         'enrollment_number': enrollment_number,
#                         'batch': batch,
#                         'batch_year': batch_year,
#                         'semester': semester,
#                         'section': section,
#                         'shift': shift,
#                         'about':"Student of Maharaja Surajmal Institute"
#                     }
#                 )

#                 print(f'Successfully processed {student} with  {enrollment_number}')

#     except FileNotFoundError:
#         print(f'File "{csv_file}" does not exist')

# if __name__ == "__main__":
#     csv_file = 'student_list1.csv'  # Path to your CSV file
#     import_students(csv_file)


# import os
# import django

# # Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
# django.setup()

# from users.models import CustomUser, Student
# from django.contrib.auth.hashers import make_password,check_password

# def hash_and_update_passwords():
#     students = Student.objects.all()
    
#     for student in students:
#         user = student.user
#         # Assuming the current password is in the format: first_initial + enrollment_number
#         initial_password = f"{user.first_name[0]}{student.enrollment_number}"
#         print(initial_password)
#         hashed_password = make_password(initial_password)
#         print(hashed_password)
#         #decrypted passwrord 
#         user.password = hashed_password
#         user.save()
#         print(f"Updated password for user: {user.username}")

#         # Verify the hashed password
#         if check_password(initial_password, user.password):
#             print(f"Password verification successful for user: {user.username}")
#         else:
#             print(f"Password verification failed for user: {user.username}")

# if __name__ == "__main__":
#     hash_and_update_passwords()
