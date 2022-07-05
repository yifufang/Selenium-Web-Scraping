from scraping.scraping import Scraping

try:
    with Scraping() as bot:
        bot.land_page()
        bot.get_film_data()
        
        bot.teardown = True
    
except Exception as e:
    raise