"""Top 40 VC firms to monitor for portfolio company activities that may compete with Guidewire."""

VC_FIRMS = [
    # Tier 1 — Global generalist (large enough to back any insurtech)
    {"name": "Sequoia Capital",            "website": "sequoiacap.com",          "blog": "https://www.sequoiacap.com/stories/",              "insurtech_focus": False},
    {"name": "Andreessen Horowitz",        "website": "a16z.com",                "blog": "https://a16z.com/tag/insurance/",                   "insurtech_focus": False},
    {"name": "Accel",                      "website": "accel.com",               "blog": "https://www.accel.com/noteworthy",                  "insurtech_focus": False},
    {"name": "Benchmark",                  "website": "benchmark.com",           "blog": None,                                               "insurtech_focus": False},
    {"name": "Kleiner Perkins",            "website": "kleinerperkins.com",      "blog": "https://www.kleinerperkins.com/stories/",           "insurtech_focus": False},
    {"name": "Greylock Partners",          "website": "greylock.com",            "blog": "https://greylock.com/greymatter/",                  "insurtech_focus": False},
    {"name": "Index Ventures",             "website": "indexventures.com",       "blog": "https://www.indexventures.com/perspectives/",       "insurtech_focus": False},
    {"name": "General Catalyst",           "website": "generalcatalyst.com",     "blog": "https://www.generalcatalyst.com/perspectives/",     "insurtech_focus": False},
    {"name": "New Enterprise Associates",  "website": "nea.com",                 "blog": "https://www.nea.com/blog/",                        "insurtech_focus": False},
    {"name": "Lightspeed Venture Partners","website": "lsvp.com",               "blog": "https://lsvp.com/stories/",                        "insurtech_focus": False},
    {"name": "Bessemer Venture Partners",  "website": "bvp.com",                 "blog": "https://www.bvp.com/blog/",                        "insurtech_focus": True},
    {"name": "Battery Ventures",           "website": "battery.com",             "blog": "https://www.battery.com/research/",                 "insurtech_focus": False},
    {"name": "IVP",                        "website": "ivp.com",                 "blog": "https://www.ivp.com/news/",                        "insurtech_focus": False},
    {"name": "Founders Fund",              "website": "foundersfund.com",        "blog": None,                                               "insurtech_focus": False},
    {"name": "Tiger Global Management",    "website": "tigerglobal.com",         "blog": None,                                               "insurtech_focus": False},
    {"name": "Coatue Management",          "website": "coatue.com",              "blog": None,                                               "insurtech_focus": False},
    {"name": "Insight Partners",           "website": "insightpartners.com",     "blog": "https://www.insightpartners.com/ideas/",            "insurtech_focus": True},
    {"name": "GV (Google Ventures)",       "website": "gv.com",                  "blog": "https://www.gv.com/updates/",                      "insurtech_focus": False},
    {"name": "Khosla Ventures",            "website": "khoslaventures.com",      "blog": "https://www.khoslaventures.com/khosla-perspective/","insurtech_focus": False},
    {"name": "First Round Capital",        "website": "firstround.com",          "blog": "https://review.firstround.com/",                   "insurtech_focus": False},
    {"name": "Spark Capital",              "website": "sparkcapital.com",        "blog": "https://www.sparkcapital.com/blog",                 "insurtech_focus": False},
    {"name": "TCV",                        "website": "tcv.com",                 "blog": "https://www.tcv.com/writing/",                     "insurtech_focus": True},
    {"name": "8VC",                        "website": "8vc.com",                 "blog": "https://8vc.com/resources/",                       "insurtech_focus": False},
    {"name": "Union Square Ventures",      "website": "usv.com",                 "blog": "https://www.usv.com/writing/",                     "insurtech_focus": False},
    {"name": "SoftBank Vision Fund",       "website": "sbvisionfund.com",        "blog": None,                                               "insurtech_focus": False},

    # Insurtech / Fintech focused
    {"name": "Ribbit Capital",             "website": "ribbitcap.com",           "blog": None,                                               "insurtech_focus": True},
    {"name": "QED Investors",              "website": "qedinvestors.com",        "blog": "https://qedinvestors.com/blog/",                   "insurtech_focus": True},
    {"name": "Anthemis Group",             "website": "anthemis.com",            "blog": "https://www.anthemis.com/insights/",               "insurtech_focus": True},
    {"name": "IA Capital Group",           "website": "iacapitalgroup.com",      "blog": None,                                               "insurtech_focus": True},
    {"name": "Munich Re Ventures",         "website": "munichre.com/ventures",   "blog": None,                                               "insurtech_focus": True},
    {"name": "MS&AD Ventures",             "website": "msad-ventures.com",       "blog": None,                                               "insurtech_focus": True},
    {"name": "Nationwide Ventures",        "website": "nationwide.com/ventures", "blog": None,                                               "insurtech_focus": True},
    {"name": "Aquiline Capital Partners",  "website": "aquiline.com",            "blog": None,                                               "insurtech_focus": True},
    {"name": "XL Innovate",               "website": "xlinnovate.com",           "blog": None,                                               "insurtech_focus": True},
    {"name": "Mundi Ventures",             "website": "mundiventures.com",       "blog": "https://mundiventures.com/blog/",                  "insurtech_focus": True},

    # International
    {"name": "DST Global",                 "website": "dst.global",              "blog": None,                                               "insurtech_focus": False},
    {"name": "Atomico",                    "website": "atomico.com",             "blog": "https://www.atomico.com/blog/",                    "insurtech_focus": False},
    {"name": "Balderton Capital",          "website": "balderton.com",           "blog": "https://www.balderton.com/grow/",                  "insurtech_focus": False},
    {"name": "Northzone",                  "website": "northzone.com",           "blog": "https://northzone.com/blog/",                      "insurtech_focus": False},
    {"name": "LocalGlobe",                 "website": "localglobe.vc",           "blog": "https://medium.com/localglobe-notes",              "insurtech_focus": False},
]

# Build a flat list of VC names for prompt construction
VC_NAMES = [f["name"] for f in VC_FIRMS]
INSURTECH_FOCUSED_VCS = [f["name"] for f in VC_FIRMS if f["insurtech_focus"]]
