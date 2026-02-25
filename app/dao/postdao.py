from app.extension import db
from app.models.post import Post
from sqlalchemy import or_
from datetime import datetime, time


class PostDao:

    # Get All Posts (Without deleted post)
    @staticmethod
    def get_all_posts(page, per_page, login_user_id=None):
        query = Post.query.filter(Post.deleted_at.is_(None))

        if login_user_id is not None:
            query = query.filter(Post.create_user_id == login_user_id)

        return query.order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )


    # Filter by Post title (Without deleted post)
    @staticmethod
    def find_by_title(title):
        return Post.query.filter(
            Post.title == title,
            Post.deleted_at.is_(None)
        ).first()


    # Filter by Post ID (Without deleted post)
    @staticmethod
    def find_by_id(post_id):
        return Post.query.filter(
            Post.id == post_id,
            Post.deleted_at.is_(None)
        ).first()


    # Filter by Multiple Post ID (Without deleted post)
    @staticmethod
    def find_by_ids(post_ids: list[int]):
        return Post.query.filter(
            Post.id.in_(post_ids),
            Post.deleted_at.is_(None)
        ).all()


    # Create Post
    @staticmethod
    def create_post(**kwargs):
        post = Post(**kwargs)
        db.session.add(post)
        return post


    # Update Post
    @staticmethod
    def update_post(post, **kwargs):
        for key, value in kwargs.items():
            setattr(post, key, value)

        return post


    # Soft Delete Post
    @staticmethod
    def delete_posts(posts: list[Post], deleted_user_id):
        for post in posts:
            post.deleted_at = datetime.utcnow()
            post.deleted_user_id = deleted_user_id


    # Multiple Post Insert
    @staticmethod
    def bulk_insert(posts_data: list[dict]):
        objs = [Post(**data) for data in posts_data]
        db.session.bulk_save_objects(objs)


    # Search post by keyword  (title, desc, status, created_date)
    @staticmethod
    def search_posts(title=None, description=None, status=None, date=None, page=1, per_page=10, user_id=None):
        query = Post.query.filter(Post.deleted_at.is_(None))

        if user_id is not None:
            query = query.filter(Post.create_user_id == user_id)

        # if keyword:
        #     query = query.filter(
        #         or_(
        #             Post.title.ilike(f"%{keyword}%"),
        #             Post.description.ilike(f"%{keyword}%")
        #         )
        #     )

        if title is not None:
            query = query.filter(Post.title.ilike(f"%{title}%"))

        if description is not None:
            query = query.filter(Post.description.ilike(f"%{description}%"))

        if status is not None:
            query = query.filter(Post.status == status)

        if date:
            try:
                selected_date = datetime.strptime(date, "%Y-%m-%d")
                start_of_day = datetime.combine(selected_date.date(), time.min)

                query = query.filter(Post.created_at >= start_of_day)
            except ValueError:
                # invalid date format → no result
                query = query.filter(False)

        return query.order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
