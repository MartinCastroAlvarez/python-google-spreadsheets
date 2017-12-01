from wolverine import Wolverine
import pytest
import os


@pytest.fixture
def sid():
    yield "1s3kY46A0KBPnM3_HEMcu8CvquSsCPUV-pxCaknv2GQ4"


@pytest.fixture
def sname():
    yield "Opportunities"


@pytest.fixture
def w(sid):
    os.environ['GOOGLE_PRIVATE_KEY_ID'] = 'c0d18bbe03f1514c5f446df8dad0ae459fc8ccff'
    os.environ['GOOGLE_PRIVATE_KEY'] = """-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDjTFNfCRSvfTVS\nj0fIvQ7fL/51mtaqYCwbYDjG64JNArY2OK9HpMgPXS3whZEVJhrXhRv2F4vimHJQ\nffPrwbb+VdoGl5A3krwIRsgewfhCq4tWCDxIf0/SWKCR6sF/8PGqRcOHeij/AhZ9\n0oeKskSB5kutAGgLoFZqMZQO1L3BGSy9JrVcxnib0MiKmJEgS/0GrrWQgzeyn+YA\nz1wN3dkKYXUGQCERoe74D3TFQAPLzKmDHBOahYackJMT6fgENovz1l/FRkLRGVH5\nH3BYRUKttjNTyVjGjIx8QJmdoIyFvuojFKrB4xqBP97InRkD9CUb3CSmZBM23pHO\nJtHzXks5AgMBAAECggEBAJ1ka9LCEf3W4MaTiqyZJaQssrIzDvSZddFbFtW/nNHA\nz/XJ2K3uj837wuTrSGRxp2KXvJ3y/h1hXL8aCH62/AUv47Ju3yFsTSIaCVcrD8Ly\n0KA5Qa0d42MPldiUy3rRmDZE6rl0QNEcXACyeML04HVmx/466tEqLMyKGjEO5XrA\nqpHGIslqJSv02xfB/TiJd3tW7sdI+uHxDKnoaXI/8IjBlmoHi0hcdGu8a0+1ZMRX\nnIo1QYb1LHbQcIqzBylpVF9JInYKeZQdK1jMwpR7TE/uvquDOUy2fIAeLDAGZTm7\nQwDhshKSx+isftttWUMmc4fasrxujXzzjiFtaBsDf0UCgYEA/A7zF2rEjBv2NrAt\njr9PPCGlJbjvy93EW+Zl/joprCnwcLnKgXjNtm62JQqtUm0QfbCUsbJzBbLfu1A/\nDTi42VU2p9lOkk0b2AL/nRJz3lDTHDVn//G1r0/WjsP2unsNLljkelSvbS+pajjU\ngF4g3FZDXXK17uZZ2E3RSPKtfz8CgYEA5tpBPiZ2+VI2FeFcnP5ZLAbDaH0FLHFM\nNkDyGYx1t8v93/GajGl8B1hFn6bNcroRgsUkwpavDFEDpCt3gTUZ9r0ISKe4ttA7\nPQ9bQhAnkpz23V0FGrYvxzhv89scHp0c1PQ9KItdpPBmbHvnMJsKhiPUnapfon4P\nHL7p7Ak0j4cCgYEAoGFSw/+neA8CpuGK211XKUevMUVvLyS4oFEFbLHNekJlPxS4\niZE4M3BWbVNR3TSQXalRs498KJAcU69Hrz38QC08Taizmdt+b//YbTUkjLyY10YU\nGoLNu/Ls7oI6J4XMaUUee8gOp0bAYVovvE4oUoqA6qDmqk/fswYwuF3RjzkCgYBo\nJUKVxUibRgl8aYUclmqoQAzcELrKx/o356jQ+dsJpg/MffTZL6VystIGKnw5K9RG\niKYC23PxPINGBw4MzmX+OF2KWZAteVegPlNPRHZ14DZGu3ZYDKUVXVK0Ur8m2H5v\nXBhTODxw8rtiaats9CUVSwjacEhgyDoNH9vsTmLV9QKBgBXv8HLQNpuy21KAmAKE\niq5ZmJsbez01GnnigSqBChNBYN1au36mIc5qfv37THu9Spn3sY5hFfonzMPjEb1n\nF29ILCsoSIYPvh2RgNjCB7DOufGcApAC6pHH6nsCVClQFcL2HnfyUo/okfW0TuVz\nkt/lpQF/B3c1RFf+v1IRH3Rz\n-----END PRIVATE KEY-----\n"""
    os.environ['GOOGLE_CLIENT_EMAIL'] = '988404755058-el9gr8pijof72snmmki214ka2670fsjq@developer.gserviceaccount.com'
    os.environ['GOOGLE_CLIENT_ID'] = '988404755058-el9gr8pijof72snmmki214ka2670fsjq.apps.googleusercontent.com'
    os.environ['GOOGLE_TYPE'] = 'service_account'
    yield Wolverine(sid)


class TestWolverine(object):

    def test_get_total_rows(self, w, sname):
        total = w.getTotalRows(sname)
        assert type(total) is int
        assert total > 0

    def test_get_total_columns(self, w, sname):
        total = w.getTotalColumns(sname)
        assert type(total) is int
        assert total > 0

    def test_get_a_few_cells(self, w, sname):
        cells = w.getCells(sname, (1, 3), (2, 5))
        a = cells[0][0]
        b = cells[0][1]
        cells = w.getCells(sname, (1, 3), (1, 5))
        assert cells[0][1] == a
        assert cells[0][2] == b

    def test_iterator(self, w, sname):
        i = 0
        for row in w.iterator(sname):
            i += 1
            assert type(row) is dict
            assert "Code" in row
        assert i > 0
