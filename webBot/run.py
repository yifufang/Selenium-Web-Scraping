from scraping.scraping import Scraping

try:
    with Scraping() as bot:
        bot.land_page()
        bot.get_all_tables()

        bot.teardown = True
        
    
except Exception as e:
    raise