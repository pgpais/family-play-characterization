import steamreviews

game_steam_ids = [730,570,1599340]
reviews = steamreviews.download_reviews_for_app_id_batch(game_steam_ids)
print(reviews)