import requests
from django.core.management.base import BaseCommand

# Set your domain here
SITE_DOMAIN = "http://example.com"

class LiteSpeedCache:
    def __init__(self):
        self.stale_key = ""

    def purge(self, items: str, stale: bool = True):
        """Send a PURGE request to LiteSpeed server."""
        if stale:
            self.stale_key = "stale,"
        headers = {"X-LiteSpeed-Purge": f"{self.stale_key}{items}"}
        response = requests.request("PURGE", SITE_DOMAIN + "/", headers=headers)
        return response.status_code, response.text

    def purge_all(self, stale: bool = True):
        return self.purge("*", stale)

    def purge_tags(self, tags: list, stale: bool = True):
        if tags:
            items = ",".join(f"tag={tag}" for tag in tags)
            return self.purge(items, stale)
        return None, "No tags provided"

    def purge_items(self, items: list, stale: bool = True):
        if items:
            return self.purge(",".join(items), stale)
        return None, "No items provided"


class Command(BaseCommand):
    help = "Purge LiteSpeed cache (all, by tags, or by items)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Purge all cache"
        )
        parser.add_argument(
            "--tags",
            nargs="+",
            help="Purge cache by tags (space-separated list)"
        )
        parser.add_argument(
            "--items",
            nargs="+",
            help="Purge cache by specific items (space-separated URLs)"
        )
        parser.add_argument(
            "--stale",
            action="store_true",
            help="Mark purged cache as stale"
        )

    def handle(self, *args, **options):
        lscache = LiteSpeedCache()
        stale = options["stale"]

        if options["all"]:
            status, text = lscache.purge_all(stale)
            self.stdout.write(f"Purged all cache, status {status}")
        elif options["tags"]:
            status, text = lscache.purge_tags(options["tags"], stale)
            self.stdout.write(f"Purged tags {options['tags']}, status {status}")
        elif options["items"]:
            status, text = lscache.purge_items(options["items"], stale)
            self.stdout.write(f"Purged items {options['items']}, status {status}")
        else:
            self.stdout.write("No purge option specified. Use --all, --tags, or --items")
