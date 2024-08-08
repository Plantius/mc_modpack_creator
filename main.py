import requests



r = requests.get('https://api.modrinth.com/v2/project/sodium')
data = r.json()
print(data['slug'])