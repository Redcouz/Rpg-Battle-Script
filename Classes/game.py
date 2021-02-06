import random
from .magic import Spell
from .inventory import Item



# Creating colors for UI
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

# Class Person, for players and enemies-------
class Person:
	def __init__(self, name, hp, mp, atk, df, magic, items):

		self.name = name
		self.hp = hp
		self.hpmax = hp
		self.mp = mp
		self.mpmax = mp
		self.atkl = atk - 10
		self.atkh = atk + 10
		self.magic = magic
		self.items = items
		self.df = df
		self.actions = ["Attack", "Magic", "Items"]

	# Creating Essential Functions---------------
	def take_damage(self, dmg):

		self.hp -= dmg
		if self.hp < 0:
			self.hp = 0

	def generate_damage(self):
		dmg = random.randrange(self.atkl, self.atkh)
		return dmg

	def get_hp(self):
		return self.hp

	def get_hp_max(self):
		return self.hpmax

	def get_mp(self):
		return self.mp

	def get_mp_max(self):
		return self.mpmax

	def reduce_mp(self, cost):
		self.mp -= cost
		return self.mp

	def heal(self, dmg):
		self.hp += dmg

	def put_hp_max(self):
		self.hp = self.hpmax

	def put_mp_max(self):
		self.mp = self.mpmax

	def get_name(self):
		return self.name

	# Functions for action selection----------------
	def choose_action(self):
		i = 1
		print("\n" + bcolors.BOLD + self.name + "'s Turns: "+ bcolors.ENDC)
		print(bcolors.FAIL + "Actions" + bcolors.ENDC)
		for item in self.actions:
			print("   " + str(i) + ":", item)
			i += 1
	def choose_magic(self):
		i = 1
		print(bcolors.OKBLUE + "Magic" + bcolors.ENDC + " (Write 0 to go back)")
		for spell in self.magic:
			print("   " + str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")" )
			i += 1

	def choose_item(self):
		i = 1
		print(bcolors.OKGREEN + "Items " + bcolors.ENDC + "(Write 0 to go back)")
		for item in self.items:
			print("   " + str(i) + "." + item["items"].name + " : " + item["items"].description + " (x" + str(item["quantity"]) + ")")
			i += 1

	def choose_target(self, enemies):
		i = 1

		print("\n" + bcolors.FAIL + bcolors.BOLD + "TARGET: " + bcolors.ENDC)
		for enemy in enemies:
			if enemy.get_hp	() != 0:
				print(" " + str(i) + "." + enemy.name  )
				i += 1
		choice = int(input("Choose Target: ")) - 1
		return choice

	def choose_enemy_spell(self):
		magic_choice = random.randrange(0, len(self.magic))
		spell = self.magic[magic_choice]
		magic_dmg = spell.generate_damage()

		if self.mp < spell.cost:
			self.choose_enemy_spell()
		else:
			return spell, magic_dmg

	def choose_enemy_item(self):
		item_choice = random.randrange(0, len(self.items))
		item = self.items[item_choice]
		item_props = item["items"].generate_prop()

		if self.items[item_choice]["quantity"] == 0:
			self.choose_enemy_item()
		else:
			return item, item_props, item_choice

	# Functions to print HP/MP Bars
	def enemy_get_stats(self):
		hp_bar = ""
		hp_mult = (self.hp / self.hpmax) * 100 / 2

		while hp_mult > 0:
			hp_bar += "█"
			hp_mult -= 1

		while len(hp_bar) < 50:
			hp_bar += " "

		hp_string = str(self.hp) + "/" + str(self.hpmax)
		current_hp = ""

		if len(hp_string) < 9:
			decreased = 9 - len(hp_string)
			while decreased > 0:
				current_hp += " "
				decreased -= 1
			current_hp += hp_string
		else:
			current_hp = hp_string

		print(bcolors.BOLD + self.name + ":" +
			  "                        " + bcolors.ENDC +
			  current_hp + " |" + bcolors.FAIL + hp_bar + bcolors.ENDC + bcolors.BOLD
			  + "|")


	# Updating HP/MP bars----------------------------------
	def get_stats(self):
		hp_bar = ""
		hp_mult = (self.hp / self.hpmax) * 100 / 4

		mp_bar = ""
		mp_mult = (self.mp / self.mpmax) * 100 / 10

		while hp_mult > 0:
			hp_bar += "█"
			hp_mult -= 1

		while len(hp_bar) < 25:
			hp_bar += " "

		while mp_mult > 0:
			mp_bar += "█"
			mp_mult -= 1

		while len(mp_bar) < 10:
				mp_bar += " "


		# Creating White Space at the beginning of the HP/MP string to maintain the UI order
		hp_string = str(self.hp) + "/" + str(self.hpmax)
		current_hp = ""

		if len(hp_string) < 9:
			decreased = 9 - len(hp_string)
			while decreased > 0:
				current_hp += " "
				decreased -= 1
			current_hp += hp_string
		else:
			current_hp = hp_string

		mp_string = str(self.mp) + "/" + str(self.mpmax)
		current_mp = ""

		if len(mp_string) < 9:
			decreased = 9 - len(mp_string)
			while decreased > 0:
				current_mp += " "
				decreased -= 1

			current_mp += mp_string
		else:
			current_mp = mp_string

		# Printing HP/MP Bars
		print(bcolors.BOLD + self.name + ":" +
			"                        " + bcolors.ENDC +
			current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + bcolors.BOLD
			+ "|     " +
			current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

