from datetime import time
import asyncio

from async_lyceum_api import db
from async_lyceum_api.db.base import init_models

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


def run_init_models():
    asyncio.run(init_models())
    print("Done")


async def get_school_list(session: AsyncSession):
    return await session.stream(select(db.School))


async def add_school(session: AsyncSession, name: str, address: str):
    new_school = db.School(name=name, address=address)
    session.add(new_school)
    await session.commit()
    return new_school


async def get_classes(session: AsyncSession, school_id: int):
    query = select(db.Class.class_id, db.Class.number, db.Class.letter,
                   db.ClassType.name)
    query = query.join(db.ClassType).join(db.School)
    query = query.filter(db.School.school_id == school_id)
    result = await session.stream(query)
    return result


async def _get_or_create_class_type_id(session: AsyncSession,
                                       class_type_name: str):
    query = select(db.ClassType.class_type_id)
    query = query.filter_by(name=class_type_name)
    result = await session.execute(
        query)
    class_type_id_tuple = result.one_or_none()
    if class_type_id_tuple is None:
        class_type = db.ClassType(name=class_type_name)
        session.add(class_type)
        await session.commit()
        class_type_id = class_type.class_type_id
    else:
        class_type_id = class_type_id_tuple[0]
    return class_type_id


async def add_class(session: AsyncSession, school_id: int, number: int,
                    letter: str, class_type: str = "класс"):
    class_type_id = await _get_or_create_class_type_id(session, class_type)
    new_class = db.Class(school_id=school_id, number=number,
                         letter=letter, class_type_id=class_type_id)
    session.add(new_class)
    await session.commit()
    return new_class, class_type


async def create_subgroup(session: AsyncSession, class_id: int, name: str):
    new_subgroup = db.Subgroup(class_id=class_id, name=name)
    session.add(new_subgroup)
    await session.commit()
    return new_subgroup


async def get_subgroups(session: AsyncSession, class_id: int):
    query = select(db.Subgroup).filter_by(class_id=class_id)
    return await session.stream(query)


async def create_teacher(session: AsyncSession, name: str):
    new_teacher = db.Teacher(name=name)
    session.add(new_teacher)
    await session.commit()
    return new_teacher


async def get_teachers(session: AsyncSession):
    query = select(db.Teacher)
    return await session.stream(query)


async def create_lesson(session: AsyncSession, school_id: int,
                        name: str, start_time: dict[str, int],
                        end_time: dict[str, int], week: int,
                        weekday: int, teacher_id: int):
    new_lesson = db.Lesson(
        name=name,
        start_time=time(hour=start_time['hour'],
                        minute=start_time['minute']),
        end_time=time(hour=end_time['hour'],
                      minute=end_time['minute']),
        week=week,
        weekday=weekday,
        teacher_id=teacher_id,
        school_id=school_id
    )
    session.add(new_lesson)
    await session.commit()
    return new_lesson


async def add_lesson_to_subgroup(session: AsyncSession, lesson_id: int,
                                 subgroup_id: int):
    new_lesson_subgroup = db.LessonSubgroup(lesson_id=lesson_id,
                                            subgroup_id=subgroup_id)
    session.add(new_lesson_subgroup)
    await session.commit()
    return new_lesson_subgroup


async def get_lessons_by_subgroup_id(session: AsyncSession, subgroup_id: int):
    query = select(db.Lesson).join(db.LessonSubgroup)
    query = query.filter(db.Subgroup.subgroup_id == subgroup_id)
    return await session.stream(query)


async def get_lessons_by_class_id(session: AsyncSession, class_id: int):
    query = select(db.Lesson).join(db.LessonSubgroup)
    query = query.join(db.Subgroup).join(db.Class)
    query = query.filter(db.Class.class_id == class_id)
    return await session.stream(query)


async def delete_subgroup(session: AsyncSession, subgroup_id: int):
    row = await session.execute(select(db.Subgroup)
                                .where(db.Subgroup.subgroup_id == subgroup_id))
    row = row.scalar_one()
    await session.delete(row)
    await session.commit()


async def delete_class(session: AsyncSession, class_id: int):
    res = await get_subgroups(session, class_id)
    async for subgroup, in res:
        await delete_subgroup(session, subgroup.subgroup_id)

    row = await session.execute(select(db.Class)
                                .where(db.Class.class_id == class_id))
    row = row.scalar_one()
    await session.delete(row)
    await session.commit()


async def delete_school(session: AsyncSession, school_id: int):
    query = select(db.Class).join(db.School)
    query = query.filter(db.School.school_id == school_id)
    async for class_in_res, in await session.stream(query):
        await delete_class(session, class_in_res.class_id)

    row = await session.execute(select(db.School)
                                .where(db.School.school_id == school_id))
    row = row.scalar_one()
    await session.delete(row)
    await session.commit()

