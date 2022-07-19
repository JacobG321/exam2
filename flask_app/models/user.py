from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import magazine


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'magazine_exam'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines = []


    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])


    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])


    @classmethod
    def check_if_email_in_system(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        else:
            return True

    @classmethod
    def get_one_user_with_magazines(cls, data):
        query = "SELECT * FROM users LEFT JOIN magazines ON users.id = magazines.user_id WHERE users.id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            user_instance = cls(results[0])
            for this_magazine_dictionary in results:
                if this_magazine_dictionary['magazines.id'] == None:
                    break
                new_magazine_dictionary = {
                    "id": this_magazine_dictionary['magazines.id'],
                    "user_id":this_magazine_dictionary['user_id'],
                    "title": this_magazine_dictionary['title'],
                    "description": this_magazine_dictionary['description'],
                    "created_at": this_magazine_dictionary['magazines.created_at'],
                    "updated_at": this_magazine_dictionary['magazines.updated_at']
                }
                this_magazine_object = magazine.Magazine(new_magazine_dictionary)
                user_instance.magazines.append(this_magazine_object)
            return user_instance

    @classmethod
    def update_user_info(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def new_user_validation(data):
        is_valid = True
        if not EMAIL_REGEX.match(data["email"]):
            flash('Invalid Email', 'register')
            is_valid = False
        if len(data['first_name']) < 3:
            flash('First name must be more than 3 characters', 'register')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name must be more than 3 characters', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be 8 or more characters', 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def update_user_validation(data):
        is_valid = True
        if not EMAIL_REGEX.match(data["email"]):
            flash('Invalid Email', 'update')
            is_valid = False
        if len(data['first_name']) < 3:
            flash('First name must be more than 3 characters', 'update')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name must be more than 3 characters', 'update')
            is_valid = False
        return is_valid

