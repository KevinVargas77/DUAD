all_set = set(range(1,11))
even = {2,4,6,8,10}
odd = {1,3,5,7,9}
union_eo = even.union(odd)
intersection_eo = even.intersection(odd)
diff_aso = all_set - odd 
comp_of_even = all_set - even
comp_odd_minus_all = all_set - (odd - all_set)

#Results
print("1) Even ∪ Odd =", union_eo)
print("2) Even ∩ Odd =", intersection_eo)
print("3) All - Odd  =", diff_aso)
print("4) C(Even)   =", comp_of_even)
print("5) C(Odd−All)=", comp_odd_minus_all)