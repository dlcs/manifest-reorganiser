import requests
import json

def transform():
    m1 = [
        "https://dlc.services/iiif-resource/22/item/1/VIS",
        "https://dlc.services/iiif-resource/22/item/1/IR",
        "https://dlc.services/iiif-resource/22/item/1/UVF",
        "https://dlc.services/iiif-resource/22/item/1/UVR"
        ]
    m2 = [
        "https://dlc.services/iiif-resource/22/item/2/VIS",
        "https://dlc.services/iiif-resource/22/item/2/IR",
        "https://dlc.services/iiif-resource/22/item/2/UVF",
        "https://dlc.services/iiif-resource/22/item/2/UVR"
        ]

    combine(m1, "Mapa Quinatzin", "../output/hmns/mapa-quinatzin.json")
    combine(m2, "Codex Xolotl", "../output/hmns/codex-xolotl.json")


def combine(nqs, title, path):
    nq_json = [
        requests.get(nqs[0]).json(),
        requests.get(nqs[1]).json(),
        requests.get(nqs[2]).json(),
        requests.get(nqs[3]).json()
    ]
    manifest = nq_json[0]
    manifest["label"] = title
    count = 0
    for canvas in manifest["sequences"][0]["canvases"]:
        if "X.020v" in canvas["thumbnail"]["@id"]:
            continue

        canvas["label"] = canvas["images"][0]["resource"]["@id"].split('/')[-5]  # .split('_')[0]
        choice = {
            "@type": "oa:Choice",
            "default": canvas["images"][0]["resource"],
            "item": [
                nq_json[1]["sequences"][0]["canvases"][count]["images"][0]["resource"],
                nq_json[2]["sequences"][0]["canvases"][count]["images"][0]["resource"],
                nq_json[3]["sequences"][0]["canvases"][count]["images"][0]["resource"]
            ]
        }
        choice["default"]["label"] = "Visible"
        choice["item"][0]["label"] = "IR"
        choice["item"][1]["label"] = "UVF"
        choice["item"][2]["label"] = "UVR"
        canvas["images"][0]["resource"] = choice
        count = count + 1
    with open(path, 'w') as f:
        json.dump(manifest, f, indent=4)


if __name__ == '__main__':
    transform()

