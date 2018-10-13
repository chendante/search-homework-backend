from project.models.base import Database


class song_list:
    @staticmethod
    def song_number():
        Database.cursor.execute("SELECT COUNT(ID) from song_list")
        data = Database.cursor.fetchall()
        return data[0][0]

    @staticmethod
    def song_name_list():
        Database.cursor.execute("SELECT song_id,song_name from song_list")
        data = Database.cursor.fetchall()
        return data
