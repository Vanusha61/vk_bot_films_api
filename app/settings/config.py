import os
from dotenv import load_dotenv

load_dotenv()

vk_bot_api = os.getenv("VK_API")
api_list_category_films = "https://api.poiskkino.dev/v1/movie/possible-values-by-field?field=genres.name"
film_name = "https://api.poiskkino.dev/v1.4/movie/search?page=1&limit=10&query="
film_filters_cursor = "https://api.poiskkino.dev/v1.5/movie?selectFields=id&notNullFields=id&id=&externalId.imdb=&externalId.tmdb=1&externalId.kpHD=&type=movie&typeNumber=&isSeries=&status=announced&year=&releaseYears.start=&releaseYears.end=&rating.kp=&rating.imdb=&rating.tmdb=&ratingMpaa=&ageRating=&votes.kp=&votes.imdb=&votes.tmdb=&votes.filmCritics=&votes.russianFilmCritics=&votes.await=&budget.value=&audience.count=&movieLength=&seriesLength=&totalSeriesLength=&genres.name=&countries.name=&ticketsOnSale=&networks.items.name=&persons.id=&persons.profession=&persons.enProfession=&fees.world.value=&fees.usa.value=&fees.russia.value=&premiere.world=&premiere.usa=&premiere.russia=&premiere.digital=&premiere.cinema=&premiere.country=&similarMovies.id=&sequelsAndPrequels.id=&watchability.items.name=&lists=&updatedAt=&createdAt=&limit=10&next=&prev=&sortField=id&sortType=&withCount=false"
x_api_key = os.getenv("X_API_KEY")