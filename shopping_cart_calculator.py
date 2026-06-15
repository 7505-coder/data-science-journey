# ============================================
#     SHOPPING CART CALCULATOR
#   Concepts: Variables, Strings, Lists,
#             Tuples, Conditionals, Loops
# ============================================

# ---------- Chapter 1: Variables & Data Types ----------
store_name = "Python Mart"
discount_rate_10 = 0.10   # 10% discount if total > 500
discount_rate_20 = 0.20   # 20% discount if total > 1000
total = 0.0
item_count = 0

# ---------- Chapter 3: Lists & Tuples ----------
cart_items = []        # List to store item names (mutable)
cart_prices = []       # List to store item prices (mutable)
valid_categories = ("Food", "Electronics", "Clothing", "Other")  # Tuple (fixed)

# ---------- Chapter 2: Strings ----------
print("=" * 45)
print(f"   Welcome to {store_name}! 🛒")
print("=" * 45)
print(f"Available Categories: {', '.join(valid_categories)}")
print()

# ---------- Chapter 5: While Loop ----------
while True:
    item_name = input("Enter item name (or 'done' to finish): ").strip()

    # ---------- Chapter 2: String Methods ----------
    if item_name.lower() == "done":
        break

    if item_name == "":
        print("Item name can't be empty. Try again.\n")
        continue     # Chapter 5: continue statement

    try:
        item_price = float(input(f"Enter price of '{item_name}': ₹ "))
    except ValueError:
        print("Invalid price. Please enter a number.\n")
        continue

    # Add to lists
    cart_items.append(item_name.title())   # String method: .title()
    cart_prices.append(item_price)
    item_count += 1
    print(f"{item_name.title()} added to cart!\n")

# ---------- Edge Case ----------
if item_count == 0:
    print("\n🛒 Your cart is empty. Nothing to calculate!")
else:
    print("\n" + "=" * 45)
    print("           YOUR BILL SUMMARY")
    print("=" * 45)

    # ---------- Chapter 5: For Loop ----------
    for i in range(len(cart_items)):
        print(f"  {i+1}. {cart_items[i]:<20} ₹ {cart_prices[i]:.2f}")
        total += cart_prices[i]

    print("-" * 45)

    # ---------- Chapter 4: Conditionals ----------
    if total > 1000:
        discount = total * discount_rate_20
        print(f"     Subtotal:              ₹ {total:.2f}")
        print(f"     Discount (20%):       -₹ {discount:.2f}")
    elif total > 500:
        discount = total * discount_rate_10
        print(f"     Subtotal:              ₹ {total:.2f}")
        print(f"     Discount (10%):       -₹ {discount:.2f}")
    else:
        discount = 0
        print(f"  Subtotal:                ₹ {total:.2f}")
        print(f"  (No discount — spend ₹500+ to unlock!)")

    final_total = total - discount

    print("=" * 45)
    print(f"    TOTAL ITEMS : {item_count}")
    print(f"    FINAL TOTAL : ₹ {final_total:.2f}")
    print("=" * 45)
    print(f"\n  Thank you for shopping at {store_name}! ")
    print("  See you again!\n")
