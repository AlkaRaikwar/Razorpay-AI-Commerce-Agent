from app.agent.tool_registry import get_tool


print("TEST 1:")
tool = get_tool("search_products")
print(tool("running shoes"))

print("\nTEST 2:")
tool = get_tool("check_stock")
print(tool("shoe-001"))

print("\nTEST 3:")
tool = get_tool("unknown_tool")
print(tool)