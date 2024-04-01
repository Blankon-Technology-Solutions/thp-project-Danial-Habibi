# TAKE HOME PROJECT BLANKON TECHNOLOGY SOLUTIONS

First of all, congratulations on reaching this step in the interview series. The take-home project is mainly designed to assess how well you structure your code and how efficiently you build a solution for the given task.

## Requirements for the take home project:
- 🫙 Please utilize Docker for easy setup and testing on our side 🫙 
- 🧪 minimum 80% test coverage 🧪 
- 🐍 The project must be written in Python and utilize Django REST framework🐍
- ❗️ You must use your own third-party credentials, such as a Google API Key or LinkedIn API Key, for your local testing. However, please do not share them in any of these files; we will use our own credentials to test it. ❗️ 

# Simple Backend Todo App
## Create a backend service for a Todo App with the following specifications:
- user can login/signup using Linkedin SSO and Google SSO
- user can login/signup using an email and password combination
- user can list,add,update and delete their todos
- If a user is logged in with the same credentials on two or more browsers, when they add, update, or delete a todo in one browser, it should sync to all browsers via socket (push mechanism
- Except for login/signup, other APIs and socket connections must be protected.



## When you are done
- 🫸 push your code to this repository, or if you put it in different branch please merge to main branch 🫸
- 🏷️ Go to issues tab, you will have 1 open issue please label that issue to Ready to Review 🏷️ 
==================================================================================================================================================================================================
To run the apps

1. `docker build -t your_image_name .`
2. `docker run -p 8000:8000 your_image_name`
3. To Create user
```
curl --location 'http://localhost:8000/api/auth/register/' \
--header 'Content-type: application/json' \

--data '{
      "username": "user2",
      "password1": "complexpassword123",
      "password2": "complexpassword123"
  }'
  
  ```
4. To Login

```
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-type: application/json' \
--data '{
      "username": "user1",
      "password": "complexpassword123"
  }'

```
The token from login can be use for Authentication Header

5. To view list of Available Task

```
curl --location 'http://127.0.0.1:8000/api/task-list/' \
--header 'Authorization: Token <Your_TOKEN>'
``` 
6. To View list of Todo API 

```
curl --location 'http://127.0.0.1:8000/api/' \
--header 'Authorization: Token <Your_Token>'
```

7. To Create Todo

```
curl --location 'http://localhost:8000/api/task-create/' \
--header 'Authorization: Token <Your_TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
        "title": "New Task 5",
        "completed": false
    }'
```


