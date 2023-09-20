from scraper import FwangoScraper

ststournaments = [
# "saltlakecity2023",
# "richmond2023",
# "philadelphia2023",
# "scgrandslam2023",
# "thepeopleschampionship",
# "heatwavevi",
# "rivercup",
# "ers23md",
# "nashvillecup2023",
# "etslondon2023",
# "windy-city-classic-23",
# "coupeestivale",
# "long-island-classic-2023",
# "sts23portlandopen",
# "toulouse2023",
# "ers23nova",
# "sdgrandslam2023",
# "queencityclassic2023",
# "stockholm",
# "atlslam23",
# "etsprague2023",
# "tograndslam2023",
# "fl-roundnet-open-23",
# "etsparis2023",
# "columbus2023",
# "bcopen-sts-2023",
# "ers23ct",
]

casr = [
    'casropen',
    'open2',
    'open3',
    'open4',
]

florida = [
    'fra23-major3',
    # 'fra23-major2',
    # 'fra23-major1'
]

misc = [
    '2023sandiego',
    'atx2023',
    
]

mra = [
    'clubspike3',
    'mra-holmescounty-2023',
    'wisconsin2023',
    'mrachicago23',
    #'goshen2023', no people
    'roogang2023',
    'cincy2023',
    'battlecreek23',
]

pra = [
    # 'clemsonts2023',
    # 'atlts2023',
    # 'nashvillets2023',
    # 'birmingham2023',
    'columbia2023',
    'chattanooga2023',
    'atlsummer2023',
    'tsgreenville',
    'tsknoxville',
    'prachampionship'
]

tasr = [
    'tasr-houston-major',
    'waco2023',
]

rotc = [
    'rotcyork',
    'rotcmississauga',
    'rotcwaterloo',
    'rotcdurham',
    'rotcwindsor2023',
    'rotc-london',
]

ers = [
    'ers23uconn',
    'ers23nj',
    'ers23bos',
    'ers23roc',
    'ers23alb'
]

gwr = [
    'gwr23jan7',
]

ets = [
    'etspadova2023',
    'ets-vienna-2023',
]

if __name__ == '__main__':
    tourney_path = "misc"
    scraper = FwangoScraper(tourney_path)
    scraper.run(misc)
    