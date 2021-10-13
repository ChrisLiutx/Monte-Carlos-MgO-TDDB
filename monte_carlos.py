import argparse

if __name__ == "__main__":
    print("Monte Carlos simulation of Magnesium Oxide time dependent dielectric breakdown")
    args = sys.argv
    if len(args) < 6:
        print("Needs at least 5 arguments")
    filedir = args[0]
    p_i = args[1]
    p_b = args[2]
    p_idid = args[3]
    p_idbd = args[4]
    p_bdbd = args[5]
    if len(args) >= 2:
        print(args[1])
        if args[1].isnumeric():
            ai = int(args[1])
        else:
            ai = args[1]
        if len(args) >= 3:
            graphics = (args[2] == "1")
            if len(args) >= 4:
                learn = (args[3] == "1")
                if len(args) >= 5:
                    notify = (args[4] == "1")
    run(ai, graphics, learn, notify)

else:
    print("Read Documentation")