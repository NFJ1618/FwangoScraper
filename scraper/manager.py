from scraper import FwangoScraper

sts = [
"saltlakecity2023",
"richmond2023",
"philadelphia2023",
"scgrandslam2023",
"thepeopleschampionship",
"heatwavevi",
"rivercup",
"ers23md",
"nashvillecup2023",
"etslondon2023",
"windy-city-classic-23",
"coupeestivale",
"long-island-classic-2023",
"sts23portlandopen",
"toulouse2023",
"ers23nova",
"sdgrandslam2023",
"queencityclassic2023",
"stockholm",
"atlslam23",
"etsprague2023",
"tograndslam2023",
"fl-roundnet-open-23",
"etsparis2023",
"columbus2023",
"bcopen-sts-2023",
"ers23ct",
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
    # '2023sandiego',
    # 'atx2023',
    'nyc'
    
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
    # 'provincials' #not yet
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

bcr = [
    # 'springslam2023',
    # 'bcts2023fv',
    # 'bcts2023van',
    # 'bcts2023okanagan',
    # 'bcts2023vic',
    'bcts2023provincials'
]

psr = [
    # 'psr2023',
    'spikeforacause',
    'gritcity2',
    # 'psrhat23',
    'seattleslam23',
    
]

ura = [
    # '2023utah', #not yet
    '2023rexburg',
    '2023back-to-school',
    '2023spike-night-open',
    '2023summer-spike',
    '2023alpine',
    '2023pc',
    '2023lindon',
    '2023spike-night',
    '2023af',
    '2023sandy',
    '2023herriman',
    '2023pg',
    '2023daybreak',
    '2023springville',
    '2023springspike',
    '2023msu',
    '2023tville',
    '2023fts',
    '2023dixie',
    '2023squads',
]


sts_2022_challengers_16 = [
    'sts22orlandofl',
    'sts22richmondva',
    'sts22dallastx',
    'sts22seattlewa',
    'sts22atlantaga',
    'sts22philadelphiapa',
    'sts22raleighnc',
    'bcroundnet',
    'sts22chicagoil',
    'yeg-isd2022',
    'sts22orangecountyca',
    'ststoronto',
    'sts22saltlakecityut',
    'sts22montrealqc',
    'sts22gent',
]

sts_2022_majors_3 = [
    'sts22sanfranciscoca',
    'sts22bostonma',
    'sts22columbusoh',
    '2022championship'
]

sts_2021_tourneys = [
    # '2021florida',
    '2021texas',
    '2021erie',
    '2021rockhill',
    '2021seattle',
    '2021newengland',
    '2021saltlakecity',
    '2021chicago',
    '2021richmond',
    '2021california',
    '2021nationals',
]

if __name__ == '__main__':
    tourney_path = "../data/2021/sts"
    scraper = FwangoScraper(tourney_path)
    scraper.run(sts_2021_tourneys)
    