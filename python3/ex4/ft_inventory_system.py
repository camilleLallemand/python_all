#!/usr/bin/env python3

import sys


def parse_inventory(args) -> dict[str, int]:
    inventory = {}
    for arg in args:
        if ':' not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue
        item, qty_str = arg.split(':', 1)
        if item in inventory:
            print(f"Redundant item '{item}' - discarding")
            continue
        try:
            qty = int(qty_str)
        except ValueError as e:
            print(f"Quantity error for '{item}': {e}")
            continue
        inventory[item] = qty
    return inventory


def display_inventory(inventory):
    print(f"Got inventory: {inventory}")
    items = list(inventory.keys())
    print(f"Item list: {items}")
    total_qty = sum(inventory.values())
    print(f"Total quantity of the {len(items)} items: {total_qty}")
    for item in items:
        percent = round(inventory[item] / total_qty * 100, 1)
        print(f"Item {item} represents {percent}%")
    max_qty = max(inventory.values())
    min_qty = min(inventory.values())
    most_item = next(k for k, v in inventory.items() if v == max_qty)
    least_item = next(k for k, v in inventory.items() if v == min_qty)
    print(f"Item most abundant: {most_item} with quantity {max_qty}")
    print(f"Item least abundant: {least_item} with quantity {min_qty}")
    inventory['magic_item'] = 1
    print(f"Updated inventory: {inventory}")


def main():
    print("=== Inventory System Analysis ===")
    if len(sys.argv) < 2:
        print("Usage: python3 ft_inventory_system.py "
              "item1:qty1 item2:qty2 ...")
        return
    args = sys.argv[1:]
    inventory = parse_inventory(args)
    if not inventory:
        print("No valid items to display.")
        return
    display_inventory(inventory)


if __name__ == "__main__":
    main()
