@app.route("/", methods=["GET"])
@jwt_required()
def home():
    return jsonify({"msg": "Homepage"}), 200


@app.route("/api/blog/add", methods=["POST"])
@jwt_required()
def blog_add():
    data = request.get_json()
    title = data["title"]
    body = data["body"]

    try:
        blog_post = BlogPost(title=title, body=body)
        db.session.add(blog_post)
        db.session.commit()
        return (
            jsonify(
                {
                    "msg": f'Успешно создана запись в блоге: "{title}"',
                    "blog_post": blog_post.to_dict(),
                }
            ),
            201,
        )
    except Exception as er:
        return jsonify({"error": str(er)}), 500


@app.route("/api/blog", methods=["GET"])
@jwt_required()
def blog():
    blog_posts = BlogPost.query.all()
    blog_posts_result = [post.to_dict() for post in blog_posts]
    return jsonify(blog_posts_result), 200


@app.route("/api/blog/<int:post_id>", methods=["GET"])
@jwt_required()
def blog_get_post_by_id(post_id):
    blog_post = BlogPost.query.get(post_id)

    if blog_post is None:
        return jsonify({"error": "Запись не найдена"}), 404

    return jsonify(blog_post.to_dict(), 200)


@app.route("/api/blog/<int:post_id>", methods=["PUT"])
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


@app.route("/api/blog/<int:post_id>", methods=["DELETE"])
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
