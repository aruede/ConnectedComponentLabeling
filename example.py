import numpy as np
import ccl

testdata = np.random.randint(2, size=(10, 10), dtype=np.uint8)

print("Testdata")
print(testdata)

# Run the data through the decision tree and
# provide provsional labels
ccc = ccl.Lmanager( testdata )
for r, row in enumerate( testdata ):
    for c, col in enumerate( row ):
        if testdata[r, c] == 0:
            continue
        else:
            ccc.decision_tree( testdata, r, c )

print("Provisional labels")
print(ccc.L_arr)

# Correct provisional labels
# using the equivalence list
for r, row in enumerate( ccc.L_arr ):
    for c, col in enumerate( ccc.L_arr ):
        ccc.L_arr[r,c] = ccc.E[ ccc.L_arr[r,c] ]

print("Corrected labels")
print(ccc.L_arr)
