#!/usr/bin/python
# David Odenwald, 20.02.2015
# coding=utf-8

import random

random.seed()

# Hilfsvariablen
tag_arbeit = []
tag_zeit = []
zahlen = []
rest_zeit = 0


def csv_lesen():
	# Datei wird ausgelesen
	c_datei = open("taetigkeiten.csv", "r")
	c_datei_alles = c_datei.read()
	c_datei.close()

	# Return entfernen
	c_datei_alles = c_datei_alles.replace("\n", "")

	# einzelne Elemente werden in Liste geschrieben
	c_elemente = c_datei_alles.split(";")

	return c_elemente


# Zufallszahl zum auswählen der Tätigkeit wird errechnet und überprüft
def gen_zahl():
	g_zufalllszahl = 1
	while g_zufalllszahl % 3 != 0:
		g_zufalllszahl = random.randint(0, len(elemente) - 4)

		# Prüfung ob die gleiche Tätigkeit in dieser Woche schon einmal ausgeführt wurde
		if str(g_zufalllszahl) in zahlen:
			g_zufalllszahl = 1
		else:
			zahlen.extend([str(g_zufalllszahl)])

		# Wenn alle Elemente schon aufgerufen wurden
		if len(zahlen) + 1 >= len(elemente):
			print("ERROR: Zu wenig Tätigkeiten übrig.")
			exit()

	return g_zufalllszahl


# Prüft ob in der csv Datei genug Studnen stehen
def std_pruefen():
	s_stunden = 0
	for s_i in range(1, len(elemente), 3):
		s_stunden += int(elemente[s_i])

	if s_stunden < 40:
		print(s_stunden, "Stunden")
		print("Zu wenig Stunden. Bitte mindestens 40 Studnen eintragen")
		exit()


# Prüft ob Tätigkeiten übertragen werden dürfen oder nicht
def pruef_uebertrag(p_wert):
	if p_wert == 0:
		return False
	else:
		return True


elemente = csv_lesen()
std_pruefen()

for tag in range(0, 5):

	# Hilfsvariablen
	summe_zeit = 0
	zeit = 0

	# neue dimensionen zur Liste hinzufügen
	tag_arbeit.append([])
	tag_zeit.append([])

	# Wird aufgerufen wenn die letzte Tätigkeit vom Vortag zu lang war
	if rest_zeit != 0:
		tag_arbeit[tag].extend([arbeit])
		tag_zeit[tag].extend([str(rest_zeit)])
		summe_zeit += rest_zeit

	rest_zeit = 0

	while summe_zeit < 8:
		zufallszahl = gen_zahl()
		zeit = 0
		# Zeit wird in Variable gespeichert und geprüft ob sie größer als 0 ist.
		while zeit < 1:
			zeit = int(elemente[zufallszahl + 1])

		# Tätigkeit wird in Variable gespeichert
		arbeit = elemente[zufallszahl]

		# Auslesen ob die Tätigkeit übertragen werden darf
		uebertrag = pruef_uebertrag(int(elemente[zufallszahl + 2]))

		# Zeit der nächsten Tätigkeit aufaddieren
		summe_zeit += zeit

		# prüfen ob die Tätigkeit nicht zu lange dauert
		if summe_zeit > 8:
			# Wenn es Freitag ist können keine Tätigkeiten übertragen werden
			if tag is 4 or not uebertrag:
				summe_zeit -= zeit
				while summe_zeit + int(elemente[zufallszahl + 1]) > 8:
					zufallszahl = gen_zahl()

				# Tätigkeit und Zeit neu zuweisen
				arbeit = elemente[zufallszahl]
				zeit = int(elemente[zufallszahl + 1])

				tag_arbeit[tag].extend([arbeit])
				tag_zeit[tag].extend([zeit])
				summe_zeit += zeit
			else:
				tag_arbeit[tag].extend([arbeit])
				rest_zeit = summe_zeit - 8
				tag_zeit[tag].extend([zeit - rest_zeit])
				summe_zeit = 8
		else:
			tag_arbeit[tag].extend([arbeit])
			tag_zeit[tag].extend([zeit])

# Test- Ausgabe
print("\n")

for tag in range(0, 5):
	for i in range(0, len(tag_arbeit[tag])):
		print(tag_arbeit[tag][i], "-", tag_zeit[tag][i])

	print("\n")

# Config Datei wird ausgelesen
datei = open("berichter.conf", "r")
config = datei.read()
datei.close()

name = ""
aus_abt = ""
aus_jahr = ""

# Variablen werden aus der Datei übernommen
exec(config)

# Nutzereingabe
ber_num = input("Ausbildungsnachweis Nr.: ")
vom = input("vom : ")
bis = input("bis : ")

with open('form.html', 'r') as file:
	data = file.readlines()
file.close()

data[
	32] = '			<p style="position:absolute;top:146px;left:219px;white-space:nowrap" class="ft02">' + name + '</p>\n'
data[
	34] = '			<p style="position:absolute;top:146px;left:600px;white-space:nowrap" class="ft02">' + aus_abt + '</p>\n'
data[
	42] = '			<p style="position:absolute;top:202px;left:805px;white-space:nowrap" class="ft03">' + aus_jahr + '</p>\n'

data[36] = '			<p style="position:absolute;top:202px;left:404px;white-space:nowrap" class="ft03">' + str(
	ber_num) + '</p>\n'
data[38] = '			<p style="position:absolute;top:202px;left:518px;white-space:nowrap" class="ft03">' + str(
	vom) + '</p>\n'
data[40] = '			<p style="position:absolute;top:202px;left:664px;white-space:nowrap" class="ft03">' + str(
	bis) + '</p>\n'

try:
	data[50] = '			<p style="position:absolute;top:271px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[0][0] + '</p>\n'
	data[51] = '			<p style="position:absolute;top:271px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[0][0]) + '</p>\n'
except:
	pass
try:
	data[53] = '			<p style="position:absolute;top:294px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[0][1] + '</p>\n'
	data[54] = '			<p style="position:absolute;top:294px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[0][1]) + '</p>\n'
except:
	pass
try:
	data[55] = '			<p style="position:absolute;top:318px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[0][2] + '</p>\n'
	data[56] = '			<p style="position:absolute;top:318px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[0][2]) + '</p>\n'
except:
	pass
try:
	data[57] = '			<p style="position:absolute;top:341px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[0][3] + '</p>\n'
	data[58] = '			<p style="position:absolute;top:341px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[0][3]) + '</p>\n'
except:
	pass
try:
	data[59] = '			<p style="position:absolute;top:364px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[0][4] + '</p>\n'
	data[60] = '			<p style="position:absolute;top:364px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[0][4]) + '</p>\n'
except:
	pass
try:
	data[61] = '			<p style="position:absolute;top:387px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[0][5] + '</p>\n'
	data[62] = '			<p style="position:absolute;top:387px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[0][5]) + '</p>  '
except:
	pass

try:
	data[67] = '			<p style="position:absolute;top:422px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[1][0] + '</p>\n'
	data[68] = '			<p style="position:absolute;top:422px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[1][0]) + '</p>\n'
except:
	pass
try:
	data[70] = '			<p style="position:absolute;top:445px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[1][1] + '</p>\n'
	data[71] = '			<p style="position:absolute;top:445px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[1][1]) + '</p>\n'
except:
	pass
try:
	data[72] = '			<p style="position:absolute;top:468px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[1][2] + '</p>\n'
	data[73] = '			<p style="position:absolute;top:468px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[1][2]) + '</p>\n'
except:
	pass
try:
	data[74] = '			<p style="position:absolute;top:491px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[1][3] + '</p>\n'
	data[75] = '			<p style="position:absolute;top:491px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[1][3]) + '</p>\n'
except:
	pass
try:
	data[76] = '			<p style="position:absolute;top:514px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[1][4] + '</p>\n'
	data[77] = '			<p style="position:absolute;top:514px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[1][4]) + '</p>\n'
except:
	pass
try:
	data[78] = '			<p style="position:absolute;top:538px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[1][5] + '</p>\n'
	data[79] = '			<p style="position:absolute;top:538px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[1][5]) + '</p>\n'
except:
	pass

try:
	data[84] = '			<p style="position:absolute;top:572px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[2][0] + '</p>\n'
	data[85] = '			<p style="position:absolute;top:572px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[2][0]) + '</p>\n'
except:
	pass
try:
	data[87] = '			<p style="position:absolute;top:595px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[2][1] + '</p>\n'
	data[88] = '			<p style="position:absolute;top:595px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[2][1]) + '</p>\n'
except:
	pass
try:
	data[89] = '			<p style="position:absolute;top:618px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[2][2] + '</p>\n'
	data[90] = '			<p style="position:absolute;top:618px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[2][2]) + '</p>\n'
except:
	pass
try:
	data[91] = '			<p style="position:absolute;top:641px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[2][3] + '</p>\n'
	data[92] = '			<p style="position:absolute;top:641px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[2][3]) + '</p>\n'
except:
	pass
try:
	data[93] = '			<p style="position:absolute;top:665px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[2][4] + '</p>\n'
	data[94] = '			<p style="position:absolute;top:665px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[2][4]) + '</p>\n'
except:
	pass
try:
	data[95] = '			<p style="position:absolute;top:688px;left:132px;white-space:nowrap" class="ft02">' + \
			   tag_arbeit[2][5] + '</p>\n'
	data[96] = '			<p style="position:absolute;top:688px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[2][5]) + '</p>\n'
except:
	pass

try:
	data[101] = '			<p style="position:absolute;top:722px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[3][0] + '</p>\n'
	data[102] = '			<p style="position:absolute;top:722px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[3][0]) + '</p>\n'
except:
	pass
try:
	data[104] = '			<p style="position:absolute;top:745px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[3][1] + '</p>\n'
	data[105] = '			<p style="position:absolute;top:745px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[3][1]) + '</p>\n'
except:
	pass
try:
	data[106] = '			<p style="position:absolute;top:768px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[3][2] + '</p>\n'
	data[107] = '			<p style="position:absolute;top:768px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[3][2]) + '</p>\n'
except:
	pass
try:
	data[108] = '			<p style="position:absolute;top:791px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[3][3] + '</p>\n'
	data[109] = '			<p style="position:absolute;top:791px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[3][3]) + '</p>\n'
except:
	pass
try:
	data[110] = '			<p style="position:absolute;top:815px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[3][4] + '</p>\n'
	data[111] = '			<p style="position:absolute;top:815px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[3][4]) + '</p>\n'
except:
	pass
try:
	data[112] = '			<p style="position:absolute;top:838px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[3][5] + '</p>\n'
	data[113] = '			<p style="position:absolute;top:838px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[3][5]) + '</p>\n'
except:
	pass

try:
	data[118] = '			<p style="position:absolute;top:872px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[4][0] + '</p>\n'
	data[119] = '			<p style="position:absolute;top:872px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[4][0]) + '</p>\n'
except:
	pass
try:
	data[121] = '			<p style="position:absolute;top:895px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[4][1] + '</p>\n'
	data[122] = '			<p style="position:absolute;top:895px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[4][1]) + '</p>\n'
except:
	pass
try:
	data[123] = '			<p style="position:absolute;top:918px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[4][2] + '</p>\n'
	data[124] = '			<p style="position:absolute;top:918px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[4][2]) + '</p>\n'
except:
	pass
try:
	data[125] = '			<p style="position:absolute;top:941px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[4][3] + '</p>\n'
	data[126] = '			<p style="position:absolute;top:941px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[4][3]) + '</p>\n'
except:
	pass
try:
	data[127] = '			<p style="position:absolute;top:965px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[4][4] + '</p>\n'
	data[128] = '			<p style="position:absolute;top:965px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[4][4]) + '</p>\n'
except:
	pass
try:
	data[129] = '			<p style="position:absolute;top:988px;left:132px;white-space:nowrap" class="ft02">' + \
				tag_arbeit[4][5] + '</p>\n'
	data[130] = '			<p style="position:absolute;top:988px;left:775px;white-space:nowrap" class="ft02">' + str(
		tag_zeit[4][5]) + '</p>\n'
except:
	pass

output_datei = "Wochenberichte/Wochenbericht-" + ber_num + ".html"

with open(output_datei, 'w') as file:
	file.writelines(data)
file.close()
