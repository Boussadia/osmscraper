from place_du_marche import Place_du_marche
from telemarket import Telemarket
from monoprix import Monoprix
from coursengo import Coursengo
from ooshop import Ooshop

import time

# Place du marche

# t0 = time.time()
# place_du_marche = Place_du_marche()
# place_du_marche.get_menu()
# print place_du_marche.get_categories()
# place_du_marche.get_products()
# print time.time()-t0

# print place_du_marche.extract_product("http://www.placedumarche.fr/supermarche-en-ligne-livraison-languedoc-roussillon-le-go-t-de-l-authentique-collection-a-lad-couverte-des-chefs-de-nos-r-gions-,7174,11,266.htm")


# Telemarket

telemarket = Telemarket()
# telemarket.get_menu()
# print telemarket.get_categories()
# print telemarket.extract_product_list("http://www.telemarket.fr/dynv6/listeProduitsCategorie/0015000100006-Lapin.shtml?module=&path=/categorie/0015-03--Boucherie-Volaille")

# Monoprix

# monoprix = Monoprix()
# monoprix.get_menu()
# print monoprix.get_categories()
# print monoprix.extract_product_list("http://courses.monoprix.fr/RIDD/Croquettes-Friandises-8594010")
# print monoprix.extract_product("http://courses.monoprix.fr/RIDE/Sensitive-2-rasoirs-jetables-1279753;jsessionid=EEA267656D5C486339E3B807C85ACF1E.00CD104B10C7166617D2084911CB550B10")

# Coursengo
# coursengo = Coursengo()
# coursengo.get_menu()
# print coursengo.get_categories()
# coursengo.extract_product_lists("http://www.coursengo.com/supermarche/bebe/couches/couches/")
# print coursengo.extract_product("http://www.coursengo.com/supermarche/salade-batavia-la-piece.html")
# print coursengo.extract_product("http://www.coursengo.com/supermarche/ail-temps-des-saisons-filet-de-250g.html")

# Ooshop
# ooshop = Ooshop()
# ooshop.get_menu()
# print ooshop.get_categories()