from app.core.redis import redis_client


class ReservationService:

    EXPIRE_TIME = 600

    @staticmethod
    def reserve_seat(session_id: int, row: int, seat: int):

        key = f"reservation:{session_id}:{row}:{seat}"

        return redis_client.set(
            key,
            "reserved",
            ex=ReservationService.EXPIRE_TIME,
            nx=True,
        )

    @staticmethod
    def release_seat(session_id: int, row: int, seat: int):

        key = f"reservation:{session_id}:{row}:{seat}"

        redis_client.delete(key)

    @staticmethod
    def is_reserved(session_id: int, row: int, seat: int):

        key = f"reservation:{session_id}:{row}:{seat}"

        return redis_client.exists(key)