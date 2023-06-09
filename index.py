import os

from dotenv import load_dotenv
import discord
from utils.db_utils import *
from datetime import datetime, date

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

client = discord.Client(intents=intents)
db_session = create_dbsession()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('!помоги'):
        await message.author.send('Список команд:\n- !список_сотрудников: без параметров'
                                  '\n- !создать-отдел: [Название отдела]'
                                  '\n- !список-отделов: без параметров'
                                  '\n- !обновить-отдел: [Название отдела][Новое название отдела]'
                                  '\n- !добавить-роль-отделу: [Название отдела][Название роли отдела]'
                                  '\n- !создать-роль: [Название роли]'
                                  '\n- !список-ролей: без параметров'
                                  '\n- !обновить-роль: [Название роли][Новое название роли]'
                                  '\n- !роли-отдела: без параметров'
                                  '\n- !снять-роль-отдела: [Название отдела][Название роли]'
                                  '\n- !удалить-отдел: [Название отдела]'
                                  '\n- !удалить-роль: [Название роли]'
                                  '\n- !все-задачи: без параметров'
                                  '\n- !создать-задачу: О[Заголовок задачи]Н[Описание задачи]О[Тип задачи: Личная, Назначенная, Отдел, Публичная]О/Н[Получатель]Н[Дата начала]Н[Дата окончания] (Заполнять через shift + enter)'
                                  '\n- !обновить-название-задачи: [Номер задачи] [Новое название задачи]'
                                  '\n- !обновить-описание-задачи: [Номер задачи] [Новое описание задачи]'
                                  '\n- !обновить-получателя-задачи: [Номер задачи] [Новый тип задачи: Личная, Назначенная, Отдел, Публичная] [Наименование получателя]'
                                  '\n- !обновить-начало-задачи: [Номер задачи] [Дата начала]'
                                  '\n- !обновить-конец-задачи: [Номер задачи] [Дата конца]'
                                  '\n- !мои-задачи-на-сегодня: без параметров'
                                  '\n- !задачи-статус: [Статус задачи: Не взята, В работе, Готов к тестированию, Тестирование, Переделать, Завершена, Заморожена]'
                                  '\n- !мои-задачи: без параметров'
                                  '\n- !задачи-пользователя: [Имя пользователя]'
                                  '\n- !задачи-отдела: [Название отдела]'
                                  '\n- !общие-задачи: без параметров'
                                  '\n- !просроченный-задачи: без параметров'
                                  '\n- !мои-просроченные-задачи: без параметров'
                                  '\n- !обновить-статус-задачи: [Номер задачи] [Статус задачи: Не взята, В работе, Готов к тестированию, Тестирование, Переделать, Завершена, Заморожена]'
                                  '\n- !задача: [Номер задачи]'
                                  )

    elif message.content.startswith('!список_сотрудников'):
        mes = 'Наши сотрудники:\n'
        for member in message.guild.members:
            mes += '\n- ' + member.name
        await message.reply(mes)

    elif message.content.startswith('!создать-отдел'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название отдела!")
            return
        elif (len(params) > 2):
            await message.author.send("Вы ввели больше 1 параметра (между словами нужен символ \'-\' !")
            return
        department = db_session.query(Department).filter_by(name=params[1]).first()
        if (department is not None):
            await message.author.send(f"Отдел с таким названием уже существует, № отдела: {department.id}.")
            return
        else:
            newDepartment = Department()
            newDepartment.name = params[1]
            db_session.add(newDepartment)
            db_session.commit()
            await message.author.send("Отдел создан!")

    elif message.content.startswith('!список-отделов'):
        departments = db_session.query(Department).order_by(Department.id.desc())
        mes = "Список отделов:\n"
        if (departments.count() == 0):
            await message.author.send("Отделов пока нет.")
            return
        for department in departments:
            mes += f"- №{department.id} {department.name}\n"
        await message.author.send(mes)

    elif message.content.startswith('!обновить-отдел'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели старое и новое название отдела!")
            return
        if (len(params) == 2):
            await message.author.send("Вы не ввели новое название отдела!")
            return
        elif (len(params) > 3):
            await message.author.send("Вы ввели больше 2-x параметров (между словами нужен символ \'-\')!")
            return
        department = db_session.query(Department).filter_by(name=params[1]).first()
        if department is None:
            await message.author.send(f"Отдела с названием {params[1]} не существует!")
            return
        department.name = params[2]
        db_session.add(department)
        db_session.commit()
        await message.author.send("Название отдела обновлено.")

    elif message.content.startswith('!добавить-роль-отделу'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название отдела и название роли!")
            return
        if (len(params) == 2):
            await message.author.send("Вы не ввели название роли!")
            return
        if (len(params) > 3):
            await message.author.send("Вы ввели больше 2-x параметров (между словами нужен символ \'-\')!")
            return
        department = db_session.query(Department).filter_by(name=params[1]).first()
        if (department is None):
            await message.author.send(f"Отдел с таким названием не существует!")
            return
        role = db_session.query(Role).filter_by(name=params[2]).first()
        if (role is None):
            await message.author.send(f"Роль с таким названием не существует!")
            return

        departmentRole = db_session.query(DepartmentRole).filter_by(department_id=department.id, role_id=role.id).first()
        if (departmentRole is not None):
            await message.author.send(f"Эта роль уже есть у отдела!")
            return

        departmentRole = DepartmentRole()
        departmentRole.department_id = department.id
        departmentRole.role_id = role.id
        db_session.add(departmentRole)
        db_session.commit()
        await message.author.send(f"Отделу №{department.id} добавлена новая роль: {role.name}.")

    elif message.content.startswith('!создать-роль'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название роли!")
            return
        if (len(params) > 2):
            await message.author.send("Вы вввели более 1 параметра (между словами нужен символ \'-\')!")
            return
        role = db_session.query(Role).filter_by(name=params[1]).first()
        if (role is not None):
            await message.author.send(f"Роль с таким названием уже существует, № роли: {role.id}.")
            return
        else:
            role = Role()
            role.name = params[1]
            db_session.add(role)
            db_session.commit()
            await message.author.send("Добавбена новая роль.")

    elif message.content.startswith('!список-ролей'):
        params = message.content.split(' ')
        if (len(params) > 1):
            await message.author.send("Для получения списка ролей не нужны параметры!")
            return
        roles = db_session.query(Role).order_by(Role.id.desc())
        mes = "Список ролей:\n"
        if (roles.count() == 0):
            await message.author.send("Ролей пока нет.")
            return
        for role in roles:
            mes += f"- №{role.id} {role.name}\n"
        await message.author.send(mes)

    elif message.content.startswith('!обновить-роль'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели старое и новое название роли!")
            return
        if (len(params) == 2):
            await message.author.send("Вы не ввели новое название роли!")
            return
        elif (len(params) > 3):
            await message.author.send("Вы ввели больше 2-x параметров (между словами нужен символ \'-\')!")
            return
        role = db_session.query(Role).filter_by(name=params[1]).first()
        if role is None:
            await message.author.send(f"Отдела с названием {params[1]} не существует!")
            return
        role.name = params[2]
        db_session.add(role)
        db_session.commit()
        await message.author.send("Название роли обновлено.")

    elif message.content.startswith('!роли-отдела'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название отдела!")
            return
        if (len(params) > 2):
            await message.author.send("Вы ввели больше 1 параметра (между словами нужен символ \'-\')!")
            return
        department = db_session.query(Department).filter_by(name=params[1]).first()
        if (department is None):
            await message.author.send(f"Отдел с таким названием не существует!")
            return

        departmentRoles = db_session.query(DepartmentRole).filter_by(department_id=department.id).order_by(DepartmentRole.role_id.asc())
        if (departmentRoles.count() == 0):
            await message.author.send(f"Ролей у отдела №{department.id} \'{department.name}\' - пока нет.")
            return

        mes = f"Список ролей отдела №{department.id} \'{department.name}\':\n"

        for departmentRole in departmentRoles:
            role = db_session.query(Role).filter_by(id=departmentRole.role_id).first()
            mes += f"- №{role.id} {role.name}\n"

        await message.author.send(mes)

    elif message.content.startswith('!снять-роль-отдела'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название отдела и назавние роли!")
            return
        if (len(params) == 2):
            await message.author.send("Вы не ввели название роли!")
            return
        if (len(params) > 3):
            await message.author.send("Вы ввели больше 1 параметра (между словами нужен символ \'-\')!")
            return

        department = db_session.query(Department).filter_by(name=params[1]).first()
        if (department is None):
            await message.author.send(f"Отдел с таким названием не существует!")
            return

        role = db_session.query(Role).filter_by(name=params[2]).first()
        if (role is None):
            await message.author.send(f"Роль с таким названием не существует!")
            return

        departmentRoles = db_session.query(DepartmentRole).filter_by(department_id=department.id, role_id=role.id).first()
        if (departmentRoles is None):
            await message.author.send("Невозможно снаять эту роль, так как ее нет у отдела.")
            return

        db_session.delete(departmentRoles)
        db_session.commit()

        await message.author.send(f'Роль \'{role.name}\' у отдела \'{department.name}\' - успешно снята!')

    elif message.content.startswith('!удалить-отдел'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название отдела!")
            return
        if (len(params) > 3):
            await message.author.send("Вы ввели больше 1 параметра (между словами нужен символ \'-\')!")
            return

        department = db_session.query(Department).filter_by(name=params[1]).first()
        if (department is None):
            await message.author.send(f"Отдел с таким названием не существует!")
            return

        departmentRoles = db_session.query(DepartmentRole).filter_by(department_id=department.id)
        for departmentRole in departmentRoles:
            findDepartmentRole = db_session.query(DepartmentRole).filter_by(department_id=departmentRole.department_id, role_id=departmentRole.role_id).first()
            db_session.delete(findDepartmentRole)

        db_session.delete(department)
        db_session.commit()

        await message.author.send(f'Отдел №{department.id} \'{department.name}\' - успешно удален!')

    elif message.content.startswith('!удалить-роль'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название роли!")
            return
        if (len(params) > 3):
            await message.author.send("Вы ввели больше 1 параметра (между словами нужен символ \'-\')!")
            return

        role = db_session.query(Role).filter_by(name=params[1]).first()
        if role is None:
            await message.author.send("Роли с таким названием нет!")
            return

        departmentRoles = db_session.query(DepartmentRole).filter_by(role_id=role.id)

        for departmentRole in departmentRoles:
            findDepartmentRole = db_session.query(DepartmentRole).filter_by(department_id=departmentRole.department_id, role_id=departmentRole.role_id).first()
            db_session.delete(findDepartmentRole)

        db_session.delete(role)
        db_session.commit()

        await message.author.send(f'Роль №{role.id} \'{role.name}\' - успешно удалена!')

    elif message.content.startswith('!все-задачи'):
        params = message.content.split(' ')
        if (len(params) > 2):
            await message.author.send("Вы ввели больше 1 параметра (параметр отвечает за номер страницы)!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 1:
            if int(params[1]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[1])

        offset = (page_number - 1) * page_size

        query = db_session.query(Note)
        total_count = query.count()

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Задач пока что нет.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Общий список задач:\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!все-задачи []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!создать-задачу'):
        params = message.content.split('\n')
        if (len(params[1]) == 0):
            await message.author.send('Минимальная длина названия задачи 1 символ!')
            return
        if (len(params[3]) == 0):
            await message.author.send('Минимальная длина типа задачи 1 символ!')
            return
        newNote = Note()
        newNote.title = params[1]
        newNote.description = params[2]
        taskType = db_session.query(NoteType).filter_by(name=params[3]).first()
        newNote.type = taskType.id
        if taskType is None:
            await message.author.send('Такого типа задачи не существует!')
            return

        if taskType.name == "Личная" or taskType.name == "Публичная":
            newNote.recipient = ""
        elif taskType.name == "Отдел":
            department = db_session.query(Department).filter_by(name=params[4]).first()
            if department is None:
                await message.author.send(f'Отдел {params[4]} не существует!')
                return
            newNote.recipient = department.name
        else:
            if len(params[4]) < 1:
                await message.author.send(f'Длина имени пользователя дожна быть больше 0!')
                return
            else:
                newNote.recipient = params[4]
        if len(params) > 5:
            if len(params[5]) == 10:
                try:
                    date_obj = datetime.strptime(params[5], '%d.%m.%Y')
                    newNote.date_start = date_obj.date()
                except ValueError:
                    await message.author.send('Неверный формат начальной даты!')
                    return
            elif len(params[5]) == 16:
                try:
                    datetime_obj = datetime.strptime(params[5], '%d.%m.%Y %H:%M')
                    newNote.date_start = datetime_obj.strftime('%d.%m.%Y %H:%M')
                except ValueError:
                    await message.author.send('Неверный формат начальной даты!')
                    return
            elif len(params[5]) == 0:
                pass
            else:
                await message.author.send('Неверный формат начальной даты!')
                return


        if len(params) > 6:
            if len(params[6]) == 10:
                try:
                    date_obj = datetime.strptime(params[6], '%d.%m.%Y')
                    newNote.date_end = date_obj.date()
                except ValueError:
                    await message.author.send('Неверный формат конечной даты!')
                    return
            elif len(params[6]) == 16:
                try:
                    datetime_obj = datetime.strptime(params[6], '%d.%m.%Y %H:%M')
                    newNote.date_end = datetime_obj.strftime('%d.%m.%Y %H:%M')
                except ValueError:
                    await message.author.send('Неверный формат конечной даты!')
                    return
            elif len(params[6]) == 0:
                pass
            else:
                await message.author.send('Неверный формат конечной даты!')
                return

        newNote.status = 1
        db_session.add(newNote)
        db_session.commit()
        await message.author.send('Задача - успешно создана!')

    elif message.content.startswith('!обновить-название-задачи'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели номер задачи и новое название задачи!")
            return

        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        if (len(params) == 2):
            await message.author.send("Вы не ввели новое название задачи!")
            return
        elif (len(params) > 3):
            await message.author.send("Вы ввели больше 2-x параметров (между словами нужен символ \'-\')!")
            return
        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send(f"Не существует задачи с №{params[1]}!")
            return
        note.title = params[2]
        note.date_update = datetime.now()
        db_session.add(note)
        db_session.commit()
        await message.author.send("Название задачи изменено.")

    elif message.content.startswith('!обновить-описание-задачи'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели номер задачи и новое описание задачи!")
            return

        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        if (len(params) == 2):
            await message.author.send("Вы не ввели новое описание задачи!")
            return
        elif (len(params) > 3):
            await message.author.send("Вы ввели больше 2-x параметров (между словами нужен символ \'-\')!")
            return
        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send(f"Не существует задачи с №{params[1]}!")
            return
        note.description = params[2]
        note.date_update = datetime.now()
        db_session.add(note)
        db_session.commit()
        await message.author.send("Описание задачи изменено.")

    elif message.content.startswith('!обновить-получателя-задачи'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели номер задачи, тип задачи и нового получателя!")
            return

        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        if (len(params) == 2):
            await message.author.send("Вы не ввели тип задачи!")
            return

        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send("Задачи с таким номером нет.")
            return


        taskType = db_session.query(NoteType).filter_by(name=params[2]).first()
        if taskType is None:
            await message.author.send('Такого типа задачи не существует!')
            return
        else:
            note.status = taskType.id
            if taskType.name == "Личная" or taskType.name == "Публичная":
                if taskType.name == "Личная":
                    note.recipient = message.author.name
                else:
                    note.recipient = ''
            elif len(params) == 4 and len(params[3]) == 1:
                await message.author.send("Длина получателя минимум 1 символ!")
                return
            elif len(params) == 4 and taskType.name == "Отдел":
                if (len(params) == 3):
                    await message.author.send("Вы не ввели название отдела!")
                    return
                department = db_session.query(Department).filter_by(name=params[3]).first()
                if department is None:
                    await message.author.send(f'Отдел \'{params[3]}\' не существует!')
                    return
                note.recipient = params[3]
            else:
                if (len(params) == 3):
                    await message.author.send("Вы не ввели имя получателя!")
                    return
                note.recipient = params[3]

        if (len(params) > 4):
            await message.author.send("Вы ввели больше 3-x параметров (между словами нужен символ \'-\')!")
            return


        note.date_update = datetime.now()

        db_session.add(note)
        db_session.commit()

        if taskType.name == 'Личная':
            await message.author.send(f"Задача №{params[1]} была назначена на вас!")
        elif taskType.name == 'Назначенная':
            await message.author.send(f"Задача №{params[1]} была назначена на пользователя \'{params[3]}\'!")
        elif taskType.name == 'Отдел':
            await message.author.send(f"Задача №{params[1]} была назначена на отдел \'{params[3]}\'!")
        else:
            await message.author.send(f"Задача №{params[1]} была назначена на всех!")

    elif message.content.startswith('!обновить-начало-задачи'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели номер задачи и время начала!")
            return

        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        if (len(params) == 2):
            await message.author.send("Вы не ввели время начала!")
            return
        if len(params) > 4:
            await message.author.send("Вы ввели больше 3-x параметров (между словами нужен символ \'-\')!")
            return

        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send(f"Нет задачи с №{params[1]}!")
            return

        if len(params) == 3 and len(params[2]) == 10:
            try:
                date_obj = datetime.strptime(params[2], '%d.%m.%Y')
                note.date_start = date_obj.date()
            except ValueError:
                await message.author.send('Неверный формат начальной даты!')
                return
        elif len(params[2] + ' ' + params[3]) == 16:
            try:
                datetime_obj = datetime.strptime(params[2] + ' ' + params[3], '%d.%m.%Y %H:%M')
                note.date_start = datetime_obj.strftime('%d.%m.%Y %H:%M')
            except ValueError:
                await message.author.send('Неверный формат начальной даты!')
                return
        else:
            await message.author.send('Неверный формат начальной даты!')
            return

        note.date_update = datetime.now()

        db_session.add(note)
        db_session.commit()

        await message.author.send(f'Обновлено начало задачи №{params[1]}!')

    elif message.content.startswith('!обновить-конец-задачи'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели номер задачи и время конца!")
            return

        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        if (len(params) == 2):
            await message.author.send("Вы не ввели конца начала!")
            return
        if len(params) > 4:
            await message.author.send("Вы ввели больше 2-x параметров (между словами нужен символ \'-\')!")
            return

        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send(f"Нет задачи с №{params[1]}!")
            return

        if len(params) == 3 and len(params[2]) == 10:
            try:
                date_obj = datetime.strptime(params[2], '%d.%m.%Y')
                note.date_end = date_obj.date()
            except ValueError:
                await message.author.send('Неверный формат конечной даты!')
                return
        elif len(params[2] + ' ' + params[3]) == 16:
            try:
                datetime_obj = datetime.strptime(params[2] + ' ' + params[3], '%d.%m.%Y %H:%M')
                note.date_end = datetime_obj.strftime('%d.%m.%Y %H:%M')
            except ValueError:
                await message.author.send('Неверный формат конечной даты!')
                return
        else:
            await message.author.send('Неверный формат конечной даты!')
            return

        note.date_update = datetime.now()

        db_session.add(note)
        db_session.commit()

        await message.author.send(f'Обновлен конец задачи №{params[1]}!')

    elif message.content.startswith('!удалить-задачу'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели номер задачи!")
            return

        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        if (len(params) > 2):
            await message.author.send("Вы ввели больше 1 параметра (между словами нужен символ \'-\')!")
            return

        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send(f"Нет задачи с №{params[1]}!")
            return

        db_session.delete(note)
        db_session.commit()

        await message.author.send(f"Задача №{params[1]} - удалена!")

    elif message.content.startswith('!мои-задачи-на-сегодня'):
        params = message.content.split(' ')
        if (len(params) > 2):
            await message.author.send("Вы указали более 2-х параметров!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 1:
            if int(params[1]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[1])

        offset = (page_number - 1) * page_size
        today = date.today()
        query = db_session.query(Note).filter(
            Note.recipient == message.author.name,
            Note.date_start >= datetime.combine(today, datetime.min.time()),
            Note.date_start < datetime.combine(today, datetime.max.time())
        )

        total_count = len(query.all())

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Для вас задач на сегодня пока что нет.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Мой список задач на сегодня:\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!мои-задачи []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!задачи-статус'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не указали статус задачи!")
            return

        statusName = ''

        for i in range(2, len(params)):
            statusName += params[i]
            if (i < len(params)-1):
                statusName += ' '

        status = db_session.query(NoteStatus).filter_by(name=statusName).first()

        if status is None:
            await message.author.send(f"Такого статуса нет (\'{statusName}\')!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 1:
            if int(params[1]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[1])

        offset = (page_number - 1) * page_size

        query = db_session.query(Note).filter(
            Note.status == status.id
        )

        total_count = len(query.all())

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Задач со статусом \'{status.name}\' пока что нет.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Задачи со статусом \'{status.name}\':\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!задачи-статус [] [статус]\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!мои-задачи'):
        params = message.content.split(' ')
        if (len(params) > 2):
            await message.author.send("Вы указали более 2-х параметров!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 1:
            if int(params[1]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[1])

        offset = (page_number - 1) * page_size

        query = db_session.query(Note).filter_by(recipient=message.author.name)
        total_count = query.count()

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Для вас задач пока что нет.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Мой список задач:\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!мои-задачи []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!задачи-пользователя'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели имя пользователя!")
            return
        if (len(params) > 3):
            await message.author.send("Вы ввели больше 2-ч параметров (параметр отвечает за номер страницы)!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 2:
            if int(params[2]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[2])

        offset = (page_number - 1) * page_size

        query = db_session.query(Note).filter_by(recipient=params[1], type=2)
        total_count = query.count()

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Для пользователя \'{params[1]}\' задач пока что нет.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Список задач пользователя \'{params[1]}\':\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!задачи-пользователя []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!задачи-отдела'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели название отдела!")
            return
        if (len(params) > 3):
            await message.author.send("Вы ввели больше 2 параметра (параметр отвечает за номер страницы)!")
            return

        department = db_session.query(Department).filter_by(name=params[1]).first()
        if department is None:
            await message.author.send(f"Нет отдела с названием \'{params[1]}\'!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 2:
            if int(params[2]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[2])

        offset = (page_number - 1) * page_size

        query = db_session.query(Note).filter_by(recipient=params[1], type=3)
        total_count = query.count()

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Для отдела \'{params[1]}\' задач пока что нет.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Список задач отдела \'{params[1]}\':\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!задачи-отдела []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!общие-задачи'):
        params = message.content.split(' ')
        if (len(params) > 2):
            await message.author.send("Вы указали более 2-х параметров!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 1:
            if int(params[1]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[1])

        offset = (page_number - 1) * page_size

        query = db_session.query(Note).filter_by(type=4)
        total_count = query.count()

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Общих задач пока что нет.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Список общих задач:\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!общие-задачи []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!просроченный-задачи'):
        params = message.content.split(' ')
        if (len(params) > 2):
            await message.author.send("Вы указали более 2-х параметров!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 1:
            if int(params[1]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[1])

        offset = (page_number - 1) * page_size
        today = date.today()
        query = db_session.query(Note).filter(
            Note.status != 6 or Note.status != 7,
            Note.date_end < datetime.combine(today, datetime.min.time())
        )

        total_count = len(query.all())

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Просроченный задачи отсутствуют.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Просроченные задачи:\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!просроченный-задачи []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!мои-просроченные-задачи'):
        params = message.content.split(' ')
        if (len(params) > 2):
            await message.author.send("Вы указали более 2-х параметров!")
            return

        page_size = 10
        page_number = 1

        if len(params) > 1:
            if int(params[1]) < 1:
                await message.author.send("Параметр страницы не может быть меньше 1!")
                return
            page_number = int(params[1])

        offset = (page_number - 1) * page_size
        today = date.today()
        query = db_session.query(Note).filter(
            Note.recipient == message.author.name,
            Note.status != 6 or Note.status != 7,
            Note.date_end < datetime.combine(today, datetime.min.time())
        )

        total_count = len(query.all())

        total_pages = (total_count + page_size - 1) // page_size

        if total_count == 0:
            await message.author.send(f"Мои просроченный задачи отсутствуют.")
            return

        if page_number > total_pages:
            await message.author.send(f"Страницы с номером {page_number} не существует!\nВсего странц: {total_pages}.")
            return

        result = query.offset(offset).limit(page_size).all()

        mes = f'Мои просроченные задачи:\n'

        for task in result:
            status = db_session.query(NoteStatus).filter_by(id=task.status).first()
            mes += f"- №{task.id} {task.title} - {status.name}\n"

        mes += f"\nСтраница {page_number} из {total_pages}, всего найдено задач: {total_count}.\nДля перехода между страницами используйте \'!мои-просроченные-задачи []\', где [] номер страницы.]"

        await message.author.send(mes)

    elif message.content.startswith('!обновить-статус-задачи'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели норме зрадачи и новый статус!")
            return

        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        if (len(params) == 2):
            await message.author.send("Вы не ввели новый статус!")
            return

        statusName = ''

        for i in range(2, len(params)):
            statusName += params[i]
            if (i < len(params) - 1):
                statusName += ' '


        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send(f"Задача \'№{params[1]}\' не существует!")
            return

        status = db_session.query(NoteStatus).filter_by(name=statusName).first()
        if status is None:
            await message.author.send(f"Статус задачи \'{statusName}\' не существует!")
            return
        note.status = status.id
        note.date_update = datetime.now()
        db_session.add(note)
        db_session.commit()
        await message.author.send(f"Статус задачи №{params[1]} обновлен на \'{status.name}\'.")

    elif message.content.startswith('!задача'):
        params = message.content.split(' ')
        if (len(params) == 1):
            await message.author.send("Вы не ввели норме зрадачи!")
            return
        if (params[1].isdigit() == False):
            await message.author.send("Вы ввели не число!")
            return

        note = db_session.query(Note).filter_by(id=params[1]).first()
        if note is None:
            await message.author.send(f"Задача \'№{params[1]}\' не существует!")
            return

        type = db_session.query(NoteType).filter_by(id=note.type).first()
        status = db_session.query(NoteStatus).filter_by(id=note.status).first()

        await message.author.send(f"Информация о задачи №{note.id}:\n\n"
                                  f"__Заголовок__: {note.title}\n"
                                  f"__Описание__: {note.description}\n"
                                  f"__Тип__: {type.name}\n"
                                  f"__Статус__: {status.name}\n"
                                  f"__Назначена на__: {note.recipient}\n"
                                  f"__Дата начала задачи__: {note.date_start}\n"
                                  f"__Дата окончания задач__: {note.date_end}\n"
                                  f"__Дата создания__: {note.date_create}\n"
                                  f"__Дата обновления__: {note.date_update}\n"
                                  )

    else:
        await message.author.send('Для работы со мной необходимо использовать команды.\nДля получения списка команд введите !помоги.')


client.run(TOKEN)