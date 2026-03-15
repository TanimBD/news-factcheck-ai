from backend.agent.factcheck_agent import factcheck_claim

while True:

    claim = input("Enter claim: ")

    result = factcheck_claim(claim)

    print(result)