import csv
from app.dao.postdao import PostDao
from app.dao.userdao import UserDao
from app.exceptions.business_exception import BusinessException
from io import StringIO, TextIOWrapper
from app.exceptions.csv_validator import PostCsvValidator


class PostService:

    # Get All Posts (Without deleted post)
    @staticmethod
    def get_all_posts(page, per_page, role=None, login_user_id=None):
        if role:             # normal user
            return PostDao.get_all_posts(page, per_page, login_user_id)

        return PostDao.get_all_posts(page, per_page)


    # Get Single Post by Specifi Post ID
    @staticmethod
    def get_post_by_id(post_id, role, user_id):
        post = PostDao.find_by_id(post_id)

        if role and post.create_user_id != user_id:
            return {
                "success": False,
                "field": "authorization",
                "message": "You are not allowed to view this post"
            }

        if not post:
            return {
                "success": False,
                "field": "post_id",
                "message": "Post not found"
            }

        created_user = None
        updated_user = None

        if post.create_user_id:
            created_user = UserDao.find_by_id(post.create_user_id)
            if created_user:
                created_user = "User" if created_user.role else "Admin"
        if post.updated_user_id:
            updated_user = UserDao.find_by_id(post.updated_user_id)
            if updated_user:
                updated_user = "User" if updated_user.role else "Admin"

        return {
            "success": True,
            "data": {
                **post.to_dict(),
                "created_user": created_user,
                "updated_user": updated_user
            }
        }


    # Create Post
    @staticmethod
    def create_post(payload, login_user_id):
        # Title duplicate check
        title_exist = PostDao.find_by_title(payload.title)
        if title_exist:
            raise BusinessException(
                field="title",
                message="Title has already been taken"
            )

        post = PostDao.create_post(
            title=payload.title,
            description=payload.description,
            create_user_id=login_user_id
        )
        return post


    # Update Post
    @staticmethod
    def update_post(post_id, payload, role, login_user_id):
        # check post exists
        post = PostDao.find_by_id(post_id)
        if not post:
            raise BusinessException(
                field="post_id",
                message="Post not found"
            )

        if role and post.create_user_id != login_user_id:
            raise BusinessException(
                field="authorization",
                message="You are not allowed to update this post"
            )

        # Title duplicate check
        title_exist = PostDao.find_by_title(payload.title)
        if title_exist and title_exist.id != post.id:
            raise BusinessException(
                field="title",
                message="Title has already been taken"
            )

        post = PostDao.update_post(
            post,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            updated_user_id=login_user_id
        )
        return post


    # Soft Delete Post
    @staticmethod
    def delete_post(post_ids, role, login_user_id):
        posts = PostDao.find_by_ids(post_ids)

        if not posts:
            raise BusinessException(
                field="post_ids",
                message="Post not found"
            )

        if role:
            for post in posts:
                if post.create_user_id != login_user_id:
                    raise BusinessException(
                        field="authorization",
                        message="You are not allowed to delete this post"
                    )

        PostDao.delete_posts(posts, login_user_id)


    # Post Download
    @staticmethod
    def export_post_csv(post_ids):
        posts = PostDao.find_by_ids(post_ids)

        if not posts:
            return None

        def generate():
            buffer = StringIO()         # memory-based file-like object
            writer = csv.writer(buffer)

            # Header
            writer.writerow([
                "ID", "Title", "Description", "Status", "Create User ID", "Updated User ID",
                "Deleted User ID", "Deleted At", "Created At", "Updated At",

            ])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

            # Rows (streaming)
            for post in posts:
                writer.writerow([
                    post.id,
                    post.title,
                    post.description,
                    post.status,
                    post.create_user_id,
                    post.updated_user_id,
                    post.deleted_user_id,
                    post.deleted_at,
                    post.created_at.strftime("%Y-%m-%d"),
                    post.updated_at.strftime("%Y-%m-%d")
                ])
                yield buffer.getvalue()
                buffer.seek(0)
                buffer.truncate(0)

        return generate


    # Post Import
    @staticmethod
    def import_post_csv(file, login_user_id):
        if not file:
            raise BusinessException(
                field="file",
                message="CSV File Field is required"
            )

        reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))

        # Header Validation
        PostCsvValidator.validate_headers(reader.fieldnames)

        posts_data = []
        total_count = 0

        for row in reader:
            total_count += 1

            # Skip empty rows
            if not any(row.values()):
                continue

            validated = PostCsvValidator.validate_row(row, total_count)
            validated["create_user_id"] = login_user_id
            posts_data.append(validated)

            # Optional: batch insert every 500 rows
            if len(posts_data) >= 500:
                PostDao.bulk_insert(posts_data)
                posts_data = []

        # Insert remaining rows
        if posts_data:
            PostDao.bulk_insert(posts_data)

        return total_count


    # Search post by keyword  (title, desc, status, created_date)
    @staticmethod
    def search_posts(role, user_id, title=None, description=None, status=None, date=None, page=1, per_page=10):
        if role:
            return PostDao.search_posts(title, description, status, date, page, per_page, user_id)

        return PostDao.search_posts(title, description, status, date, page, per_page)
