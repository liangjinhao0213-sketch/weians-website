import sys, os, json
from concurrent.futures import ThreadPoolExecutor
import urllib.request

ROOT = r"C:\Users\LJHRMXS\Documents\deepseek-harness\default-workspace\weinas-site"
IDS = {
"01":"photo-1512917774080-9991f1c4c750","02":"photo-1600585154340-be6161a56a0c","03":"photo-1600607687939-ce8a6c25118c",
"04":"photo-1600566753086-00f18fb6b3ea","05":"photo-1600210492486-724fe5c67fb0","06":"photo-1600585154526-990dced4db0d",
"07":"photo-1600047509807-ba8f99d2cdde","08":"photo-1600566753190-17f0baa2a6c3","09":"photo-1616486338812-3dadae4b4ace",
"10":"photo-1616594039964-ae9021a400a0","11":"photo-1613490493576-7fde63acd811","12":"photo-1512918728675-ed5a9ecdebfd",
"13":"photo-1493809842364-78817add7ffb","14":"photo-1523217582562-09d0def993a6","15":"photo-1564013799919-ab600027ffc6",
"16":"photo-1583608205776-bfd35f0d9f83","17":"photo-1449844908441-8829872d2607","18":"photo-1502672260266-1c1ef2d93688",
"19":"photo-1484154218962-a197022b5858","20":"photo-1502005229762-cf1b2da7c5d6","21":"photo-1519710164239-da123dc03ef4",
"22":"photo-1600607687920-4e2a09cf159d","23":"photo-1600585152220-90363fe7e115","24":"photo-1541123437800-1bb1317badc2",
"25":"photo-1487958449943-2429e8be8625","26":"photo-1497366216548-37526070297c","27":"photo-1497366754035-f200968a6e72",
"28":"photo-1524758631624-e2822e304c36","29":"photo-1618221195710-dd6b41faaea6","30":"photo-1600585153490-76fb20a32601",
"31":"photo-1581094794329-c8112a89af12","32":"photo-1565043589221-1a6fd9ae45c7","33":"photo-1504328345606-18bbc8c9d7d1",
"34":"photo-1581092160562-40aa08e78837","35":"photo-1565793298595-6a879b1d9492","36":"photo-1517420704952-d9f39e95b43e",
}

def fetch(item):
    key, pid = item
    out = os.path.join(ROOT, "_source", "thumbs", key + ".jpg")
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        return key, "cached"
    url = "https://images.unsplash.com/%s?w=420&q=70&fm=jpg" % pid
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as r, open(out, "wb") as f:
            f.write(r.read())
        return key, "ok %d" % os.path.getsize(out)
    except Exception as e:
        return key, "FAIL %s" % e

with ThreadPoolExecutor(max_workers=8) as ex:
    for k, s in ex.map(fetch, IDS.items()):
        print(k, s)
