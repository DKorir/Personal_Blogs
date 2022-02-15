class Comment:
    all_comments = []
    @classmethod
    def get_comments(cls,id):

        response = []

        for comment in cls.all_comments:
            if comment.quote_id == id:
                response.append(comment)

        return response