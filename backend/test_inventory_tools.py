from app.tools.inventory_tools import check_stock


print("TEST 1:")
print(check_stock("shoe-001"))

print("\nTEST 2:")
print(check_stock("shoe-002"))

print("\nTEST 3:")
print(check_stock("unknown"))