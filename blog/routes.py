from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import BlogPost
from app import db

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/", methods=["GET"])
@jwt_required()
def home():
    return jsonify({"msg": "Homepage"}), 200


@blog_bp.route("/api/blog/add", methods=["POST"])
@jwt_required()
def blog_add():
    data = request.get_json()
    title = data["title"]
    body = data["body"]

    existing_post = BlogPost.query.filter_by(title=title).first()

    if existing_post:
        return jsonify({"error": "Запись уже существует"})

    current_user_id = get_jwt_identity()

    try:
        new_blog_post = BlogPost(title=title, body=body, user_id=current_user_id)
        print(new_blog_post)
        db.session.add(new_blog_post)
        db.session.commit()
        return (
            jsonify(
                {
                    "msg": f'Успешно создана запись в блоге: "{title}"',
                    "new_blog_post": new_blog_post.to_dict(),
                }
            ),
            201,
        )
    except Exception as er:
        return jsonify({"error": str(er)}), 500


@blog_bp.route("/api/blog", methods=["GET"])
@jwt_required()
def blog():
    blog_posts = BlogPost.query.all()
    blog_posts_result = [post.to_dict() for post in blog_posts]
    return jsonify(blog_posts_result), 200


@blog_bp.route("/api/blog/<int:post_id>", methods=["GET"])
@jwt_required()
def blog_get_post_by_id(post_id):
    blog_post = BlogPost.query.get(post_id)

    if blog_post is None:
        return jsonify({"error": "Запись не найдена"}), 404

    return jsonify(blog_post.to_dict(), 200)


@blog_bp.route("/api/blog/<int:post_id>", methods=["PUT"])
@jwt_required()
def blog_update_post_by_id(post_id):
    data = request.get_json()
    title = data["title"]
    body = data["body"]

    blog_post = BlogPost.query.get(post_id)

    if blog_post is None:
        return jsonify({"error": "Запись не найдена"}), 404
    else:
        blog_post.title = title
        blog_post.body = body

        db.session.commit()

        return jsonify(
            {
                "msg": f'Успешно обновлена запись в блоге: "{post_id}"',
                "blog_post": blog_post.to_dict(),
            },
            201,
        )


@blog_bp.route("/api/blog/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_blog_post_by_id(post_id):
    blog_post = BlogPost.query.get(post_id)

    if blog_post is None:
        return jsonify({"error": "Запись не найдена"}), 404
    else:
        db.session.delete(blog_post)
        db.session.commit()
        return jsonify(
            {"msg": f"Успешно удалена запись в блоге с идентификатором: {post_id}"}, 200
        )


@blog_bp.route("/api/blog/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_blog_posts_by_user(user_id):
    current_user_id = get_jwt_identity()

    if current_user_id != user_id:
        return jsonify({"error": "Доступ запрещен"}), 403

    user_posts = BlogPost.query.filter_by(user_id=user_id).all()

    user_posts_result = [post.to_dict() for post in user_posts]

    return jsonify(
        {
            "msg": f'Успешно получены посты для пользователя: "{user_id}"',
            "user_posts_result": user_posts_result,
        },
        200,
    )
