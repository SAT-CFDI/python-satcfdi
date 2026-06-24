import io
from collections import namedtuple
from zipfile import ZipFile, ZipInfo

ZipData = namedtuple("ZipFile", "filename data")

_MASK_UTF_FILENAME = 1 << 11


class _ZipInfo(ZipInfo):
    def _encodeFilenameFlags(self):
        return self.filename.encode('utf-8'), self.flag_bits | _MASK_UTF_FILENAME

def zip_create(target: io.BytesIO, files: list[ZipData]):
    with ZipFile(target, "w") as myzip:
        myzip._seekable = False

        for f in files:
            zinfo = _ZipInfo(
                filename=f.filename
            )
            zinfo.compress_type = 8
            zinfo.create_system = 0

            with myzip.open(zinfo, 'w') as stream:
                zinfo.external_attr = 0
                f.data(stream)


def zip_file(zipfile, files: list[ZipData]):
    # Create a ZipFile object in write mode
    with ZipFile(zipfile, 'w') as zipf:
        # Add the input file to the zip archive with its base name
        for f in files:
            zinfo = ZipInfo(
                filename=f.filename,
                # date_time=datetime_to_tuple(datetime.now())
            )
            zinfo.compress_type = 8
            zinfo.create_system = 0

            with zipf.open(zinfo, 'w') as stream:
                stream.write(f.data)
