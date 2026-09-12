#!/usr/bin/env python3
"""Build GemGame's six English acquisition pages from current, bounded claims.

Run from any directory. Assets are checked in; source provenance is in
gemgame/assets/2026-09/provenance.json. Publication is a separate Pages deployment.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://georgepwall1991.github.io/fleet-commander-site/gemgame/"
STORE = "https://apps.apple.com/app/id6761720994"
NAVBASE = "/fleet-commander-site/gemgame/"
ASSETS = "assets/2026-09/"
SHOTS = [
    ("gameplay", "Swap jewels. Make a spectacular match."),
    ("conservatory", "Bring five magical worlds back to life."),
    ("garden", "Restore fountains and flowering corners."),
    ("specials", "Try a special combination in Jewel Lab."),
    ("mastery", "Explore optional world mastery."),
    ("boss", "Take on a cosmic guardian."),
    ("daily-star", "Return for a free Daily Star puzzle."),
]


def link(route, label):
    return f'<a href="{NAVBASE}{route}">{escape(label)}</a>'


def cta(prefix):
    return f'<div class="download"><a href="{STORE}" aria-label="Download GemGame on the App Store"><img src="{prefix}assets/app-store-badge.svg" width="180" height="60" alt="Download on the App Store"></a><p>Free for iPhone · iOS 18 or later<br>Optional in-app purchases · English-language game</p></div>'


def section(title, content):
    return f'<section class="section"><h2>{escape(title)}</h2>{content}</section>'


def picture(name, alt, prefix, eager=False):
    return f'<picture><source srcset="{prefix}{ASSETS}{name}.webp" type="image/webp"><img src="{prefix}{ASSETS}{name}.jpg" width="600" height="1300" loading="{"eager" if eager else "lazy"}" {"fetchpriority=high" if eager else ""} alt="{escape(alt)}"></picture>'


def render(route, title, description, heading, lead, content):
    prefix = "../" if route else "./"
    url = BASE + route
    schema = {
        "@context": "https://schema.org", "@type": "WebPage",
        "name": title, "description": description, "url": url,
        "inLanguage": "en", "dateModified": "2026-09-12",
        "about": {"@id": BASE + "#game"},
    }
    if not route:
        schema = {"@context": "https://schema.org", "@graph": [schema, {
            "@type": ["VideoGame", "MobileApplication"], "@id": BASE + "#game",
            "name": "GemGame: Cozy Match 3 Puzzle", "alternateName": "GemGame",
            "description": description, "url": BASE, "sameAs": STORE,
            "applicationCategory": "GameApplication", "genre": "Match 3 puzzle",
            "operatingSystem": "iOS 18.0 or later", "inLanguage": "en",
            "image": BASE + ASSETS + "icon.png", "downloadUrl": STORE,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "url": STORE},
            "author": {"@type": "Person", "name": "George Wall"},
            "screenshot": [BASE + ASSETS + n + ".jpg" for n, _ in SHOTS],
        }]}
    hero_image = picture("gameplay", "Real GemGame match-3 board with jewel combinations", prefix, True) if not route else ""
    nav = "".join(link(r, label) for r, label in [("no-ads/", "No ads"), ("offline/", "Offline play"), ("garden/", "The garden"), ("faq/", "FAQ")])
    # Preserve reciprocal language alternates for the five existing translated pages.
    alternates = ""
    if route != "offline/":
        alternates = ''.join(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{locale}{route}">\n' for lang, locale in [("en", ""), ("fr", "fr/"), ("de", "de/"), ("it", "it/"), ("el", "el/"), ("fi", "fi/"), ("x-default", "")])
    page = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
{alternates}<meta name="apple-itunes-app" content="app-id=6761720994">
<meta property="og:type" content="website"><meta property="og:site_name" content="GemGame">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{ASSETS}icon.png">
<meta property="og:image:width" content="1024"><meta property="og:image:height" content="1024">
<meta property="og:image:alt" content="GemGame cyan jewel and leaves app icon">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(description)}"><meta name="twitter:image" content="{BASE}{ASSETS}icon.png">
<link rel="icon" type="image/png" href="{prefix}{ASSETS}icon.png"><meta name="theme-color" content="#081e22">
<link rel="stylesheet" href="{prefix}assets/acquisition.css">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</', '<\\/')}</script>
</head><body><a class="skip" href="#main">Skip to content</a><div class="shell">
<header><a class="brand" href="{NAVBASE}"><img src="{prefix}{ASSETS}icon-small.png" width="48" height="48" alt="">GemGame</a><nav aria-label="Main navigation">{nav}</nav></header>
<main id="main"><section class="hero {"home-hero" if not route else "article-hero"}"><div><p class="eyebrow">A little escape for iPhone</p>
<h1>{heading}</h1><p class="lead">{lead}</p>{cta(prefix)}
<ul class="pills" aria-label="Game features"><li>No ads</li><li>Offline core puzzles</li><li>Restore a garden</li></ul></div>{hero_image}</section>
{content}
<section class="closing"><p class="eyebrow">Your next clever move</p><h2>Make room for a little magic.</h2>{cta(prefix)}<p class="small">Campaign lives refill over time. Daily Star costs no lives. Purchases and Game Center need an internet connection.</p></section></main>
<footer><p>© 2026 GemGame · George Wall</p><nav aria-label="Footer">{link('press/','Press kit')}{link('support/','Support')}{link('privacy/','Privacy')}{link('terms/','Terms')}{link('site-index/','All guides')}</nav></footer>
</div></body></html>
'''
    path = ROOT / "gemgame" / route / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page)


def build():
    gallery = '<div class="gallery">' + ''.join(f'<figure>{picture(n,a,"./")}<figcaption>{escape(a)}</figcaption></figure>' for n,a in SHOTS) + '</div>'
    home = section("A satisfying match. Something lasting.", '''<div class="cards"><article><h3>Find the combination</h3><p>Swap neighbouring jewels to match three. Create striped, wrapped, rainbow and seeker specials, then combine them for sparkling cascades.</p></article><article><h3>Bring the garden to life</h3><p>Spend earned stars to restore fountains and flowering corners. Discover districts, decorative finishes and woodland visitors.</p></article><article><h3>Take a small daily adventure</h3><p>Play a fresh Daily Star puzzle without spending lives. Try combinations in the free Jewel Lab, or draft powers for a five-board Relic Run.</p></article></div>''')
    home += section("See the game you'll play", '<p>Real gameplay and earned progress from the five-world adventure. Gardens and mastery unlock as you play.</p>' + gallery)
    home += section("Twenty-four seconds of magic", '<video controls playsinline preload="none" poster="./assets/2026-09/gameplay.jpg" width="886" height="1920" aria-label="GemGame real gameplay preview"><source src="./assets/2026-09/preview.mp4" type="video/mp4"><a href="./assets/2026-09/preview.mp4">Watch the gameplay preview</a></video>')
    home += section("What is free?", '<p>The base campaign, garden and Jewel Lab are free. Daily Star gives you a free daily board without spending a life. Campaign lives refill over time.</p><p>The optional Complete Collection is one permanent purchase with five premium chapter reward tracks and 50 Hard Mode puzzles. Coin packs and some decorative finishes are optional purchases.</p>')
    home += section("Find your kind of puzzle break", f'<div class="cards"><article><h3>A game without ad breaks</h3><p>No banners, interstitials or rewarded video ads.</p>{link("no-ads/","How no-ads play works →")}</article><article><h3>A puzzle for the commute</h3><p>Core puzzles run locally; online extras are clearly explained.</p>{link("offline/","What works without Wi-Fi →")}</article><article><h3>A garden to return to</h3><p>Turn earned stars into visible restoration.</p>{link("garden/","Explore the garden →")}</article></div>')
    render("", "GemGame — Offline Match 3 for iPhone, No Ads", "Play GemGame, a cozy match 3 puzzle for iPhone with no ads. Swap jewels, enjoy offline core puzzles and restore a magical garden. Free with optional purchases.", "Offline match 3.<br>A little everyday magic.", "Swap sparkling jewels, discover a clever combination and bring a magical garden to life. A cozy puzzle break with no ads.", home)

    noads = section("No ad purchase required", '<p>GemGame has no banner ads, no interstitials and no rewarded video ads. You do not need to buy an ad-removal upgrade.</p>')
    noads += section("Free to start, with optional extras", '<p>The base campaign and garden remain free. The optional Complete Collection adds five premium reward tracks and 50 Hard Mode puzzles. Coins and some decorative finishes are optional purchases.</p>')
    noads += section("No ad breaks does not mean unlimited lives", '<p>Campaign lives refill over time. If you run out, you can wait for a refill. Daily Star offers a free daily board with no life cost, and Jewel Lab lets you practise combinations without spending lives or earning campaign rewards.</p>')
    noads += section("Think through your next swap", '<p>Campaign levels are move-based. There is no countdown rushing an individual move. Match neighbouring jewels and combine specials; this is a swap-three puzzle.</p>' + picture("gameplay", "Actual swap-three GemGame board", "../"))
    noads += section("Playing without a connection", '<p>Core puzzles work offline. Purchases, Restore Purchases and Game Center require internet access.</p>' + link("offline/", "Read the offline guide →"))
    render("no-ads/", "Match 3 With No Ads for iPhone — GemGame", "Looking for an iPhone match 3 with no ads? GemGame has no ad-removal fee. Play jewel puzzles and restore a garden, with refilling lives and optional purchases.", "A match 3 with<br>no ad breaks.", "Make your next match without a video interrupting it. GemGame has no ads from the first puzzle.", noads)

    offline = section("What works offline?", '<div class="table-wrap"><table><thead><tr><th>Feature</th><th>Connection needed?</th></tr></thead><tbody><tr><td>Core campaign puzzles and locally saved progress</td><td>No</td></tr><tr><td>Garden restoration using earned stars</td><td>No</td></tr><tr><td>Jewel Lab practice</td><td>No</td></tr><tr><td>Download or update the app</td><td>Yes</td></tr><tr><td>Buy or restore purchases</td><td>Yes</td></tr><tr><td>Game Center leaderboards and achievements services</td><td>Yes</td></tr></tbody></table></div>')
    offline += section("Before a flight or a journey", '<ol><li>Download GemGame from the App Store while connected.</li><li>Open the game and check it is ready to play.</li><li>If you need to restore a purchase on this device, do that while online.</li><li>Open your next campaign board when you want an offline puzzle break.</li></ol><p>Progress is stored on the device. Keep the app installed to preserve local progress; do not assume reinstalling will recover a save.</p>')
    offline += section("No Wi-Fi is different from unlimited play", '<p>Offline campaign play still uses lives, which refill over time. Being offline does not remove the life system or unlock purchases. Within a level, you can consider each move without a countdown clock.</p>')
    offline += section("A real jewel-matching puzzle", picture("specials", "Jewel Lab practice with real gem combinations", "../") + '<p>Swap adjacent jewels, make matches and discover special combinations. Then use earned stars to bring your garden back to life.</p>' + link("garden/", "See what your stars restore →"))
    render("offline/", "Offline Match 3 for iPhone: What Works Without Wi-Fi? — GemGame", "Play GemGame's core match 3 puzzles offline on iPhone. See what works without Wi-Fi, what needs internet, and how campaign lives and local saves work.", "Your next match.<br>Without Wi-Fi.", "Core GemGame puzzles run on your iPhone. Download before your journey, then enjoy jewel matching without a constant connection.", offline)

    garden = section("Your matches become a place", '<p>Earn stars through campaign play and spend them restoring fountains, flowering corners and peaceful places to sit. Discover new districts and choose decorative finishes as your garden grows.</p>' + picture("garden", "Actual GemGame garden with restored areas and decorative choices", "../"))
    garden += section("Five worlds to awaken", '<p>Travel from the Living Conservatory through the Nebula Waterways, Aurora Observatory and Plasma Forge to the Heart of the Void. Face guardians and make each world transformation permanent through campaign progress.</p><p>Return to choose free lighting, replay an awakening and pursue optional mastery. These places unfold through progress; the mature garden shown here is not your starting save.</p>')
    garden += section("A little company", '<p>Welcome butterflies, songbirds and other woodland visitors as you play. Restore a corner, look around and enjoy the change before your next puzzle.</p>')
    garden += section("What can I restore for free?", '<p>The base garden remains free, and restoration uses earned stars. Some decorative finishes require premium access. Optional purchases are explained in the game; you do not need to buy the Complete Collection to begin growing your garden.</p>' + link("faq/", "Read the purchase and progress FAQ →"))
    render("garden/", "Garden Match 3 for iPhone — Restore a Magical Garden | GemGame", "Match jewels and spend earned stars restoring GemGame's magical garden. Discover districts and woodland visitors. Free base garden with optional premium finishes.", "One clever match.<br>A garden coming to life.", "Restore a fountain, make room for flowers and welcome a little woodland company. Your puzzle progress becomes something you can return to.", garden)

    answers = [
        ("Is GemGame free?", "Yes. Download it free on iPhone with iOS 18 or later. The base campaign, garden and Jewel Lab are free. Purchases are optional."),
        ("Does it have ads?", "No. There are no banners, interstitials or rewarded video ads, and no ad-removal purchase is required."),
        ("Can I play offline?", "Core puzzles, local progress and garden restoration work offline. Downloading, updating, purchases, Restore Purchases and Game Center require internet."),
        ("Are lives unlimited?", "No. Campaign lives refill over time. Daily Star gives you a free daily board with no life cost. Jewel Lab practice uses no lives and awards no campaign rewards."),
        ("Is there a countdown during a level?", "Campaign levels use a move budget, with no countdown rushing each swap. The life refill timer is separate."),
        ("What is the Complete Collection?", "One permanent purchase includes all five premium chapter reward tracks and 50 Hard Mode puzzles. Rewards are earned through play. The base campaign and garden remain free. Coin packs are separate, optional purchases."),
        ("I already bought a chapter pass or Hard Mode. Do I pay again?", "Verified owners of a legacy chapter pass or Hard Mode qualify for the Complete Collection through Restore Purchases at no extra cost. Restore while online using the Apple account that made the purchase. Coin-pack ownership alone does not qualify."),
        ("Will reinstalling restore my progress?", "Game progress is stored locally. Restore Purchases restores eligible ownership, not a deleted campaign save. Keep the app installed to preserve your local progress."),
        ("What language is the game in?", "The current App Store listing reports English for the app. Translated website or store text does not mean the game's interface supports that language."),
        ("How do I get help?", "Email georgewall1991@icloud.com with the issue, app version and your iPhone model. Do not include passwords or payment-card details."),
    ]
    anchors = {0: 'faq-getting-started', 3: 'faq-gameplay', 7: 'faq-account'}
    faq = '<section class="section"><dl class="faq">' + ''.join(f'<dt id="{anchors.get(i, f"question-{i + 1}")}">{escape(q)}</dt><dd>{escape(a)}</dd>' for i,(q,a) in enumerate(answers)) + '</dl></section>'
    render("faq/", "GemGame FAQ — Offline Play, Lives and Purchases", "Answers about GemGame for iPhone: no ads, offline puzzles, free lives, Complete Collection, Restore Purchases and local progress. English-language game.", "A few things<br>worth knowing.", "Clear answers before your first match, and a little help when you need it.", faq)

    press = section("The short version", '<p>GemGame is a free match-3 puzzle for iPhone by independent developer George Wall. Swap jewels, combine specials and restore a magical garden across five connected worlds. No ads; core puzzles work offline. Campaign lives refill over time and purchases are optional.</p>')
    press += section("Facts for a review", '<ul><li>Platform: iPhone, iOS 18 or later; English-language game.</li><li>Public version checked 12 September 2026: 2.3.0.</li><li>Base campaign and garden free; optional Complete Collection, coin packs and premium decorative finishes.</li><li>Daily Star: one free daily board without a life cost.</li><li>Jewel Lab: free practice with no life cost and no campaign rewards.</li><li>Relic Run: draft powers across a five-board run.</li></ul>')
    press += section("Current artwork and real gameplay", '<p>Use these supplied images and footage when covering GemGame. Screenshots include normally earned progress, not the initial player state. Please keep the gameplay accurate and credit GemGame / George Wall.</p><ul>' + ''.join(f'<li><a href="../{ASSETS}{n}.jpg">{escape(a)} — screenshot</a></li>' for n,a in SHOTS) + f'<li><a href="../{ASSETS}icon.png">App icon</a></li><li><a href="../{ASSETS}preview.mp4">24-second gameplay preview</a></li></ul>')
    press += section("Contact the developer", '<p>For coverage, questions or review requests: <a href="mailto:georgewall1991@icloud.com">georgewall1991@icloud.com</a>.</p>')
    render("press/", "GemGame Press Kit — Facts, Screenshots and Gameplay", "GemGame press kit: current iPhone gameplay, screenshots, app icon, accurate feature and purchase details, and independent developer George Wall's contact.", "A small game.<br>A world of little moments.", "Facts, current artwork and real gameplay for people writing about GemGame.", press)
    print("Built six English GemGame acquisition pages")


if __name__ == "__main__":
    build()
