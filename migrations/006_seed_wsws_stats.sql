-- Migration 006: Seed ski resort stats for wsws venues
-- Data sourced from official resort websites, OnTheSnow, SkiCentral, Indy Pass,
-- Michigan.gov (Porcupine Mountains), skigranitepeak.com, cascademountain.com,
-- terrypeak.com, mtbohemia.com, perfectnorth.com, paolipeaks.com, wilmotmountain.com,
-- obergatlinburg.com, skibrule.com, alpinevalleyresort.com, and Wikipedia (Kettlebowl).
--
-- Columns updated: trail_count, lift_count, vertical_drop_ft, summit_elevation_ft
-- season_opens and season_closes are NOT set — these vary year to year and should
-- be managed via the admin UI once auth is in place.

-- Alpine Valley Resort (Elkhorn, WI)
-- Source: alpinevalleyresort.com — 20 runs, 15 lifts, 388ft vertical, summit 1,040ft
UPDATE wsws.venues SET
    trail_count = 20,
    lift_count = 15,
    vertical_drop_ft = 388,
    summit_elevation_ft = 1040
WHERE slug = 'alpine-valley-resort';

-- Blackjack Ski Resort (Bessemer, MI) — now part of Snowriver Mountain Resort
-- Source: skiresort.info (standalone Blackjack mountain) — 26 trails, 6 lifts, ~490ft vertical
UPDATE wsws.venues SET
    trail_count = 26,
    lift_count = 6,
    vertical_drop_ft = 490
WHERE slug = 'blackjack-ski-resort';

-- Camp 10 Ski Area (Rhinelander, WI)
-- Source: skicentral.com, indyskipass.com — 15 trails, 4 lifts, 240ft vertical
UPDATE wsws.venues SET
    trail_count = 15,
    lift_count = 4,
    vertical_drop_ft = 240
WHERE slug = 'camp-10-ski-area';

-- Cascade Mountain (Portage, WI)
-- Source: cascademountain.com FAQs — 48 trails, 11 lifts, 460ft vertical, summit 1,280ft, base 820ft
UPDATE wsws.venues SET
    trail_count = 48,
    lift_count = 11,
    vertical_drop_ft = 460,
    summit_elevation_ft = 1280
WHERE slug = 'cascade-mountain';

-- Granite Peak (Wausau, WI)
-- Source: skigranitepeak.com — 58 trails, 7 lifts, 700ft vertical, summit 1,942ft, base 1,242ft
UPDATE wsws.venues SET
    trail_count = 58,
    lift_count = 7,
    vertical_drop_ft = 700,
    summit_elevation_ft = 1942
WHERE slug = 'granite-peak';

-- Kettlebowl Ski Hill (Bryant, WI)
-- Source: Wikipedia, travelwisconsin.com — 7 trails, 5 rope tows, 325ft vertical
UPDATE wsws.venues SET
    trail_count = 7,
    lift_count = 5,
    vertical_drop_ft = 325
WHERE slug = 'kettlebowl-ski-hill';

-- Mont Ripley (Houghton, MI) — Michigan Tech
-- Source: mtu.edu/mont-ripley — 24 trails, 3 lifts, 440ft vertical
UPDATE wsws.venues SET
    trail_count = 24,
    lift_count = 3,
    vertical_drop_ft = 440
WHERE slug = 'mont-ripley';

-- Mount Bohemia (Lac La Belle, MI)
-- Source: mtbohemia.com — 105 trails, 2 chairlifts, 900ft vertical, summit 1,500ft, base 600ft
UPDATE wsws.venues SET
    trail_count = 105,
    lift_count = 2,
    vertical_drop_ft = 900,
    summit_elevation_ft = 1500
WHERE slug = 'mount-bohemia';

-- Nordic Mountain (Wild Rose, WI)
-- Source: onthesnow.com, nordicmountain.com — 25 trails, 7 lifts, 90ft vertical
UPDATE wsws.venues SET
    trail_count = 25,
    lift_count = 7,
    vertical_drop_ft = 90
WHERE slug = 'nordic-mountain';

-- Ober Gatlinburg (Gatlinburg, TN)
-- Source: obergatlinburg.com, onthesnow.com — 10 trails, 4 lifts, 500ft vertical, summit 3,300ft
UPDATE wsws.venues SET
    trail_count = 10,
    lift_count = 4,
    vertical_drop_ft = 500,
    summit_elevation_ft = 3300
WHERE slug = 'ober-gatlinburg';

-- Paoli Peaks (Paoli, IN)
-- Source: paolipeaks.com, onthesnow.com — 15 trails, 5 lifts, 300ft vertical, summit 900ft
UPDATE wsws.venues SET
    trail_count = 15,
    lift_count = 5,
    vertical_drop_ft = 300,
    summit_elevation_ft = 900
WHERE slug = 'paoli-peaks';

-- Paul Bunyan Ski Hill (Lakewood, WI)
-- Source: indyskipass.com — 14 trails, 6 lifts, 150ft vertical
UPDATE wsws.venues SET
    trail_count = 14,
    lift_count = 6,
    vertical_drop_ft = 150
WHERE slug = 'paul-bunyan-ski-hill';

-- Perfect North Slopes (Lawrenceburg, IN)
-- Source: perfectnorth.com, onthesnow.com — 23 trails, 5 lifts (chairlifts only), 400ft vertical, summit 800ft
UPDATE wsws.venues SET
    trail_count = 23,
    lift_count = 5,
    vertical_drop_ft = 400,
    summit_elevation_ft = 800
WHERE slug = 'perfect-north-slopes';

-- Porcupine Mountains Winter Sports Complex (Ontonagon, MI)
-- Source: michigan.gov/skitheporkies — 20 trails, 2 lifts (triple + tow rope), 630ft vertical
UPDATE wsws.venues SET
    trail_count = 20,
    lift_count = 2,
    vertical_drop_ft = 630
WHERE slug = 'porcupine-mountains';

-- Ski Brule (Iron River, MI)
-- Source: skibrule.com/brule-mountain/trail-map-stats/ — 17 trails, 11 lifts, 500ft vertical, summit 1,860ft
UPDATE wsws.venues SET
    trail_count = 17,
    lift_count = 11,
    vertical_drop_ft = 500,
    summit_elevation_ft = 1860
WHERE slug = 'ski-brule';

-- Terry Peak Ski Area (Lead, SD)
-- Source: terrypeak.com — 30 trails, 5 lifts, 1,100ft vertical, summit 7,100ft
UPDATE wsws.venues SET
    trail_count = 30,
    lift_count = 5,
    vertical_drop_ft = 1100,
    summit_elevation_ft = 7100
WHERE slug = 'terry-peak-ski-area';

-- Wilmot Mountain (Wilmot, WI)
-- Source: wilmotmountain.com, onthesnow.com — 21 trails, 12 lifts, 190ft vertical
UPDATE wsws.venues SET
    trail_count = 21,
    lift_count = 12,
    vertical_drop_ft = 190
WHERE slug = 'wilmot-mountain';
