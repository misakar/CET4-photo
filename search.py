# coding: utf-8

"""
    search.py
    ~~~~~~~~

        CET4 search engine: search your friend's photo
"""

from flask import Flask, render_template, redirect, url_for, session
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import sys


# 设置编码
reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'I like CET4'


class NameForm(Form):
    """搜索表单"""
    name = StringField('name', validators=[Required()])
    submit = SubmitField('search')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """查询姓名，获取学号，根据学号获取图片"""
    # open stuinfo.txt file
    form = NameForm()
    # session['stuphoto'] = "http://7xj431.com1.z0.glb.clouddn.com/0eb30f2442a7d9331abfc6f3ad4bd11373f0011e.jpg.png"
    # session['stuphoto'] = "http://cet.tinyin.net/photos/2014210761.jpg"
    if form.validate_on_submit():
        # 表单查询
        name = form.name.data.decode('utf-8')
        info = open("stuinfo.txt", 'r+')
        info_list = info.readlines()
        for line in info_list:
            if name in line:
                stuno = line[15:25]
                stuphoto = "http://cet.tinyin.net/photos/%s.jpg" % stuno
                session['stuphoto'] = stuphoto
                break
        else:
            session['stuphoto']="http://cet.tinyin.net/photos/2014210761.jpg"
        info.close()
        return redirect(url_for('search'))

    return render_template('index.html', form=form, session=session)


if __name__ == "__main__":
    app.run(debug=True)
