import numpy as np
import ccl

testdata = np.random.randint(2, size=(10, 10), dtype=np.uint8)

print("Testdata")
print(testdata)

# Run the data through the decision tree and
# provide provsional labels
cc = ccl.Lmanager( testdata )
for r, row in enumerate( testdata ):
    for c, col in enumerate( row ):
        if testdata[r, c] == 0:
            continue
        else:
            cc.decision_tree( testdata, r, c )

print("Provisional labels")
print(cc.labels_arr)

# Correct the provisional labels
# using the equivalence list
for r, row in enumerate( cc.labels_arr ):
    for c, col in enumerate( cc.labels_arr ):
        cc.labels_arr[r,c] = cc.equi_l[ cc.labels_arr[r,c] ]

print("Corrected labels")
print(cc.labels_arr)

print("Number of cluster:")
print( len(set(cc.equi_l))-1 )


ccl.cluster_analyzer(cc.equi_l, cc.labels_arr)

