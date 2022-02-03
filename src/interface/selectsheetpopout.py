import re

string = 'Frugtsalat m/druer , håndskåret i lage (3,2kg) - Økologsk'
print(re.sub(' - Økologisk', '', string))
