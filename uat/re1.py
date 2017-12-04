# import re
#
# pattern = '([0-9a-zA-Z]{8})-([0-9a-zA-Z]{4})-([0-9a-zA-Z]{4})-([0-9a-zA-Z]{4})-([0-9a-zA-Z]{12})'
# pattern2 = '([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?)'
# string1 = 'bca8e3d6-5a54-11e7-addb-000c296cc8d9'
# string2 = 'bca481dd-5a54-11e7-addb-000c296cc8d9'
# string3 = '08e7fb09-83e7-11e7-95d2-000c293526b7'
# string4 = 'a39f47a6-5d32-11e7-bae2-000c2966be9f'
# a1 = re.match(pattern=pattern2,string=string3)
# print (a1)
import docker

client = docker.DockerClient(base_url='http://192.168.151.17:4243', version='auto')
a1 = client.login(username='guest',password='Allbright1', email='guest@example.com', registry='registry.allbright.local', reauth=False)
print(a1)





