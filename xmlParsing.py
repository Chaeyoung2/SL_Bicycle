import urllib.request
from urllib.parse import urlencode, quote_plus, unquote
import xml.etree.ElementTree as ET

#"https://openapi.gg.go.kr/PublicBicycle?KEY=817d84c596314ed5a234ba8fc015519e"

decode_key = unquote('817d84c596314ed5a234ba8fc015519e')
print(decode_key)

url = 'https://openapi.gg.go.kr/PublicBicycle'

queryParams = '?' + urlencode({quote_plus('Key') : decode_key})

req = urllib.request
addrlist = []

#print(queryParams)

body = req.urlopen(url + queryParams)
req.get_method = lambda: 'GET'
response_body = body.read()
result = response_body.decode('utf-8')

tree = ET.ElementTree(ET.fromstring(result))
note = tree.getroot()

# for i in note:
#     addrlist.append(i)
#     print(addrlist)

for i in note.iter():
    addrlist.append(i.text)

print(addrlist)

# for i in note.iter("SIGUN_NM"):
#     bicycle_place = i.text
#     if '' in bicycle_place:
#         addrlist.append(i.text)
#         print(addrlist)

