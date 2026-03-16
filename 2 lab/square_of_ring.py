import math


def compute_square(external_ring_rad: int, internal_ring_rad: int) -> str:
    square_of_ring = math.pi * (external_ring_rad ** 2 - internal_ring_rad ** 2)

    return f"Площадь кольца с радиусами {external_ring_rad} и {internal_ring_rad} = {round(square_of_ring, 2)}"


def main():
    external_ring_rad = int(input("Введите внешний радиус кольца: "))
    internal_ring_rad = int(input("Введите внутренний радиус кольца: "))

    print(compute_square(external_ring_rad, internal_ring_rad))


if __name__ == "__main__":
    main()