# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_fixture[build_httpie_command-fixture_001] 1'] = 'http http://localhost:8080/Plone/front-page Accept:application/json -a admin:admin'

snapshots['test_fixture[build_httpie_command-fixture_002] 1'] = '''echo '{
  "@type": "Document",
  "title": "My Document"
}' | http POST http://localhost:8080/Plone/folder Accept:application/json Content-Type:application/json -a admin:admin'''

snapshots['test_fixture[build_httpie_command-fixture_003] 1'] = '''echo '{
  "title": "My New Document Title"
}' | http PATCH http://localhost:8080/Plone/folder/my-document Accept:application/json Content-Type:application/json -a admin:admin'''

snapshots['test_fixture[build_httpie_command-fixture_004] 1'] = 'http http://localhost:8080/Plone/front-page Accept:application/json'

snapshots['test_fixture[build_httpie_command-fixture_005] 1'] = 'http http://localhost:8080/Plone/front-page Accept:application/json Authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI"'

snapshots['test_fixture[build_httpie_command-fixture_006] 1'] = 'echo defgh | http PATCH http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f Accept:application/json Content-Type:"application/offset+octet-stream" Tus-Resumable:1.0.0 Upload-Offset:3 -a admin:secret'

snapshots['test_fixture[build_httpie_command-fixture_007] 1'] = "http 'http://localhost:8080/Plone/front-page?foo=bar&bar=foo' Accept:application/json -a admin:admin"

snapshots['test_fixture[build_curl_command-fixture_001] 1'] = 'curl -i -X GET http://localhost:8080/Plone/front-page -H "Accept: application/json" --user admin:admin'

snapshots['test_fixture[build_curl_command-fixture_002] 1'] = 'curl -i -X POST http://localhost:8080/Plone/folder -H "Accept: application/json" -H "Content-Type: application/json" --data-raw \'{"@type": "Document", "title": "My Document"}\' --user admin:admin'

snapshots['test_fixture[build_curl_command-fixture_003] 1'] = 'curl -i -X PATCH http://localhost:8080/Plone/folder/my-document -H "Accept: application/json" -H "Content-Type: application/json" --data-raw \'{"title": "My New Document Title"}\' --user admin:admin'

snapshots['test_fixture[build_curl_command-fixture_004] 1'] = 'curl -i -X GET http://localhost:8080/Plone/front-page -H "Accept: application/json"'

snapshots['test_fixture[build_curl_command-fixture_005] 1'] = 'curl -i -X GET http://localhost:8080/Plone/front-page -H "Accept: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI"'

snapshots['test_fixture[build_curl_command-fixture_006] 1'] = 'curl -i -X PATCH http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f -H "Accept: application/json" -H "Content-Type: application/offset+octet-stream" -H "Tus-Resumable: 1.0.0" -H "Upload-Offset: 3" --data-raw \'defgh\' --user admin:secret'

snapshots['test_fixture[build_curl_command-fixture_007] 1'] = 'curl -i -X GET \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' -H "Accept: application/json" --user admin:admin'

snapshots['test_fixture[build_wget_command-fixture_001] 1'] = 'wget -S -O- http://localhost:8080/Plone/front-page --header="Accept: application/json" --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_wget_command-fixture_002] 1'] = 'wget -S -O- http://localhost:8080/Plone/folder --header="Accept: application/json" --header="Content-Type: application/json" --post-data=\'{"@type": "Document", "title": "My Document"}\' --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_wget_command-fixture_003] 1'] = 'wget -S -O- --method=PATCH http://localhost:8080/Plone/folder/my-document --header="Accept: application/json" --header="Content-Type: application/json" --body-data=\'{"title": "My New Document Title"}\' --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_wget_command-fixture_004] 1'] = 'wget -S -O- http://localhost:8080/Plone/front-page --header="Accept: application/json"'

snapshots['test_fixture[build_wget_command-fixture_005] 1'] = 'wget -S -O- http://localhost:8080/Plone/front-page --header="Accept: application/json" --header="Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI"'

snapshots['test_fixture[build_wget_command-fixture_006] 1'] = 'wget -S -O- --method=PATCH http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f --header="Accept: application/json" --header="Content-Type: application/offset+octet-stream" --header="Tus-Resumable: 1.0.0" --header="Upload-Offset: 3" --body-data=\'defgh\' --auth-no-challenge --user=admin --password=secret'

snapshots['test_fixture[build_wget_command-fixture_007] 1'] = 'wget -S -O- \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' --header="Accept: application/json" --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_requests_command-fixture_001] 1'] = "requests.get('http://localhost:8080/Plone/front-page', headers={'Accept': 'application/json'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_requests_command-fixture_002] 1'] = "requests.post('http://localhost:8080/Plone/folder', headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'@type': 'Document', 'title': 'My Document'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_requests_command-fixture_003] 1'] = "requests.patch('http://localhost:8080/Plone/folder/my-document', headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'title': 'My New Document Title'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_requests_command-fixture_004] 1'] = "requests.get('http://localhost:8080/Plone/front-page', headers={'Accept': 'application/json'})"

snapshots['test_fixture[build_requests_command-fixture_005] 1'] = "requests.get('http://localhost:8080/Plone/front-page', headers={'Accept': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI'})"

snapshots['test_fixture[build_requests_command-fixture_006] 1'] = "requests.patch('http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f', headers={'Accept': 'application/json', 'Content-Type': 'application/offset+octet-stream', 'Tus-Resumable': '1.0.0', 'Upload-Offset': '3'}, data='defgh', auth=('admin', 'secret'))"

snapshots['test_fixture[build_requests_command-fixture_007] 1'] = "requests.get('http://localhost:8080/Plone/front-page?foo=bar&bar=foo', headers={'Accept': 'application/json'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_httpie_command-fixture_008] 1'] = 'http \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' Accept:application/json Accept-Encoding:"gzip, deflate" Cookie:"zyx 123" If-None-Match:\'"\'"abc123"\'"\' Authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"'

snapshots['test_fixture[build_curl_command-fixture_008] 1'] = 'curl -i -X GET \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' -H "Accept: application/json" -H "Accept-Encoding: gzip, deflate" -H "Cookie: zyx 123" -H "If-None-Match: "\'"\'"abc123"\'"\' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"'

snapshots['test_fixture[build_wget_command-fixture_008] 1'] = 'wget -S -O- \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' --header="Accept: application/json" --header="Accept-Encoding: gzip, deflate" --header="Cookie: zyx 123" --header="If-None-Match: "\'"\'"abc123"\'"\' --header="Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"'

snapshots['test_fixture[build_requests_command-fixture_008] 1'] = 'requests.get(\'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\', headers={\'Accept\': \'application/json\', \'Accept-Encoding\': \'gzip, deflate\', \'Cookie\': \'zyx 123\', \'If-None-Match\': \'"abc123"\', \'Authorization\': \'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ\'})'

snapshots['test_fixture[build_httpie_command-fixture_009] 1'] = '''echo '{
  "/": {
    "fstype": "btrfs",
    "readonly": true,
    "storage": {
      "device": "/dev/sda1",
      "type": "disk"
    }
  },
  "/tmp": {
    "storage": {
      "sizeInMB": 64,
      "type": "tmpfs"
    }
  },
  "/var": {
    "fstype": "ext4",
    "options": [
      "nosuid"
    ],
    "storage": {
      "label": "8f3ba6f4-5c70-46ec-83af-0d5434953e5f",
      "type": "disk"
    }
  },
  "/var/www": {
    "storage": {
      "remotePath": "/exports/mypath",
      "server": "my.nfs.server",
      "type": "nfs"
    }
  }
}\' | http PATCH http://localhost:8080/etc/fstab Accept:application/vnd.acme+json Accept-Encoding:"gzip, deflate" Content-Type:"application/vnd.acme+json; charset=utf-8" If-None-Match:\'"\'"abc123"\'"\' Authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"'''

snapshots['test_fixture[build_curl_command-fixture_009] 1'] = 'curl -i -X PATCH http://localhost:8080/etc/fstab -H "Accept: application/vnd.acme+json" -H "Accept-Encoding: gzip, deflate" -H "Content-Type: application/vnd.acme+json; charset=utf-8" -H "If-None-Match: "\'"\'"abc123"\'"\' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ" --data-raw \'{"/": {"fstype": "btrfs", "readonly": true, "storage": {"device": "/dev/sda1", "type": "disk"}}, "/tmp": {"storage": {"sizeInMB": 64, "type": "tmpfs"}}, "/var": {"fstype": "ext4", "options": ["nosuid"], "storage": {"label": "8f3ba6f4-5c70-46ec-83af-0d5434953e5f", "type": "disk"}}, "/var/www": {"storage": {"remotePath": "/exports/mypath", "server": "my.nfs.server", "type": "nfs"}}}\''

snapshots['test_fixture[build_wget_command-fixture_009] 1'] = 'wget -S -O- --method=PATCH http://localhost:8080/etc/fstab --header="Accept: application/vnd.acme+json" --header="Accept-Encoding: gzip, deflate" --header="Content-Type: application/vnd.acme+json; charset=utf-8" --header="If-None-Match: "\'"\'"abc123"\'"\' --header="Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ" --body-data=\'{"/": {"fstype": "btrfs", "readonly": true, "storage": {"device": "/dev/sda1", "type": "disk"}}, "/tmp": {"storage": {"sizeInMB": 64, "type": "tmpfs"}}, "/var": {"fstype": "ext4", "options": ["nosuid"], "storage": {"label": "8f3ba6f4-5c70-46ec-83af-0d5434953e5f", "type": "disk"}}, "/var/www": {"storage": {"remotePath": "/exports/mypath", "server": "my.nfs.server", "type": "nfs"}}}\''

snapshots['test_fixture[build_httpie_command-fixture_011] 1'] = "http 'http://localhost/items?user_id=12&user_id=13&from=20170101&to=20171231&user_id=15&limit=20&sort=date-asc' Accept:application/json -a admin:admin"

snapshots['test_fixture[build_curl_command-fixture_011] 1'] = 'curl -i -X GET \'http://localhost/items?user_id=12&user_id=13&from=20170101&to=20171231&user_id=15&limit=20&sort=date-asc\' -H "Accept: application/json" --user admin:admin'

snapshots['test_fixture[build_requests_command-fixture_011] 1'] = "requests.get('http://localhost/items?user_id=12&user_id=13&from=20170101&to=20171231&user_id=15&limit=20&sort=date-asc', headers={'Accept': 'application/json'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_wget_command-fixture_011] 1'] = 'wget -S -O- \'http://localhost/items?user_id=12&user_id=13&from=20170101&to=20171231&user_id=15&limit=20&sort=date-asc\' --header="Accept: application/json" --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_httpie_command-fixture_012] 1'] = '''echo '{
  "max": 0.2,
  "min": 0.1
}' | http POST http://localhost:8080/metrics Accept:application/json Content-Type:application/json -a admin:admin'''

snapshots['test_fixture[build_curl_command-fixture_012] 1'] = 'curl -i -X POST http://localhost:8080/metrics -H "Accept: application/json" -H "Content-Type: application/json" --data-raw \'{"max": 0.2, "min": 0.1}\' --user admin:admin'

snapshots['test_fixture[build_wget_command-fixture_012] 1'] = 'wget -S -O- http://localhost:8080/metrics --header="Accept: application/json" --header="Content-Type: application/json" --post-data=\'{"max": 0.2, "min": 0.1}\' --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_requests_command-fixture_012] 1'] = "requests.post('http://localhost:8080/metrics', headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'max': 0.2, 'min': 0.1}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_requests_command-fixture_009] 1'] = 'requests.patch(\'http://localhost:8080/etc/fstab\', headers={\'Accept\': \'application/vnd.acme+json\', \'Accept-Encoding\': \'gzip, deflate\', \'Content-Type\': \'application/vnd.acme+json; charset=utf-8\', \'If-None-Match\': \'"abc123"\', \'Authorization\': \'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ\'}, json={\'/\': {\'fstype\': \'btrfs\', \'readonly\': True, \'storage\': {\'device\': \'/dev/sda1\', \'type\': \'disk\'}}, \'/tmp\': {\'storage\': {\'sizeInMB\': 64, \'type\': \'tmpfs\'}}, \'/var\': {\'fstype\': \'ext4\', \'options\': [\'nosuid\'], \'storage\': {\'label\': \'8f3ba6f4-5c70-46ec-83af-0d5434953e5f\', \'type\': \'disk\'}}, \'/var/www\': {\'storage\': {\'remotePath\': \'/exports/mypath\', \'server\': \'my.nfs.server\', \'type\': \'nfs\'}}})'
