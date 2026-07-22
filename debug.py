import os

print("--- DEBUGGING PATHS ---")
current_folder = os.getcwd()
print(f"Current Working Directory: {current_folder}")

templates_folder = os.path.join(current_folder, 'templates')

if os.path.exists(templates_folder):
    print("✅ 'templates' folder FOUND.")
    files = os.listdir(templates_folder)
    print(f"Files inside templates: {files}")
    
    if 'register.html' in files:
        print("✅ 'register.html' FOUND inside templates.")
    else:
        print("❌ 'register.html' is MISSING from templates folder.")
else:
    print("❌ 'templates' folder NOT FOUND. Please create it.")