if input("Open in interactive mode?\n") in 'yes': import time;
from pylabutils.numfit.methods import simple_fit
try:
    from pylabutils.utils.operate import multisort
    multisort_imported = True
except:
    print("could not import multisort")
exec("try: time.sleep(1)\nexcept NameError: pass")

print("\nLoading data from a real laboratory experiment!")

exp_phase = [0, 5.90, 10.0, 16.5, 20.0, 25.5, 33.0, 35.0, 42.5, 46.0,
    51.0, 55.0, 61.0, 65.0, 69.0, 75.0, 355.0, 350.5, 344.0, 341.5,
    334.5, 330.0, 324.0, 320.5, 315.0, 309.0, 305.5, 299.5, 295.0,
    290.0, 284.5, 281.0, 276.0] #degrees
freq = [5.07, 5.16, 5.22, 5.30, 5.37, 5.43, 5.62, 5.66, 5.81, 5.89,
    6.09, 6.22, 6.52, 6.85, 7.82, 9.41, 5.03, 4.97, 4.91, 4.86,
    4.79, 4.73, 4.66, 4.55, 4.45, 4.39, 4.29, 4.04, 3.89, 3.68,
    3.33, 3.14, 2.29] #KHz
exec("try: time.sleep(1)\nexcept NameError: pass")

print("Experimental phases: {0}, ..., {1}".format(
    str(exp_phase[:4])[:-1], str(exp_phase[len(exp_phase)-4:])[1:]))
exec("try: time.sleep(1)\nexcept NameError: pass")

print("Frequencies: {0}, ..., {1}".format(
    str(freq[:4])[:-1], str(freq[len(freq)-4:])[1:]))
exec("try: time.sleep(2)\nexcept NameError: pass")

print("Added experimental uncertainties...")
sexp_phase = [5.5] * len(exp_phase)
sfreq = [0.01] * len(freq)
exec("try: time.sleep(2)\nexcept NameError: pass")

print("(increased their values for graphing purposes :-))")
exec("try: time.sleep(2)\nexcept NameError: pass")

print("Sorting the data so everything runs fine...")
exec("try: time.sleep(2)\nexcept NameError: pass")
if multisort_imported == True:
    try:
        multisort(exp_phase, freq, include_guide = True, inplace = True)
    except:
        print("there was an error utilizing multisort function.")
exec("try: time.sleep(2)\nexcept NameError: pass")

print("Starting the tests...")
exec("try: time.sleep(2)\nexcept NameError: pass")

print("Test, part 1:")
exec("try: time.sleep(1)\nexcept NameError: pass")
print("Executing:\n")
exec("try: time.sleep(1)\nexcept NameError: pass")
print("""simple_fit('phase = {A} * np.exp([frequency])', freq, exp_phase,
    yerr = sexp_phase, graph = True, split = False)\n""")
exec("try: time.sleep(2)\nexcept NameError: pass")
simple_fit('phase = {A} * np.exp([frequency])', freq, exp_phase,
    yerr = sexp_phase, graph = True, split = False)
exec("try: time.sleep(2)\nexcept NameError: pass")

go = input("Continue? y/n\n")
exec("try: time.sleep(1)\nexcept NameError: pass")

if go in ['y', 'yes']:
    print("\nTest, part 2:")
    exec("try: time.sleep(1)\nexcept NameError: pass")
    print("Executing:\n")
    exec("try: time.sleep(1)\nexcept NameError: pass")
    print("""simple_fit('y = {A} * np.sin({B} + x/{C})', exp_phase, freq,
        yerr =  sfreq, beta0 = [5, 20, 400], size = (12, 8), graph = True,
        split = False, colors = ['orange', 'purple', 'yellow'])\n""")
    exec("try: time.sleep(2)\nexcept NameError: pass")
    simple_fit('y = {A} * np.sin({B} + x/{C})', exp_phase, freq,
        yerr =  sfreq, beta0 = [5, 20, 400], size = (12, 8), graph = True,
        split = True, colors = ['orange', 'purple', 'yellow'])
