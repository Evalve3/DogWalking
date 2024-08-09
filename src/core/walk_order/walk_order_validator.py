import datetime


class WalkOrderValidator:

    def validate_walk_duration(self, duration: int) -> bool:
        # Прогулка может длиться не более получаса.
        return duration <= 30

    def validate_walk_time(self, time: datetime.time) -> bool:
        # Проверяем, что время начинается либо в начале часа, либо в половине
        if time.minute not in (0, 30):
            return False

        # Проверяем, что время находится в допустимом диапазоне (7 утра - 23 вечера)
        if time.hour < 7 or (time.hour >= 23 and time.minute > 0):
            return False

        return True
