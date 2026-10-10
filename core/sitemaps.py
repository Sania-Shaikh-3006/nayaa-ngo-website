from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    def items(self):
        return ["home","about","work","projects","media","volunteer","partner","fundraise","campaigns","community","blog","contact","donate"]
    def location(self, item): return reverse(item)
