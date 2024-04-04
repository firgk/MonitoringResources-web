from flask import *
from threading import*
from func import *
app = Flask(__name__,static_folder="", template_folder="")

@app.route('/')
def index():
    # 获取图片文件夹中的文件列表
    content=display_system_resources()
    # 在index.html后添加传入的参数
    return render_template('index.html',content=content.split('\n'))


if __name__ == '__main__':
    app.run(debug=True)
