



def create_str(data: dict) -> str:
    genres = data.get("genres", [])
    if genres:
        genres_str = ", ".join([item.get('name', '') for item in genres])
    else:
        genres_str = "Не указаны"

    text_data = (
        f"Название: {data.get('name', 'Название не известно')}\n"
        f"Описание: {data.get('description', 'Описания нет')}\n"
        f"Год: {data.get('year', 'Год не указан')}\n"
        f"Рейтинг: {data['rating'].get('kp', 'Рейтинг не указан')}\n"
        f"Жанр: {genres_str}\n"
        f"Возраст: {data.get('ageRating', 'Не указан')}"
    )
    return text_data

