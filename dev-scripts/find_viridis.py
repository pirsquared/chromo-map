import chromo_map as cm
import traceback

try:
    print("Looking for viridis in matplotlib catalog...")
    
    # Check all matplotlib categories
    for category in cm.cmaps.matplotlib.keys():
        if 'viridis' in cm.cmaps.matplotlib[category]:
            print(f"Found viridis in {category}")
            break
    else:
        print("viridis not found in any matplotlib category")
        
    # Check what's in each category
    print("\nAll categories and their first few items:")
    for category in cm.cmaps.matplotlib.keys():
        items = list(cm.cmaps.matplotlib[category].keys())
        print(f"{category}: {items[:5]}")
    
    # Check if viridis is in the general catalog
    print(f"\nViridis in cm.cmaps.all: {'viridis' in cm.cmaps.all}")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
