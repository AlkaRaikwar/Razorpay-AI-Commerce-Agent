from app.agent.agent import CommerceAgent


agent = CommerceAgent()


print("\nTEST 1:")
print(agent.run("running shoes under 1800"))


print("\nTEST 2:")
print(agent.run("shoe-001 ka stock batao"))


print("\nTEST 3:")
print(agent.run("shoe-002 ki details batao"))


print("\nTEST 4:")
print(agent.run("Hello"))