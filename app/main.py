from app import app
import routes
from posts.blueprints import posts



app.register_blueprint(posts)

if __name__ == '__main__':
    app.run()