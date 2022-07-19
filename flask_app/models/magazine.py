from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Magazine:
    db = 'magazine_exam'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save_magazine(cls, data):
        query = "INSERT INTO magazines (user_id, title, description) VALUES (%(user_id)s, %(title)s, %(description)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_magazine_by_id(cls,data):
        query = "SELECT * FROM magazines JOIN users ON users.id = magazines.user_id WHERE magazines.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            magazine = cls(results[0])
            user_data = {
                "id":results[0]['users.id'],
                "first_name":results[0]['first_name'],
                "last_name":results[0]['last_name'],
                "email":results[0]['email'],
                "password":results[0]['password'],
                "created_at":results[0]['users.created_at'],
                "updated_at":results[0]['users.updated_at']
            }
            magazine_maker = user.User(user_data)
            magazine.creator = magazine_maker
            return magazine

    @classmethod
    def get_all_magazines(cls):
        query = "SELECT * FROM magazines JOIN users ON users.id = magazines.user_id"
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @classmethod
    def delete_magazine(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @staticmethod
    def new_magazine_validation(data):
        is_valid = True
        if len(data['title']) < 2:
            flash('Title must be 2 or more characters', "magazine")
            is_valid = False
        if len(data['description']) < 10:
            flash('Description must be 10 or more characters', "magazine")
            is_valid = False
        return is_valid