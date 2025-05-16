classes = ["Flammable",
           "Corrosive",
           "Explosive",
           "Hazardous to the Environment",
           "Oxidizing",
           "Toxic",
           "Health Hazard/Hazardous to Ozone Layer",
           "Compressed Gas",
           "Serious Health hazard", ]


def get_label(idx: int):
    if idx < 0 or idx >= len(classes):
        return None
    return classes[idx]


def get_idx(label: str):
    try:
        idx = classes.index(label)
        return idx
    except ValueError:
        return None


def get_label_short_version(dicti: dict):
    dicti = dicti.copy()
    dicti["Hazar. to Environment"] = dicti.pop("Hazardous to the Environment")
    dicti["Health Hazard"] = dicti.pop("Health Hazard/Hazardous to Ozone Layer")
    return dicti

# print(get_idx("Flammable"))
# print(get_idx("Compressed Gas"))
# print(get_idx("None"))
