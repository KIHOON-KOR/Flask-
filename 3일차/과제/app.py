from flask import Flask 
from flask_smorest import Api 
from flask_sqlalchemy import SQLAlchemy 
from db import db
# 프로젝트의 db.py 안에 정의된 db = SQLAlchemy() 객체를 가져옴.
from models import User, Board
#모델 클래스를 미리 임포트해서 create_all() 호출 시 테이블 메타데이터가 등록되도록 함.

app = Flask(__name__) # Flask 애플리케이션 인스턴스 생성.
# app.config[...]에 DB/Swagger 설정을 채운다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:000112@127.0.0.1/oz'
# DB 연결 문자열 설정. MySQL + PyMySQL 드라이버 사용.(oz라는 데이터베이스는 미리 만들어져 있어야 함.)
# SQLALCHEMY_DATABASE_URI: DB 접속 주소(어디 DB 쓸지).
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLALCHEMY_TRACK_MODIFICATIONS: 불필요 기능 끄기.
db.init_app(app)
#위에서 가져온 db 객체를 이 app과 연결. (애플리케이션 컨텍스트가 생기면 세션/엔진 사용 가능)

# bluepring 설정 및 등록
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
#Swagger UI 자동 생성
app.config["OPENAPI_VERSION"] = "3.1.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

from routes.user import user_blp
from routes.board import board_blp
# 각 엔드포인트를 묶은 Smorest Blueprint들을 임포트.

api = Api(app) # Api(app) 생성
api.register_blueprint(user_blp)
api.register_blueprint(board_blp)
# 이 순간부터 /users/..., /boards/... 경로가 살아남.

from flask import render_template
@app.route('/manage-boards')
def manage_boards():
    return render_template('boards.html')
# /manage-boards 요청 시 templates/boards.html을 렌더링.

@app.route('/manage-users')
def manage_users():
    return render_template('users.html')

if __name__ == '__main__':
# 이 파일을 직접 실행할 때만 아래 블록을 수행(모듈로 임포트될 때는 실행 안 함).
    with app.app_context():
# 애플리케이션 컨텍스트를 수동으로 푸시하고 모든 모델 테이블을 생성.
        print("여기 실행?")
        db.create_all()
    app.run(debug=True)