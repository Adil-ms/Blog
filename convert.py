with open("backup_fixed.json", "r", encoding="utf-16") as f:
    content = f.read()

with open("backup_fixeds.json", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed JSON saved as backup_fixed.json")
