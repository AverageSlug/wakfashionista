import urllib.request
import json

#MODIFIER ICI !				#############################################################################
lvl = 215					# Niveau maximum des items dans le build, 1-230								#
printStats = 1				# 0 = Ne pas afficher les stats des equipements choisis, uniquement le nom	#
elements = 2				# Nombres d'elements que tu veux utiliser, 0-4								#
secondaire = 1				# 0 = Full Elem (0 maîtrises secondaires), 1 = Normal						#
maitrise = 0				# -1 = Mêlée, 0 = Elem, 1 = Distance										#
tankyness = 2				# 0 = No Tank, 1 = Normal	| PV et Résis									#	
crit = 1					# 0 = Pas Crit, 1 = Normal	| Maîtrise Crit et %CC							#
dos = 0						# 0 = Pas Dos, 1 = Normal	| Maîtrise Dos									#
berz = 0					# 0 = Pas Berz, 1 = Normal	| Maîtrise Berzerk								#
soin = 0					# 0 = Pas Soin, 1 = Normal	| Maîtrise Soin									#
PAPM = 3					# -1 = PM>PA (~<11/7), 0 = PM=PM (~12/6), 1 = PA>PM (~>13/5)				#
PW = 1						# 0 = Pas PW, 1 = PW														#
PO = 1						# 0 = Pas PO, 1 = PO														#
ce = 1						# 1 = Pas de concentration elementaire, 1.2 = concentration elementaire		#
alt = 1						# 1 = Pas de Alternance, 1.2 = Alternance									#
denouement = 1				# 0 = Pas de Dénouement, 1 = Dénouement										#
							#############################################################################

#TO DO
#Choisir quelles raretés apparaissent
#Aptitudes et Enchantement
#Epées des Nations
#Autres items à condition
#Valeurs définies par l'utilisateur (ex. <10%CC, 13PA 5PM...)

#Limites
if (lvl > 230):
	lvl = 230
if (elements > 4 or elements < 4):
	elements = 4
if (elements):
	elements = 4 / elements
if (secondaire != 0 and secondaire != 1):
	secondaire = 1
if (secondaire == 0):
	secondaire = -100 * lvl

#ID de la statistique dans items.json
actionId = [""] * 32768
actionId[20] = "PV"
actionId[21] = "Points de Vie"							#Négatif
actionId[26] = "Maîtrise Soin"
actionId[31] = "PA"
actionId[390] = "Armure donnée"
actionId[391] = "Armure reçue"
actionId[400] = "Armure donnée"							#Négatif
actionId[401] = "Armure reçue"							#Négatif
actionId[41] = "PM"
actionId[42] = "PM"										#Négatif
actionId[56] = "PA max"									#Négatif
actionId[57] = "PM max"									#Négatif
actionId[71] = "Résistance Dos"
actionId[80] = "Résistance Élémentaire"
actionId[82] = "Résistance Feu"
actionId[83] = "Résistance Eau"
actionId[84] = "Résistance Terre"
actionId[85] = "Résistance Air"
actionId[98] = "Résistance Eau"							#Négatif
actionId[100] = "Résistance Élémentaire"				#Négatif
actionId[120] = "Maîtrise Élémentaire"
actionId[130] = "Maîtrise Élémentaire"					#Négatif
actionId[149] = "Maîtrise Critique"
actionId[150] = "Coup critique"
actionId[160] = "Portée"
actionId[161] = "Portée"								#Négatif
actionId[168] = "Coup critique"							#Négatif
actionId[173] = "Tacle"
actionId[175] = "Esquive"
actionId[176] = "Esquive"								#Négatif
actionId[177] = "Volonté"
actionId[180] = "Maîtrise Dos"
actionId[181] = "Maîtrise Dos"							#Négatif
actionId[184] = "Contrôle"
actionId[191] = "PW"
actionId[192] = "PW max"								#Négatif
actionId[4570] = "Dofus Prismatique (+1 Niv.)"			#304
actionId[6731] = "Dofus Turquoise (Niv.1)"				#304
actionId[7106] = "Dofushu (Niv.1)"						#304
actionId[8251] = "Dofus Ivoire (Niv.1)"					#304
actionId[400] = "+50% de vitesse de déplacement"
actionId[875] = "Parade"
actionId[988] = "Résistance Critique"
actionId[1052] = "Maîtrise Mêlée"
actionId[1053] = "Maîtrise Distance"
actionId[1055] = "Maîtrise Berserk"
actionId[1061] = "Maîtrise Berserk"						#Négatif
actionId[1062] = "Résistance Critique"					#Négatif
actionId[1063] = "Résistance Dos"						#Négatif
actionId[10681] = "Maîtrise sur 1 éléments aléatoires"	#1068	@self
actionId[10682] = "Maîtrise sur 2 éléments aléatoires"	#1068	@self
actionId[10683] = "Maîtrise sur 3 éléments aléatoires"	#1068	@self
actionId[10691] = "Résistance sur 1 éléments aléatoires"#1069	@self
actionId[10692] = "Résistance sur 2 éléments aléatoires"#1069	@self
actionId[10693] = "Résistance sur 3 éléments aléatoires"#1069	@self
actionId[20164] = "Quantité Récolte en Paysan"			#2001	@self
actionId[20171] = "Quantité Récolte en Forestier"		#2001	@self
actionId[20172] = "Quantité Récolte en Herboriste"		#2001	@self
actionId[20173] = "Quantité Récolte en Mineur"			#2001	@self
actionId[20174] = "Quantité Récolte en Trappeur"		#2001	@self
actionId[20175] = "Quantité Récolte en Pêcheur"			#2001	@self

#Poids des statistiques
poids = [0] * 32768
poids[20] = tankyness * 0.2 #PV
poids[21] = -1 #Points de Vie, Négatif
poids[26] = 4 * soin * secondaire #Maîtrise Soin
poids[31] = lvl * (PAPM + 4) #PA
poids[390] = 0 #Armure donnée
poids[391] = 0 #Armure reçue
poids[400] = 0 #Armure donnée
poids[401] = 0 #Armure reçue
poids[41] = lvl * (4 - PAPM) #PM
poids[42] = lvl -(4 - PAPM) #PM, Négatif
poids[56] = lvl * -(PAPM + 4) #PA max, Négatif
poids[57] = lvl * -(4 - PAPM) #PM max, Négatif
poids[71] = tankyness * 2 #Résistance Dos
poids[80] = tankyness * 8 #Résistance Élémentaire
poids[82] = tankyness * 2 #Résistance Feu
poids[83] = tankyness * 2 #Résistance Eau
poids[84] = tankyness * 2 #Résistance Terre
poids[85] = tankyness * 2 #Résistance Air
poids[98] = tankyness * -2 #Résistance Eau
poids[100] = tankyness * -8 #Résistance Élémentaire, Négatif
if (elements):
	poids[120] = 4 * ce * alt #Maîtrise Élémentaire
	poids[130] = -4 * ce * alt #Maîtrise Élémentaire, Négatif
if (denouement):
	poids[149] = 4 * crit #Maîtrise Critique
else:
	poids[149] = 4 * crit * secondaire #Maîtrise Critique
poids[150] = lvl * 0.25 * crit #Coup critique
poids[160] = lvl * PO #Portée
poids[161] = lvl * (-PO) #Portée, Négatif
poids[168] = lvl * -0.25 * crit #Coup critique, Négatif
poids[173] = 0 #Tacle
poids[175] = 0 #Esquive
poids[176] = 0 #Esquive, Négatif
poids[177] = 0 #Volonté
poids[180] = 0 * dos * secondaire #Maîtrise Dos
poids[181] = -4 * dos #Maîtrise Dos, Négatif
poids[184] = 0 #Contrôle
poids[191] = lvl * 2 * PW #PW
poids[192] = lvl * (-1 - PW) #PW max, Négatif
#poids[4570] = "Dofus Prismatique (+1 Niv.)"			#304
#poids[6731] = "Dofus Turquoise (Niv.1)"				#304
#poids[7106] = "Dofushu (Niv.1)"						#304
#poids[8251] = "Dofus Ivoire (Niv.1)"					#304
poids[400] = 0 #+50% de vitesse de déplacement
poids[875] = 0 #Parade
poids[988] = tankyness * 3 #Résistance Critique
if (secondaire == (-100 * lvl)):
	poids[1052] = 4 * secondaire #Maîtrise Mêlée
else:
	poids[1052] = -4 * maitrise * secondaire #Maîtrise Mêlée
if (secondaire == (-100 * lvl)):
	poids[1053] = 4 * secondaire #Maîtrise Distance
else:
	poids[1053] = 4 * maitrise * secondaire #Maîtrise Distance
poids[1055] = 0 * berz * secondaire #Maîtrise Berserk
poids[1056] = -4 * crit #Maîtrise Critique, Négatif
poids[1061] = -4 * berz #Maîtrise Berserk, Négatif
poids[1062] = tankyness * -3 #Résistance Critique, Négatif
poids[1063] = tankyness * -2 #Résistance Dos, Négatif
poids[10681] = elements * 1 * ce * alt #Maîtrise sur 1 éléments aléatoires, 1068		@self
poids[10682] = elements * 2 * ce * alt #Maîtrise sur 2 éléments aléatoires, 1068		@self
poids[10683] = elements * 3 * ce * alt #Maîtrise sur 3 éléments aléatoires, 1068		@self
poids[10691] = tankyness * 2 #Résistance sur 1 éléments aléatoires, 1069	@self
poids[10692] = tankyness * 4 #Résistance sur 2 éléments aléatoires, 1069	@self
poids[10693] = tankyness * 6 #Résistance sur 3 éléments aléatoires, 1069	@self
poids[20164] = 0 #Quantité Récolte en Paysan, 2001							@self
poids[20171] = 0 #Quantité Récolte en Forestier, 2001						@self
poids[20172] = 0 #Quantité Récolte en Herboriste, 2001						@self
poids[20173] = 0 #Quantité Récolte en Mineur, 2001							@self
poids[20174] = 0 #Quantité Récolte en Trappeur, 2001						@self
poids[20175] = 0 #Quantité Récolte en Pêcheur, 2001							@self

if (poids[10682] > 4):
	poids[10682] = 4
if (poids[10683] > 4):
	poids[10683] = 4
expertdesarmeslegeres = lvl * poids[120] * 1.5 * 0

#Poids des meilleurs equipements actuel
equipementsPoids = [0] * 1024
equipements = [{}] * 1024

#ID des different types d'équipements
#Armes 1 Main	108, 110, 113, 115, 254
#Armes 2 Mains	101, 111, 114, 117, 223, 253
#Seconde Main	112, 189

#Hache			101
#Anneau2		102	@self
#Anneau			103
#Canne			108
#Epée 1 Main	110
#Pelle			111
#Dague			112
#Baguette		113
#Marteau		114
#Aiguille		115
#Arc			117
#Bottes			119
#Amulette		120
#Cape			132
#Ceinture		133
#Coiffe			134
#Plastron		136
#Epaulettes		138
#Bouclier		189
#Epée 2 Mains	223
#Baton			253
#Cartes			254
#Familier		582
#Monture		611
#Emblème		646

#???			811
#Sublimations	812

#Relique		1000 @self
#Epique			1001 @self

rarete = [""] * 8
rarete[0] = "Qualité commune (Ancien Objet)"
rarete[1] = "Inhabituel"
rarete[2] = "Rare"
rarete[3] = "Mythique"
rarete[4] = "Légendaire"
rarete[5] = "Relique"
rarete[6] = "Souvenir"
rarete[7] = "Epique"

#Scraper
def	getResponse(url):
	operUrl = urllib.request.urlopen(url)
	if (operUrl.getcode() == 200):
		data = operUrl.read()
		jsonData = json.loads(data)
	else:
		print("Error receiving data", operUrl.getcode())
	return jsonData

#Pour avoir 2 anneaux et pour combiner les armes dans le même slot
def armes(typeArme):
	if (typeArme == 103 and equipementsPoids[103] > equipementsPoids[102]):
		return 102
	if (typeArme == 110 or typeArme == 113 or typeArme == 115 or typeArme == 254):
		return 108
	if (typeArme == 111 or typeArme == 114 or typeArme == 117 or typeArme == 223 or typeArme == 253):
		return 101
	if (typeArme == 189):
		return 112
	return typeArme

def	main():
	urlData = "https://wakfu.cdn.ankama.com/gamedata/config.json"
	jsonData = getResponse(urlData)
	urlData = "https://wakfu.cdn.ankama.com/gamedata/" + jsonData["version"] + "/items.json"
	jsonData = getResponse(urlData)

	reliqueDiff = 0
	epiqueDiff = 0
	x=-1
	for i in jsonData:
		x = x+1
		temp = 0
		relique = 0
		epique = 0
		anneau = 1
		e = i["definition"]["item"]["baseParameters"]["itemTypeId"]
		e = armes(e)
		#jsp quoi faire pour les equipements à condition, les epées des nations sont trop OP sans l'anneau donc banned .. 
		if (e == 811 or i["definition"]["item"]["level"] != lvl or i["title"]["fr"] == "Epée de Brâkmar" or i["title"]["fr"] == "Epée de Sufokia" or i["title"]["fr"] == "Epée de Bonta" or i["title"]["fr"] == "Epée d'Amakna"):
			continue
		if (i["definition"]["item"]["baseParameters"]["rarity"] == 5):
			relique = 1
		if (i["definition"]["item"]["baseParameters"]["rarity"] == 7):
			epique = 1
		for j in i["definition"]["equipEffects"]:
			if (j["effect"]["definition"]["params"] != []):
				a = j["effect"]["definition"]["actionId"]
				#if (i["title"]["fr"] == "Bague Amemnon"): #check for unknown/new actionId
				#	print(x)
				#	exit(0)
				if (a == 39 or a == 40):
					a = int(str(a) + str(int(j["effect"]["definition"]["params"][4]) % 2))
				if (a == 1068 or a == 1069):
					a = int(str(a) + str(int(j["effect"]["definition"]["params"][2])))
				elif (a == 2001):
					a = int("201" + str(int(j["effect"]["definition"]["params"][2])))
				if (i["title"]["fr"] == "Gélutin Combattant" or i["title"]["fr"] == "Gélutin Soigneur" or i["title"]["fr"] == "Gélutin Chasseur" or i["title"]["fr"] == "Gélutin Berserker" or i["title"]["fr"] == "Gélutin Aventurier"):
					temp = temp + ((j["effect"]["definition"]["params"][0] + (j["effect"]["definition"]["params"][1] * 25)) * poids[a])
				elif (e == 582 or e == 611):
					temp = temp + ((j["effect"]["definition"]["params"][0] + (j["effect"]["definition"]["params"][1] * 50)) * poids[a])
				else:
					temp = temp + (j["effect"]["definition"]["params"][0] * poids[a])
		if (e == 102 or e == 103):
			anneau = 2
		#Pour avoir une seule Relique/Epique
		if (relique == 1 and temp > equipementsPoids[e] and (temp - equipementsPoids[e]) * anneau > reliqueDiff):
			reliqueDiff = temp - equipementsPoids[e]
			equipementsPoids[1000] = temp
			equipements[1000] = i
		elif (epique == 1 and temp > (equipementsPoids[e] and temp - equipementsPoids[e]) * anneau > epiqueDiff):
			epiqueDiff = temp - equipementsPoids[e]
			equipementsPoids[1001] = temp
			equipements[1001] = i
		elif (temp > equipementsPoids[e] and relique == 0 and epique == 0):
			equipementsPoids[e] = temp
			equipements[e] = i
	#Pour remplacer les equipements avec la Relique/Epique choisie
	e = equipements[1000]["definition"]["item"]["baseParameters"]["itemTypeId"]
	e = armes(e)
	equipements[e] = equipements[1000]
	equipementsPoids[e] = equipementsPoids[1000]
	e = equipements[1001]["definition"]["item"]["baseParameters"]["itemTypeId"]
	e = armes(e)
	equipements[e] = equipements[1001]
	equipementsPoids[e] = equipementsPoids[1001]
	equipements[1000] = {}
	equipements[1001] = {}
	#Pour verifier quel combinaison d'armes est meilleure
	if (expertdesarmeslegeres > equipementsPoids[112] and expertdesarmeslegeres + equipementsPoids[108] > equipementsPoids[101]):
		equipements[101] = {}
		equipements[112] = {}
	elif (equipementsPoids[108] + equipementsPoids[112] > equipementsPoids[101]):
		equipements[101] = {}
	else:
		equipements[108] = {}
		equipements[112] = {}
	#Afficher les equipements choisis
	for i in equipements:
		if (i != {}):
			print(i["title"]["fr"] + " | " + rarete[i["definition"]["item"]["baseParameters"]["rarity"]])
			if (printStats != 0):
				for j in i["definition"]["equipEffects"]:
					a = j["effect"]["definition"]["actionId"]
					if (a == 400):
						print(actionId[a])
					if (j["effect"]["definition"]["params"] != []):
						if (i["title"]["fr"] == "Gélutin Combattant" or i["title"]["fr"] == "Gélutin Soigneur" or i["title"]["fr"] == "Gélutin Chasseur" or i["title"]["fr"] == "Gélutin Berserker" or i["title"]["fr"] == "Gélutin Aventurier"):
							j["effect"]["definition"]["params"][0] = j["effect"]["definition"]["params"][0] + (j["effect"]["definition"]["params"][1] * 25)
						elif (i["definition"]["item"]["baseParameters"]["itemTypeId"] == 582 or i["definition"]["item"]["baseParameters"]["itemTypeId"] == 611):
							j["effect"]["definition"]["params"][0] = j["effect"]["definition"]["params"][0] + (j["effect"]["definition"]["params"][1] * 50)
						if (a == 304):
							print(actionId[int(j["effect"]["definition"]["params"][0])])
						else:
							if (a == 21 or a == 40 or a == 42 or a == 56 or a == 57 or a == 100 or a == 130 or a == 161 or a == 168 or a == 176 or a == 181 or a == 192 or a == 1056 or a == 1061 or a == 1062 or a == 1063):
								print("-",end="")
							print(int(j["effect"]["definition"]["params"][0]),end="")
							if (a == 39 or a == 40 or a == 150 or a == 168 or a == 875 or a == 2001):
								print("%",end="")
							if (a == 39 or a == 40):
								print(" " + actionId[int(str(a) + str(int(j["effect"]["definition"]["params"][4]) % 2))])
							elif (a == 1068 or a == 1069):
								print(" " + actionId[int(str(a) + str(int(j["effect"]["definition"]["params"][2])))])
							elif (a == 2001):
								print(" " + actionId[int("201" + str(int(j["effect"]["definition"]["params"][2])))])
							else:
								print(" " + actionId[a])
				print("")

if __name__ == '__main__':
    main()