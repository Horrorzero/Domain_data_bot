from db.base import get_session
from db.models import User, Domain

from sqlalchemy import select, func, update

async def add_user(user_tg_id,username):
	async with get_session() as session:
		user_query = select(func.count('*')).where(User.tg_id == user_tg_id)
		user_matched_count: int = (await session.execute(user_query)).scalar()

	if user_matched_count == 0:
		user_db_instance = User(
			username = username,
			tg_id = user_tg_id,
		)

		session.add(user_db_instance)
		await session.commit()

async def add_domains(domains,username):
	async with get_session() as session:
		user_query_u = select(User.id).where(User.username == username)
		user_matched_id = await session.execute(user_query_u)

		user_id = 0

		for i in user_matched_id:
			user_id = i[0]

		user_query_d = select(func.count('*')).where(Domain.user_id == user_id)
		user_matched_count: int = (await session.execute(user_query_d)).scalar()

		if user_matched_count == 0:
			domain_db_instance = Domain(
				name = domains,
				user_id = user_id
			)
			session.add(domain_db_instance)
		else:
			domain_db_instance = (
				update(Domain).
				where(Domain.user_id == user_id).
				values(name = domains)
			)
			await session.execute(domain_db_instance)

		await session.commit()