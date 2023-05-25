from ..models import Code


def format_address_raw(calle, num_exterior, num_interior, referencia, colonia, municipio, localidad, estado, pais, codigo_postal):
    parts = []

    calle_num = None
    if calle or num_exterior or num_interior:
        if num_exterior:
            calle_num = f"{calle} #{num_exterior}"
        else:
            calle_num = f"{calle}"

        if num_interior:
            calle_num = f"{calle_num}, int. #{num_interior}"

    if colonia:
        if calle_num:
            parts.append(f"{calle_num}, {colonia}")
        else:
            parts.append(f"{colonia}")

    if referencia:
        parts.append(f"{referencia}")

    if localidad and localidad != municipio:
        parts.append(f"{localidad}")

    if municipio:
        parts.append(f"{municipio}, {estado} {codigo_postal}")
    else:
        parts.append(f"{estado} {codigo_postal}")

    parts.append(f"{pais}")
    return "\n".join(parts)


def format_address(k):
    return format_address_raw(
        calle=k["Calle"],
        num_exterior=k.get("NumeroExterior"),
        num_interior=k.get("NumeroInterior"),
        referencia=desc(k.get("Referencia")),
        colonia=desc(k.get("Colonia")),
        municipio=desc(k.get("Municipio")),
        localidad=desc(k.get("Localidad")),
        estado=desc(k["Estado"]),
        pais=desc(k["Pais"]),
        codigo_postal=k["CodigoPostal"]
    )


def desc(s):
    if isinstance(s, Code):
        return s.description
    return s
