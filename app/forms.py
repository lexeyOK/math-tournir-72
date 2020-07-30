# Файл, содержащий формы для входа и регистрации

from flask_wtf import FlaskForm
from flask_wtf.file import *
from wtforms import *
from wtforms.validators import *
from config import Constants


# Функция-Валидатор для проверки строки на номер задачи

def is_task_validator(form, field):
    game_type = form.game_type.data
    task = field.data
    if game_type == "domino":
        if task not in Constants.VALID_DOMINO_TASKS_NUMBERS:
            raise ValidationError("Номер задачи не прошёл проверку")
    elif game_type == "penalty":
        if task not in Constants.VALID_PENALTY_TASKS_NUMBERS:
            raise ValidationError("Номер задачи не прошёл проверку")


# Функция-Валидатор для проверки, добавлен ли хотя бы один файл

def at_least_one_file_validator(form, field):
    files = field.data
    raise ValidationError(repr(files))


# Константные валидаторы проверки имени и наличия ввода

IS_NAME_VALIDATOR = [Regexp(regex="^[А-Я+Ё][а-я+ё]+", message="Неверный формат записи")]
DATA_REQUIRED_VALIDATOR = [InputRequired(message="Это поле обязательно для заполения")]
FILE_REQUIRED_VALIDATOR = [FileRequired(message="Нужно отправить этот файл")]
AT_LEAST_ONE_FILE_REQUIRED_VALIDATOR = []
IS_TASK_VALIDATOR = [is_task_validator]
ALL_IMAGES_FILES = [FileAllowed(Constants.ALLOWED_IMAGE_EXTENSIONS, message="Неправильный формат "
                                                                         "файла")]
ALL_TEXT_FILES = [FileAllowed(Constants.ALLOWED_TEXT_EXTENSIONS, message="Неправильный формат файла")]

EMAIL_VALIDATOR = [Email(message="Формат ввода Email неправильный")]

GRADE_CHOICES = [(str(i), str(i)) for i in range(4, 12)]
GAME_TYPE_CHOICES = [("domino", "Домино"), ("penalty", "Пенальти")]
RIGHT_CHOICES = [('checker', 'Проверяющий'), ('author', 'Автор'), ('moderator', 'Модератор'), ('god', "'Бог'")]


# Форма для входа
class LoginForm(FlaskForm):
    login = StringField("Логин", validators=DATA_REQUIRED_VALIDATOR)
    password = PasswordField("Пароль", validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField("Вход")


# Форма для регистрации пользователя с полями логина, пароля, названия команды, выбора класса
class SignUpUserForm(FlaskForm):
    login = StringField("Логин*", validators=DATA_REQUIRED_VALIDATOR)
    password = PasswordField("Пароль*", validators=DATA_REQUIRED_VALIDATOR)
    email = StringField("Email*", validators=DATA_REQUIRED_VALIDATOR + EMAIL_VALIDATOR)
    name = StringField("Имя*", validators=DATA_REQUIRED_VALIDATOR + IS_NAME_VALIDATOR)
    surname = StringField("Фамилия*", validators=DATA_REQUIRED_VALIDATOR + IS_NAME_VALIDATOR)
    grade = SelectField("Класс*",
                        choices=GRADE_CHOICES,
                        coerce=int)
    school = StringField("Школа*", validators=DATA_REQUIRED_VALIDATOR)
    teachers = StringField("Учителя математики и руководители кружков, которые внесли вклад в "
                           "Ваши успехи*",
                           validators=DATA_REQUIRED_VALIDATOR)
    info = StringField("Дополнительная информация о Вас (как с Вами можно связаться, "
                       "что Вы хотите рассказать о себе)")
    submit = SubmitField("Зарегистрироваться")


# Форма для забывчивых
class ForgotPassword(FlaskForm):
    email = StringField("Email", validators=DATA_REQUIRED_VALIDATOR + EMAIL_VALIDATOR)
    submit = SubmitField("Восстановить пароль")


# Форма для добавления задачи в архив
class AddTaskForm(FlaskForm):
    min_grade = SelectField("Самый младший рекомендуемый класс", default='5',
                            choices=GRADE_CHOICES)
    max_grade = SelectField("Самый старший рекомендуемый класс", default='5',
                            choices=GRADE_CHOICES)
    condition_file = FileField("*.txt файл с условием", validators=FILE_REQUIRED_VALIDATOR)
    condition_images = MultipleFileField("Файлы иллюстраций к условию (допустимы файлы "
                                         "*.png/*.jpg/*.jpeg/*.gif)",
                                         validators=ALL_IMAGES_FILES)
    solution_file = FileField("*.txt файл с решением", validators=ALL_TEXT_FILES)
    solution_images = MultipleFileField("Файлы иллюстраций к решению (допустимы файлы "
                                        "*.png/*.jpg/*.jpeg/*.gif)",
                                        validators=ALL_IMAGES_FILES)
    answer = StringField("Ответ", validators=DATA_REQUIRED_VALIDATOR)
    manual_check = BooleanField("Задача проверяется вручную")
    ans_picture = BooleanField("Ответом является рисунок (тогда задача проверяется вручную)")
    submit = SubmitField("Добавить задачу")


# Чтобы выбрать класс и тип игры
class GradeGameForm(FlaskForm):
    grade = RadioField("Выберите класс", choices=GRADE_CHOICES,
                       validators=DATA_REQUIRED_VALIDATOR)
    game = RadioField("Выберите игру", choices=GAME_TYPE_CHOICES)
    submit = SubmitField("Перейти")


# Форма для заполнения общей информации о игре
class GameCommonInfoForm(FlaskForm):
    title = StringField('Название игры', validators=DATA_REQUIRED_VALIDATOR)
    info = TextAreaField('Описание игры', validators=DATA_REQUIRED_VALIDATOR)
    grade = SelectField('Класс', choices=GRADE_CHOICES, coerce=str)
    game_type = SelectField('Тип игры', choices=Constants.GAMES_DICT, coerce=str)
    start_time = StringField('Время начала', validators=DATA_REQUIRED_VALIDATOR)
    end_time = StringField('Время конца', validators=DATA_REQUIRED_VALIDATOR)
    game_format = SelectField('Формат игры', choices=[('personal', 'личная'), ('team', 'командная')])
    privacy = SelectField('Приватность игры', choices=[('private', 'закрытая'), ('open', 'открытая')])
    submit = SubmitField("Создать/изменить игру")


# Форма для заполнения информации о блоке задач
class GameTasksInfoForm(FlaskForm):
    tasks_number = IntegerField('Количество задач', validators=DATA_REQUIRED_VALIDATOR)
    sets_number = IntegerField('Количество наборов задач', validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField('Подтвердить изменения')


# Форма для заполнения информации о размере команд
class GameTeamInfoForm(FlaskForm):
    min_team_size = IntegerField('Максимальный размер команды', validators=DATA_REQUIRED_VALIDATOR)
    max_team_size = IntegerField('Минимальный размер команды', validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField('Подтвердить изменения')


# Форма для заполнения информации о авторах и проверяющих
class GameAuthorsAndCheckersInfoForm(FlaskForm):
    authors = StringField('Имена и Фамилии авторов через пробел')
    checkers = StringField('Имена и Фамилии проверяющих через пробел')
    submit = SubmitField('Подтвердить изменения')


# Форма для выбора начала и конца соревнования
class StartEndTimeForm(FlaskForm):
    game_type = SelectField("Тип игры", choices=[("domino", "Домино"), ("penalty", "Пенальти")],
                            validators=DATA_REQUIRED_VALIDATOR)
    time_start = DateTimeField("Начало игры (в формате дд.мм.гггг чч:мм:сс)", format="%d.%m.%Y %H:%M:%S",
                               validators=DATA_REQUIRED_VALIDATOR)
    time_end = DateTimeField("Конец игры (в формате дд.мм.гггг чч:мм:сс)", format="%d.%m.%Y %H:%M:%S",
                             validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField("Установить время начала и конца")


# Форма для бана пользователя
class BanForm(FlaskForm):
    name = StringField('Имя', validators=DATA_REQUIRED_VALIDATOR)
    surname = StringField('Фамилия', validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField('Заблокировать пользователя')


# Форма для пардона пользователя
class PardonForm(FlaskForm):
    name = StringField('Имя', validators=DATA_REQUIRED_VALIDATOR)
    surname = StringField('Фамилия', validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField('Разблокировать пользователя')


# Форма для выдачи прав
class GiveRightForm(FlaskForm):
    name = StringField("Имя", validators=DATA_REQUIRED_VALIDATOR)
    surname = StringField("Фамилия", validators=DATA_REQUIRED_VALIDATOR)
    right = SelectField("Выберите набор прав, который хотите выдать", RIGHT_CHOICES)
    submit = SubmitField("Выдать набор прав")


class MakeNewForm(FlaskForm):
    picture = FileField("Изображение к новости(допустимы файлы *.png/*.jpg/*.jpeg/*.gif)", validators=ALL_IMAGES_FILES)
    title = StringField("Название", validators=DATA_REQUIRED_VALIDATOR)
    info = StringField("Содержание новости", validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField("Опубликовать новость")


class UpdateNewForm(FlaskForm):
    picture = FileField("Изображение к новости(допустимы файлы *.png/*.jpg/*.jpeg/*.gif)", validators=ALL_IMAGES_FILES)
    title = StringField("Название", validators=DATA_REQUIRED_VALIDATOR)
    info = StringField("Содержание новости", validators=DATA_REQUIRED_VALIDATOR)
    submit = SubmitField("Опубликовать новость")



''' ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ '''


def get_extension(filename):
    if '.' not in filename:
        return ""

    return filename.rsplit('.', 1)[1].lower()
