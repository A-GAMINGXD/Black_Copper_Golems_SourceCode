from PIL import Image
import os, zipfile, json
import numpy as np

img = Image.open("shadow_golem.png").convert("RGBA").resize((64,64), Image.NEAREST)
arr = np.array(img)
brightness = arr[...,0]*0.299 + arr[...,1]*0.587 + arr[...,2]*0.114
mask = brightness > 150
em = np.zeros_like(arr)
em[mask] = arr[mask]
em_img = Image.fromarray(em, 'RGBA')

base = "Shadow_Copper_Golem_Glow"
os.makedirs(f"{base}/assets/minecraft/textures/entity/copper_golem", exist_ok=True)
os.makedirs(f"{base}/assets/minecraft/optifine", exist_ok=True)

img.save(f"{base}/assets/minecraft/textures/entity/copper_golem/copper_golem.png")
em_img.save(f"{base}/assets/minecraft/textures/entity/copper_golem/copper_golem_e.png")

with open(f"{base}/assets/minecraft/optifine/emissive.properties","w") as f:
    f.write("suffix.emissive=_e\n")

mcmeta = {
    "pack": {
        "pack_format": 32,
        "description": "Shadow Copper Golem (Glowing Eyes)"
    }
}
with open(f"{base}/pack.mcmeta","w") as f:
    json.dump(mcmeta,f,indent=2)

with zipfile.ZipFile("Shadow_Copper_Golem_Glow.zip","w",zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(base):
        for file in files:
            fp = os.path.join(root,file)
            z.write(fp, fp[len(base)+1:])