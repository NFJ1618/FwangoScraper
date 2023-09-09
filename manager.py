from scraper import FwangoScraper

ststournaments = [
# "saltlakecity2023",
# "richmond2023",
# "philadelphia2023",
# "scgrandslam2023",
# "thepeopleschampionship",
# "heatwavevi",
# "rivercup",
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
]

if __name__ == '__main__':
    tourney_path = "sts"
    scraper = FwangoScraper(tourney_path)
    scraper.run(ststournaments)
    