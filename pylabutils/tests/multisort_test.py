from pylabutils.utils.operate import multisort

g = [5, 3, 1, 6, 4, 2]
d1 = [10, 11, 12, 13, 14, 15]
d2 = [0, 0, 1, 1, 2, 2]

print(
    " Starting lists:\n",
    "{} = {}\n".format('guide', g),
    "{} = {}\n".format('data1', d1),
    "{} = {}\n".format('data2', d2),
)

print(" Executing:\n" \
    "multisort(guide, data1, data2, include_guide = True, inplace = True)\n")
multisort(g, d1, d2, include_guide = True, inplace = True)

print(
    "\n Results:\n",
    "{} = {}\n".format('guide', g),
    "{} = {}\n".format('data1', d1),
    "{} = {}\n".format('data2', d2),
)

print(" Reassigning variables to starting values...\n")
g = [5, 3, 1, 6, 4, 2]
d1 = [10, 11, 12, 13, 14, 15]
d2 = [0, 0, 1, 1, 2, 2]

print(
    " Creating new variable:\n",
    "data = [data1, data2]\n",
)
d = [d1, d2]

print(
    " Executing:\nsorted_data1, sorted_data2 =",
    "multisort(guide, data, include_guide = False, inplace = False)\n"
)
sd1, sd2 = multisort(g, d, include_guide = False, inplace = False)

print(
    "\n Results:\n",
    "{} = {}\n".format('sorted_data1', sd1),
    "{} = {}\n".format('sorted_data2', sd2),
)
