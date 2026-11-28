# Databricks notebook source
# Weekly bronze run: load files landed today. See docs/runbooks/bronze.md.
import os
import sys

# Make the repo's src/ folder importable (this notebook sits in notebooks/).
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "..", "src")))

from leviathan.bronze.load import run

summary = run(spark)
print(summary)
