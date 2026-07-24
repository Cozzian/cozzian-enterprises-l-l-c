import os
f = 'competitive_intel_report.html'
size = os.path.getsize(f)
print(f"File: {f}")
print(f"Size: {size:,} bytes ({size/1024:.1f} KB)")