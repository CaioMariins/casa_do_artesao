from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="casa_artesao")

CACHE_COORDENADAS = {}

def obter_coordenadas(cidade):

    if cidade in CACHE_COORDENADAS:
        return CACHE_COORDENADAS[cidade]
    try:
        local = geolocator.geocode(f"{cidade}, Rio de Janeiro, Brasil")

        if local:
            coordenadas = (
                local.latitude,
                local.longitude
            )
            CACHE_COORDENADAS[cidade] = coordenadas
            
            return coordenadas

    except:
        pass

    return None, None
