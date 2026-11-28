# Databricks notebook source
# Weekly landing run: discover, compare, land, record. See docs/runbooks/landing.md.
import os
import sys

# Make the repo's src/ folder importable (this notebook sits in notebooks/).
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "..", "src")))

from leviathan.landing.manifest import run

summary = run(spark)
print(summary)
