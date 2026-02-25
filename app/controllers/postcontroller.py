from app.core.transactional import transactional
from app.requests.postrequest import CreatePostRequest, PostSearchRequest, UpdatePostRequest
from app.services.postservice import PostService
from pydantic import ValidationError
from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


class PostController:

    # Get All Posts (Without deleted post)
    @staticmethod
    @jwt_required(optional=True)
    def get_all_posts():
        claims = get_jwt()
        identity = get_jwt_identity()
        role = claims.get("role")
        login_user_id = int(identity) if identity else None
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        pagination = PostService.get_all_posts(
            page, per_page, role, login_user_id)

        return jsonify({
            "success": True,
            "data": [
                post.to_dict()
                for post in pagination.items
            ],
            "meta": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "total_pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }), 200


    # Get Single Post by Specifi Post ID
    @staticmethod
    @jwt_required()
    def get_post_by_id(post_id):
        claims = get_jwt()
        role = claims.get("role")
        login_user_id = int(get_jwt_identity())
        result = PostService.get_post_by_id(post_id, role, login_user_id)

        if not result["success"]:
            return jsonify(
                [
                    {
                        "loc": [result["field"]],
                        "msg": result["message"]
                    }
                ]
            ), 400

        return jsonify({
            "success": True,
            "data": result["data"],
        }), 200


    # Create Post
    @staticmethod
    @jwt_required()
    @transactional
    def create_post():
        payload = CreatePostRequest(**request.form)
        login_user_id = int(get_jwt_identity())
        post = PostService.create_post(payload, login_user_id)

        return jsonify({
            "success": True,
            "data": post.to_dict(),
            "message": "Post created successfully"
        }), 201


    # Update Post
    @staticmethod
    @jwt_required()
    @transactional
    def update_post(post_id):
        payload = UpdatePostRequest(**request.form)
        claims = get_jwt()
        role = claims.get("role")
        login_user_id = int(get_jwt_identity())
        post = PostService.update_post(
            post_id, payload, role, login_user_id)

        return jsonify({
            "success": True,
            "data": post.to_dict(),
            "message": "Post updated successfully"
        }), 200


    # Soft Delete Post
    @staticmethod
    @jwt_required()
    @transactional
    def delete_post():
        payload = request.get_json()
        claims = get_jwt()
        role = claims.get("role")
        login_user_id = int(get_jwt_identity())
        PostService.delete_post(payload["post_ids"], role, login_user_id)

        return jsonify({
            "success": True,
            "message": "Post Deleted Successfully"
        }), 200


    # Search post by keyword  (title, desc, status, created_date)
    @staticmethod
    @jwt_required()
    def search_posts():
        try:
            payload = PostSearchRequest(**(request.get_json() or {}))
        except ValidationError as e:
            return jsonify(
                [
                    {"loc": err["loc"], "msg": err["msg"]}
                    for err in e.errors()
                ]
            ), 422

        claims = get_jwt()
        role = claims.get("role")
        login_user_id = int(get_jwt_identity())
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = PostService.search_posts(
            role=role,
            user_id=login_user_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            date=payload.date,
            page=page,
            per_page=per_page
        )

        return jsonify({
            "success": True,
            "data": [
                post.to_dict()
                for post in pagination.items
            ],
            "meta": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "total_pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }), 200


    # Post Download
    @staticmethod
    @jwt_required(optional=True)
    def export_post_csv():
        payload = request.get_json()
        generator = PostService.export_post_csv(payload["post_ids"])

        if not generator:
            return jsonify([
                {"loc": ["post_id"], "msg": "Post not found"}
            ]), 400

        return Response(
            generator(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=posts.csv"}
        )


    # Post Import
    @staticmethod
    @jwt_required()
    @transactional
    def import_post_csv():
        file = request.files.get('file')
        login_user_id = int(get_jwt_identity())

        count = PostService.import_post_csv(file, login_user_id)

        return jsonify({
            "success": True,
            "message": f"Imported successfully",
            "count": count
        }), 200
