
# Samvadika - An online Interaction Platform


## Problem Statement or Motivation
An online discussion forum for the students and faculty of IITB to discuss various topics of their interest.
In the current online semester, several students of our college have a tough time finding like minded people to share their thoughts and creativity. A discussion forum is a great way for students to talk about what they love and find other people sharing the same interests. Similarly the current scenario makes it tough for students to find the right people to ask and clarify their doubts. As a solution, we've built samvadika, an online discussion forum for students to interact with each other and have light-hearted discussions.


## Sell your product or service
Samvadika is an online platform for students to share thoughts, start a discussion on any topic and filter people who are into various hobbies.

## List of features
- Posting questions and replies in the form of threads
- Like and dislike questions
- Upvote and downvote replies
- Finding people with similar hobbies
- Save questions so as to access them easily in the future
- Notification page showing all the notifications on the platform
- A score for each user by looking at his/her activity

## Technology Stack
- **Python**
- Django
- Ajax
- **SQLite**
- **HTML, CSS, Bootstrap, JS**

## List of deliverables
- [x] Post Questions and replies/comments
  - [x] Upvotes and Downvotes for each question and replies
  - [x] Save Question or Comment option
  - [x] Question can be tagged with default tags or custom created tags
- [x] Personal Dashboard for each user
  - [x] Interface to find people of same interest and search by interest/hobby functionality
  - [x] Score based on User posted Questions/comments votes
  - [x] CRUD on First name, Last name, Username and Password
- [x] Notification interface and Search functionality
  - [x] Each user can see their related activity in Notification page
  - [x] Fast searching of Questions by tag
- [x] Authentication system
  - [x] Signup with required info like username, password, email, first name and last name etc and login in secured way

## Hardware/Software Requirements
Operating System - Windows, macOS, Linux/Unix with atleast 4 GB RAM <br>
Software -  Python 3.6 to 3.8, Django

## How to operate
Once the repository is cloned, run the following commands:
```
cd project-code_busters
source bin/activate
cd samvadika
python manage.py makemigrations
python manage.py migrate
```
To create a superuser, run ```python manage.py createsuperuser``` and enter the required data. Finally to run the project, execute <br>
```python manage.py runserver``` <br>
A login page could now be accessed by visiting the URL http://127.0.0.1:8000. Using the "Register here" button in the login page, new users can register and get access to the discussion forum.

## Primary stakeholders of the product built
The platform would be used by students and faculties of IIT Bombay.

## Team details along with the contribution
Team Name: **Code Busters** <br/>
Ajay Ravindran (213059004) <br/>
Naveen Badathala (213050052) <br/>
Tushar Tomar (213050023) <br/>
Vivek Anil Pandey (21q05r004) <br/>
Contributions:
* Post Questions and replies/comments - **Tushar, Vivek**
* Questions tagging with default tags or custom created tags and filter by tags functionality - **Naveen, Tushar**
* Upvotes and Downvotes for each question and replies - **Ajay**
* Save Question or Comment option - **Vivek**
* Find people Interface to find people of same interest and search by interest/hobby functionality - **Naveen**
* Notifications and Score Calculation based on User related activity - **Vivek, Ajay**
* Update Profile functionality - Name, password, profile picture,hobbies and social links - **Tushar, Naveen**
* Authentication- User Signup and Sigin Interface - **Tushar**
* Sphinx Documentation - **Naveen**
* Testing and Code comments - **Ajay, Naveen, Tushar, Vivek**
## Path to Code Documentation
project-code_busters/docs/build/html/index.html
