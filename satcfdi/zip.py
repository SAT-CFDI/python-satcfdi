import io
from collections import namedtuple
from zipfile import ZipFile, ZipInfo

ZipData = namedtuple("ZipFile", "filename data")


def zip_create(target: io.BytesIO, files: list[ZipData]):
    p = target.tell()

    with ZipFile(target, "w") as myzip:
        for f in files:
            zinfo = ZipInfo(
                filename=f.filename
            )
            zinfo.filename = f.filename
            zinfo.compress_type = 8
            zinfo.create_system = 0

            with myzip.open(zinfo, 'w') as stream:
                zinfo.flag_bits = 2056
                zinfo.external_attr = 0
                f.data(stream)

    with target.getbuffer() as view:  # change zip flag bytes
        view[p + 6:p + 8] = b"\x08\x08"


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
