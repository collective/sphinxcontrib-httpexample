# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_fixture[build_httpie_command-fixture_001] 1'] = 'http -j http://localhost:8080/Plone/front-page -a admin:admin'

snapshots['test_fixture[build_httpie_command-fixture_002] 1'] = 'http -j POST http://localhost:8080/Plone/folder \\\\@type=Document title="My Document" -a admin:admin'

snapshots['test_fixture[build_httpie_command-fixture_003] 1'] = 'http -j PATCH http://localhost:8080/Plone/folder/my-document title="My New Document Title" -a admin:admin'

snapshots['test_fixture[build_httpie_command-fixture_004] 1'] = 'http -j http://localhost:8080/Plone/front-page'

snapshots['test_fixture[build_httpie_command-fixture_005] 1'] = "http -j http://localhost:8080/Plone/front-page Authorization:'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI'"

snapshots['test_fixture[build_httpie_command-fixture_006] 1'] = 'http -j PATCH http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f Tus-Resumable:1.0.0 Upload-Offset:3 defgh -a admin:secret'

snapshots['test_fixture[build_httpie_command-fixture_007] 1'] = "http -j 'http://localhost:8080/Plone/front-page?foo=bar&bar=foo' -a admin:admin"

snapshots['test_fixture[build_curl_command-fixture_001] 1'] = "curl -i http://localhost:8080/Plone/front-page -H 'Accept: application/json' --user admin:admin"

snapshots['test_fixture[build_curl_command-fixture_002] 1'] = 'curl -i -X POST http://localhost:8080/Plone/folder -H \'Accept: application/json\' -H \'Content-Type: application/json\' --data-raw \'{"@type": "Document", "title": "My Document"}\' --user admin:admin'

snapshots['test_fixture[build_curl_command-fixture_003] 1'] = 'curl -i -X PATCH http://localhost:8080/Plone/folder/my-document -H \'Accept: application/json\' -H \'Content-Type: application/json\' --data-raw \'{"title": "My New Document Title"}\' --user admin:admin'

snapshots['test_fixture[build_curl_command-fixture_004] 1'] = "curl -i http://localhost:8080/Plone/front-page -H 'Accept: application/json'"

snapshots['test_fixture[build_curl_command-fixture_005] 1'] = "curl -i http://localhost:8080/Plone/front-page -H 'Accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI'"

snapshots['test_fixture[build_curl_command-fixture_006] 1'] = "curl -i -X PATCH http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f -H 'Accept: application/json' -H 'Content-Type: application/offset+octet-stream' -H 'Tus-Resumable: 1.0.0' -H 'Upload-Offset: 3' --data-raw 'defgh' --user admin:secret"

snapshots['test_fixture[build_curl_command-fixture_007] 1'] = "curl -i 'http://localhost:8080/Plone/front-page?foo=bar&bar=foo' -H 'Accept: application/json' --user admin:admin"

snapshots['test_fixture[build_wget_command-fixture_001] 1'] = "wget -S -O- http://localhost:8080/Plone/front-page --header='Accept: application/json' --auth-no-challenge --user=admin --password=admin"

snapshots['test_fixture[build_wget_command-fixture_002] 1'] = 'wget -S -O- http://localhost:8080/Plone/folder --header=\'Accept: application/json\' --header=\'Content-Type: application/json\' --post-data=\'{"@type": "Document", "title": "My Document"}\' --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_wget_command-fixture_003] 1'] = 'wget -S -O- --method=PATCH http://localhost:8080/Plone/folder/my-document --header=\'Accept: application/json\' --header=\'Content-Type: application/json\' --body-data=\'{"title": "My New Document Title"}\' --auth-no-challenge --user=admin --password=admin'

snapshots['test_fixture[build_wget_command-fixture_004] 1'] = "wget -S -O- http://localhost:8080/Plone/front-page --header='Accept: application/json'"

snapshots['test_fixture[build_wget_command-fixture_005] 1'] = "wget -S -O- http://localhost:8080/Plone/front-page --header='Accept: application/json' --header='Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI'"

snapshots['test_fixture[build_wget_command-fixture_006] 1'] = "wget -S -O- --method=PATCH http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f --header='Accept: application/json' --header='Content-Type: application/offset+octet-stream' --header='Tus-Resumable: 1.0.0' --header='Upload-Offset: 3' --body-data='defgh' --auth-no-challenge --user=admin --password=secret"

snapshots['test_fixture[build_wget_command-fixture_007] 1'] = "wget -S -O- 'http://localhost:8080/Plone/front-page?foo=bar&bar=foo' --header='Accept: application/json' --auth-no-challenge --user=admin --password=admin"

snapshots['test_fixture[build_requests_command-fixture_001] 1'] = "requests.get('http://localhost:8080/Plone/front-page', headers={'Accept': 'application/json'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_requests_command-fixture_002] 1'] = "requests.post('http://localhost:8080/Plone/folder', headers={'Accept': 'application/json'}, json={'@type': 'Document', 'title': 'My Document'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_requests_command-fixture_003] 1'] = "requests.patch('http://localhost:8080/Plone/folder/my-document', headers={'Accept': 'application/json'}, json={'title': 'My New Document Title'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_requests_command-fixture_004] 1'] = "requests.get('http://localhost:8080/Plone/front-page', headers={'Accept': 'application/json'})"

snapshots['test_fixture[build_requests_command-fixture_005] 1'] = "requests.get('http://localhost:8080/Plone/front-page', headers={'Accept': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsbmFtZSI6IiIsInN1YiI6ImFkbWluIiwiZXhwIjoxNDY0MDQyMTAzfQ.aOyvMwdcIMV6pzC0GYQ3ZMdGaHR1_W7DxT0W0ok4FxI'})"

snapshots['test_fixture[build_requests_command-fixture_006] 1'] = "requests.patch('http://nohost/plone/folder/@upload/032803b64ad746b3ab46d9223ea3d90f', headers={'Accept': 'application/json', 'Tus-Resumable': '1.0.0', 'Upload-Offset': '3'}, data='defgh', auth=('admin', 'secret'))"

snapshots['test_fixture[build_requests_command-fixture_007] 1'] = "requests.get('http://localhost:8080/Plone/front-page?foo=bar&bar=foo', headers={'Accept': 'application/json'}, auth=('admin', 'admin'))"

snapshots['test_fixture[build_httpie_command-fixture_008] 1'] = 'http -j \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' Accept-Encoding:\'gzip, deflate\' Cookie:\'zyx 123\' If-None-Match:\'"abc123"\' Authorization:\'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ\''

snapshots['test_fixture[build_curl_command-fixture_008] 1'] = 'curl -i \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' -H \'Accept: application/json\' -H \'Accept-Encoding: gzip, deflate\' -H \'Cookie: zyx 123\' -H \'If-None-Match: "abc123"\' -H \'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ\''

snapshots['test_fixture[build_wget_command-fixture_008] 1'] = 'wget -S -O- \'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\' --header=\'Accept: application/json\' --header=\'Accept-Encoding: gzip, deflate\' --header=\'Cookie: zyx 123\' --header=\'If-None-Match: "abc123"\' --header=\'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ\''

snapshots['test_fixture[build_requests_command-fixture_008] 1'] = 'requests.get(\'http://localhost:8080/Plone/front-page?foo=bar&bar=foo\', headers={\'Accept\': \'application/json\', \'Accept-Encoding\': \'gzip, deflate\', \'Cookie\': \'zyx 123\', \'If-None-Match\': \'"abc123"\', \'Authorization\': \'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ\'})'
