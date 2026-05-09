#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend/app/services')
from health_aggregator import aggregator
import json

r = aggregator.get_full_health()
print(f"Overall Score: {r['overall_score']}")
print(f"Memory Score: {r['systems']['memory']['score']}")
print(f"Skills Score: {r['systems']['skills']['score']}")
print(f"Self-loop Score: {r['systems']['ai_self_loop']['score']}")
print("\nFull data:")
print(json.dumps(r, indent=2, ensure_ascii=False))