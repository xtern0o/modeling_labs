import matplotlib.pyplot as plt
import numpy as np


def plot_deviations(deviations, sizes):
    for name, values in deviations.items():
        plt.plot(sizes, values, marker="o", label=name)

    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(sizes)
    plt.xlabel("Размер выборки")
    plt.ylabel("Отклонение от n=300, %")
    plt.grid()
    plt.legend()
    plt.savefig("out/deviations.svg", bbox_inches="tight")
    plt.show()


def plot_sequence(x, filename="sequence"):
    plt.figure()
    plt.plot(range(1, len(x) + 1), x, marker="o", markersize=3)
    plt.xlabel("i")
    plt.ylabel("значение x_i")
    plt.grid()
    plt.savefig(f"out/{filename}.svg", bbox_inches="tight")
    plt.show()


def plot_autocorrelation(autocorrelations):
    lags = list(autocorrelations)
    values = list(autocorrelations.values())

    plt.figure(figsize=(8, 4))
    plt.stem(lags, values, basefmt=" ")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(lags)
    plt.xlabel("Сдвиг")
    plt.ylabel("Коэффициент автокорреляции")
    plt.grid(axis="y", alpha=0.3)
    plt.savefig("out/autocorrelation.svg", bbox_inches="tight")
    plt.show()


def plot_histogram(x, log=False):
    bins = int(np.ceil(np.sqrt(len(x))))
    plt.figure(figsize=(8, 4))
    plt.hist(x, bins=bins, edgecolor="black")

    if log:
        plt.yscale("log")

    plt.xlabel("Значение")
    plt.ylabel("Частота")
    plt.grid(axis="y", alpha=0.3)
    plt.savefig(
        f"out/histogram{'_log' if log else ''}.svg",
        bbox_inches="tight",
    )
    plt.show()

def plot_distribution_fit(x, p, lambda1, lambda2):
    bins = int(np.ceil(np.sqrt(len(x))))
    values = np.linspace(0, np.max(x), 1000)
    density = (
        p * lambda1 * np.exp(-lambda1 * values)
        + (1 - p) * lambda2 * np.exp(-lambda2 * values)
    )

    plt.figure(figsize=(8, 4))
    plt.hist(
        x,
        bins=bins,
        density=True,
        alpha=0.6,
        edgecolor="black",
        label="Исходные данные",
    )
    plt.plot(
        values,
        density,
        linewidth=2,
        label="Гиперэкспоненциальная плотность",
    )
    plt.xlabel("Значение")
    plt.ylabel("Плотность")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig("out/distribution_fit.svg", bbox_inches="tight")
    plt.show()



def plot_autocorrelation_comparison(original, generated):
    lags = list(original)

    plt.figure(figsize=(8, 4))
    plt.plot(lags, original.values(), marker="o", label="Исходная")
    plt.plot(lags, generated.values(), marker="o", label="Сгенерированная")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(lags)
    plt.xlabel("Сдвиг")
    plt.ylabel("Коэффициент автокорреляции")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig("out/autocorrelation_comparison.svg", bbox_inches="tight")
    plt.show()