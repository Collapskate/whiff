from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, request
from data import db_session
from wtforms.fields.html5 import EmailField
from data.users import User
import flask_login
from flask import Flask, jsonify
from flask_login import LoginManager, login_required, current_user
from flask_login import login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


#Главная страница
@app.route('/')
def hom():
    return render_template('new.html', title='w h i f f .')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/home")


#Музеи
@app.route('/ermitag')
def ermi():
    return render_template('Ermitag.html')


@app.route('/msiid')
def msiid():
    return render_template('Rostov.html')


@app.route('/tret')
def tret():
    return render_template('Tretiakovka.html')


@app.route('/sarat')
def sara():
    return render_template('Saratov.html')


#Картины Третьяковки
@app.route('/t1')
def t1():
    return render_template('t1.html')


@app.route('/t2')
def t2():
    return render_template('t2.html')


@app.route('/t3')
def t3():
    return render_template('t3.html')


@app.route('/t4')
def t4():
    return render_template('t4.html')


@app.route('/t5')
def t5():
    return render_template('t5.html')


#Картины музея в Саратове
@app.route('/s1')
def s1():
    return render_template('s1.html')


@app.route('/s2')
def s2():
    return render_template('s2.html')


@app.route('/s3')
def s3():
    return render_template('s3.html')


@app.route('/s4')
def s4():
    return render_template('s4.html')


#Картины Ростовского музея
@app.route('/r1')
def r1():
    return render_template('r1.html')


@app.route('/r2')
def r2():
    return render_template('r2.html')


@app.route('/r3')
def r3():
    return render_template('r3.html')


@app.route('/r4')
def r4():
    return render_template('r4.html')


#Картины Эрмитажа
@app.route('/e1')
def e1():
    return render_template('e1.html')


@app.route('/e2')
def e2():
    return render_template('e2.html')


@app.route('/e3')
def e3():
    return render_template('e3.html')


@app.route('/e4')
def e4():
    return render_template('e4.html')


#РАБОТА С РЕГИСТРАЦИЕЙ И ВХОДОМ В АККАУНТ
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе(Понравившиеся работы художников, избранные музеи, любимые деятели искусства)")
    submit = SubmitField('Зарегистрировать')


#Личный кабинет
@app.route('/private_office/<user>')
def lk(user):
    if current_user.is_authenticated:
        return render_template('private_office.html', username=current_user.name, about=current_user.about)
    else:
        return redirect('/login')


def user(username=None):
    if request.method == 'POST':
        if request.form['logout'] == 'Logout':
            login.logout(username)
            return redirect(url_for('/home'))
    else:
        flash(authenticationError)
    return redirect(url_for('/home'))


#Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/private_office/{user.name}")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


#Регистрация
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


text = """г.Санкт-Петербург, Дворцовая набережная, 34 Государственный Эрмитаж Более 250 лет назад Екатерина II в 
Малом Эрмитаже пожелала иметь уголок для уединения. Годом создания музея считается 1764 г., когда разорившийся 
немецкий купец был вынужден погасить свой долг. Не имея наличных средств, он расплатился коллекцией из 225 полотен 
знаменитых художников. Эти картины украсили стены Малого Эрмитажа. До 1852 года, когда экспозиции были открыты для 
широкой публики, посмотреть на произведения искусств могли только «сливки» аристократического общества. Сегодня 
коллекция Эрмитажа включает в себя более 3 млн. экспонатов, которые представлены полотнами, скульптурами, предметами 
декоративно-прикладного искусства и другими памятниками культуры. Некоторых из них относятся к каменному веку. 

г.Москва, Лаврушинский переулок Третьяковская галерея Государственная Третьяковская галерея – крупнейший музей 
русского искусства, имеющий мировую известность. Галерея названа по имени московского купца и промышленника Павла 
Михайловича Третьякова (1832–1898), коллекционировавшего с 1856 произведения современных ему художников, 
желая «собрать русскую школу как она есть в последовательном своем ходе». 

г.Саратов, ул. имени А.Н. Радищева, 39 Саратовский государственный художественный музей им. А.Н. Радищева Cаратовский 
государственный художественный музей имени А.Н. Радищева принадлежит к числу самых крупных и старейших в стране. 
Основанный в 1885 году, он на протяжении долгих лет являлся одним из немногих общедоступных художественных собраний в 
дореволюционной России. 

г.Ростов-на-Дону, ул. Шаумяна, 51 Музей Современного Изобразительного Искусства на Дмитровской (МСИИД) МСИИД строит 
свою работу на основных принципах музееведческой практики: коллекционирование, хранение и экспонирование. Свою 
историческую и культурную миссию музей видит в формировании и пропаганде коллекции, как мастеров прошлого ХХ века, 
так и художников наступившего ХХI. Фонды музея насчитывают более 1800 произведений, преимущественно живописи и 
графики c 1930 года по сегодняшний день. """


@app.route('/api')
def get_api():
    return jsonify(text)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, host='0.0.0.0')
