from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import core
from typing import Any


def create_app(static_folder):
    app = Flask(__name__, static_folder=static_folder, static_url_path="/")

    # 处理按键输入
    @app.route("/api/input", methods=["POST"])
    def handle_input():
        data = request.get_json()
        if not data or "key" not in data or "expression" not in data:
            return jsonify({"error": "无效的输入"}), 400

        key: str = data["key"]
        expression: list[str] = data["expression"]
        state: dict[str, Any] = data["state"]

        expression: list[str] = core.handle_input(expression, key)
        result = core.calculate(expression, state)

        return jsonify({"expression": expression, "result": result})

    # 默认路由，返回前端的入口页面
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        assert app.static_folder is not None
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # 如果路径不存在，则返回 index.html
            return send_from_directory(app.static_folder, "index.html")

    return app


# 启动应用
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    static_folder_path = "../frontend/out"  # 默认静态文件路径
    production_mode = False  # 默认开发模式

    if len(sys.argv) > 1:
        static_folder_path = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2].lower() == "production":
        production_mode = True

    if not os.path.isabs(static_folder_path):
        # 将相对路径转换为绝对路径
        static_folder_path = os.path.abspath(static_folder_path)

    if not os.path.exists(static_folder_path):
        print(f"错误: 指定的静态文件路径不存在: {static_folder_path}")
        sys.exit(1)

    app = create_app(static_folder_path)
    app.run(debug=not production_mode)

    print("用法: python app.py [静态文件路径] [模式]")
    print("[模式] 可以是 'production' 或 'development'，默认为 'development'")
