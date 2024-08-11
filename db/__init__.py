from db.base import get_session
from db.models import User, Domain

from sqlalchemy import select, func, update, delete

from bot.utils.logic import editor
from bot.utils.translations import translations


async def add_user(user_tg_id):
    async with get_session() as session:
        user_query = select(func.count('*')).where(User.tg_id == user_tg_id)
        user_matched_count: int = (await session.execute(user_query)).scalar()

        if user_matched_count == 0:
            user_db_instance = User(
                tg_id=user_tg_id,
            )

            session.add(user_db_instance)
            await session.commit()


async def add_domains(domains, user_tg_id):
    async with get_session() as session:
        user_query_u = select(User.id).where(User.tg_id == user_tg_id)
        user_matched_id = await session.execute(user_query_u)

        current_query_domains = select(Domain.name).where(Domain.user_id == user_query_u)
        current_domains = (await session.execute(current_query_domains)).scalars().all()

        domains_set = set(list(editor(domains).split(' ')))

        current_domains_set = set()

        if len(current_domains) != 0:

            current_domains_set = set(list(editor(current_domains[0]).split(' ')))

            if len(current_domains_set) + len(domains_set) > 20:
                return False

        if domains_set - current_domains_set == set():
            return False

        domains = str(domains_set - current_domains_set)

        for i in user_matched_id:
            user_id = i[0]

        user_query_d = select(func.count('*')).where(Domain.user_id == user_id)
        user_matched_count: int = (await session.execute(user_query_d)).scalar()

        if user_matched_count == 0:
            domain_db_instance = Domain(
                name=domains,
                user_id=user_id
            )
            session.add(domain_db_instance)
        else:
            domain_db_instance = (
                update(Domain).
                where(Domain.user_id == user_id).
                values(name=Domain.name + ', ' + domains)
            )
            await session.execute(domain_db_instance)

        await session.commit()


async def show_domains(tg_id):
    async with get_session() as session:
        user_id_query = select(User.id).where(User.tg_id == tg_id).scalar_subquery()

        domains_query = select(Domain.name).where(Domain.user_id == user_id_query)
        domains = (await session.execute(domains_query)).scalar()

        domains = editor(domains)

        return domains


async def delete_all_domains(user_tg_id):
    async with get_session() as session:
        user_query = select(User.id).where(User.tg_id == user_tg_id)
        user_result = await session.execute(user_query)
        user_id = user_result.scalar()

        domains_del = delete(Domain).where(Domain.user_id == user_id)
        await session.execute(domains_del)

        await session.commit()


async def delete_domains(user_tg_id, domains_to_delete, language):
    async with get_session() as session:

        user_id_query = select(User.id).where(User.tg_id == user_tg_id)
        user_id = (await session.execute(user_id_query)).scalar()

        domains_query = select(Domain.name).where(Domain.user_id == user_id_query)
        domains = (await session.execute(domains_query)).scalar()

        domains = editor(domains)

        domains_set = set(list(domains.split(' ')))

        domains_to_delete_set = set(domains_to_delete)

        if len(domains_to_delete_set) == 1:
            if list(domains_to_delete_set)[0] not in domains_set:
                return translations[language]['wrong_domain']

        if len(domains_set) == 1 or len(domains_set) == len(domains_to_delete_set):
            await delete_all_domains(user_tg_id)
        else:

            remaining_domains = domains_set - domains_to_delete_set

            remaining_domains = ' '.join(remaining_domains)

            domain_db_instance = (
                update(Domain).
                where(Domain.user_id == user_id).
                values(name=remaining_domains)
            )
            await session.execute(domain_db_instance)

            await session.commit()

        return translations[language]['domain_delete']