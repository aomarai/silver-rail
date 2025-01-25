from stats.models import Stat

# Derive DEFAULT_STATS by including the category for each stat type
DEFAULT_STATS = [
    {"stat_type": stat_type[0], "stat_category": category, "value": 0}
    for category, category_stats in {
        "base": Stat.STAT_TYPES[:4],  # Base stats
        "advanced": Stat.STAT_TYPES[4:12],  # Advanced stats
        "damage": Stat.STAT_TYPES[12:19],  # Damage types
        "resistance": Stat.STAT_TYPES[19:],  # Resistance types
    }.items()
    for stat_type in category_stats
]
