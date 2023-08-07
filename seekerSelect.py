import sys
import importlib

def template_seeker_select(site, TEMPLATES_JSON, loads, choise):

	with open(TEMPLATES_JSON, 'r') as templ:
		templ_info = templ.read()

	templ_json = loads(templ_info)

	for item in templ_json['templates']:
		name = item['name']
		print(f'[{templ_json["templates"].index(item)}] {name}')

	try:
		# selected = choise
		if choise < 0:
			print()
			print(f'[-] Invalid Input!')
			sys.exit()
	except ValueError:
		print()
		print(f'[-] Invalid Input!')
		sys.exit()

	try:
		site = templ_json['templates'][choise]['dir_name']
	except IndexError:
		print()
		print(f'[-] Invalid Input!')
		sys.exit()

	print()
	print(f'[+] Loading {templ_json["templates"][choise]["name"]} Template...')

	module = templ_json['templates'][choise]['module']
	if module is True:
		imp_file = templ_json['templates'][choise]['import_file']
		importlib.import_module(f'template.{imp_file}')
	else:
		pass
	return site