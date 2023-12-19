<h2>Simple Exam Application using Django</h2>
<h3>Introduction</h3>
This project is a simple  exam application developed with Django, designed to facilitate the creation and management of multiple-choice exams by teachers for their respective classes.I tried this during early COVID-19 as classes were shifiting online. But by the time I finished this application there were alot of tools and sites there for online exams. Butt anyway this was a great django practice.

<h3>Key Features</h3>
User Roles: Distinguishes between teacher and student accounts.
Class Management: Allows teachers to create and organize classes.
Exam Creation: Enables teachers to compose exams, adding questions and their respective choices.
Access Control: Requires a unique 16-digit code for students to participate in an exam.
Secure Code Generation: Utilizes a random string generator to create unique access codes.

<h3>How It Works</h3>
Teacher Account Creation: Teachers register and log in to their accounts.
Class Setup: Teachers create classes for their respective subjects.
Exam Creation: Teachers generate exams by adding questions and their multiple choices.
Code Generation: Upon completing the question set, teachers receive a 26-digit access code for students to access that question set.
Student Participation: Students log in with their credentials and use the provided code to access and take exams.
Answer check: The student can see their result instantly and also admin will be able to view the marks each student got in the backend 


<h3>Usage</h3>
Setup
Clone this repository to your local environment.
Install dependencies using pip install -r requirements.txt.
Run the Django server locally with python manage.py runserver.

<h3>Configuration</h3>
Configure database settings and any required environment variables.
Customize the application as per specific requirements.

<h3>Contributing</h3>
Contributions are encouraged! Please follow the outlined guidelines for code contributions and submit pull requests.


<h3>Acknowledgments</h3>
Special thanks to the Django community for their invaluable resources and support throughout the development process.
