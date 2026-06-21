import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


def macaulay(x, a, power):
    return np.where(x >= a, (x-a)**power, 0.0)


def main():

    print("="*60)
    print("       BEAM DEFLECTION SOLVER - MACAULAY METHOD")
    print("="*60)


    # Beam type
    print("\n1. Simply Supported")
    print("2. Cantilever")
    print("3. Overhanging")

    choice = input("Choose: ").strip()

    if choice not in ['1','2','3']:
        return


    # Material
    E = float(input("\nYoung's modulus E (GPa): ")) * 1e9

    width = float(input("Width b (mm): ")) / 1000
    height = float(input("Height h (mm): ")) / 1000

    I = width * height**3 / 12
    EI = E * I

    print(f"\nI = {I:.4e} m^4")


    # Geometry

    L = float(input("\nBeam length (m): "))

    a = 0
    b = L

    if choice == '3':

        a = float(input("Left support position: "))
        b = float(input("Right support position: "))


    # Loads

    n = int(input("\nNumber of point loads: "))

    loads=[]

    for i in range(n):

        pos=float(input(f"Load {i+1} position (m): "))
        P=float(input(f"Load {i+1} magnitude (N downward): "))

        loads.append((pos,P))


    # Reactions

    RA=RB=0
    MA=0


    if choice == '2':

        RA=sum(P for _,P in loads)

        # FIXED MOMENT
        MA=sum(P*x for x,P in loads)


        print("\nFixed reaction")
        print(f"Force = {RA/1000:.3f} kN")
        print(f"Moment = {MA/1000:.3f} kNm")


    else:

        total=sum(P for _,P in loads)

        moment=sum(
            P*(x-a)
            for x,P in loads
        )

        RB=moment/(b-a)

        RA=total-RB


        print("\nSupport reactions")
        print(f"RA = {RA/1000:.3f} kN")
        print(f"RB = {RB/1000:.3f} kN")



    # Macaulay equation

    def beam_eq(x):

        slope=np.zeros_like(x)
        y=np.zeros_like(x)


        # Point loads

        for pos,P in loads:

            slope += -P/2*macaulay(x,pos,2)

            y += -P/6*macaulay(x,pos,3)



        # Cantilever reactions

        if choice=='2':

            slope += MA*macaulay(x,0,1)

            y += MA/2*macaulay(x,0,2)


            slope += RA/2*macaulay(x,0,2)

            y += RA/6*macaulay(x,0,3)



        else:

            slope += RA/2*macaulay(x,a,2)

            y += RA/6*macaulay(x,a,3)


            slope += RB/2*macaulay(x,b,2)

            y += RB/6*macaulay(x,b,3)


        return slope,y



    # Boundary constants

    if choice=='2':

        C1=0
        C2=0


    else:

        _,ya=beam_eq(np.array([a]))
        _,yb=beam_eq(np.array([b]))


        A=np.array([
            [a,1],
            [b,1]
        ])

        B=np.array([
            -ya[0],
            -yb[0]
        ])


        C1,C2=np.linalg.solve(A,B)



    # Solve

    x=np.linspace(0,L,5000)

    _,raw=beam_eq(x)

    # IMPORTANT:
    # downward = negative y
    y=(raw+C1*x+C2)/EI



    max_i=np.argmax(abs(y))

    print("\nMaximum deflection:")
    print(
        f"{y[max_i]*1000:.5f} mm "
        f"at x={x[max_i]:.3f} m"
    )



    # Table

    print("\nDeflection table")

    xt=np.linspace(0,L,11)

    _,yt=beam_eq(xt)

    yt=(yt+C1*xt+C2)/EI


    table=[]

    for X,Y in zip(xt,yt):

        table.append(
            [
                f"{X:.2f}",
                f"{Y*1000:.4f}"
            ]
        )


    print(
        tabulate(
            table,
            headers=["x(m)","Deflection(mm)"],
            tablefmt="grid"
        )
    )



    # Plot

    plt.figure(figsize=(11,6))


    plt.plot(
        x,
        y*1000,
        linewidth=2.5,
        label="Elastic curve"
    )


    plt.axhline(
        0,
        linestyle="--",
        linewidth=1,
        label="Original beam"
    )


    # Supports

    if choice!='2':

        plt.plot(
            a,0,
            "^",
            markersize=12,
            label="Support"
        )

        plt.plot(
            b,0,
            "^",
            markersize=12
        )

    else:

        plt.axvline(
            0,
            linewidth=5,
            label="Fixed end"
        )



    # Loads

    arrow_height=max(abs(y))*0.5


    for pos,P in loads:

        plt.annotate(
            "",
            xy=(pos,0),
            xytext=(pos,arrow_height),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=2
            )
        )


        plt.text(
            pos,
            arrow_height*1.1,
            f"{P/1000:.2f} kN",
            ha="center",
            fontsize=10,
            weight="bold"
        )


    plt.title(
        "Beam Deflection Diagram",
        fontsize=14,
        weight="bold"
    )


    plt.xlabel("Position (m)")
    plt.ylabel("Deflection (mm)")

    plt.grid(True,linestyle=":")

    plt.legend()

    plt.tight_layout()

    plt.show()



if __name__=="__main__":
    main()