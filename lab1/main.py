import numpy as np

from data import data
from graphtools import *

SIZES = (10, 20, 50, 100, 200, 300)
Z_VALUES = {
    0.90: 1.645,
    0.95: 1.960,
    0.99: 2.576,
}

x = np.array(data)

def calculate_metrics(sample):
    n = len(sample)
    mean = np.mean(sample)
    variance = np.var(sample, ddof=1)
    std = np.sqrt(variance)

    return {
        "mean": mean,
        "variance": variance,
        "std": std,
        "variation": std / mean,
        "ci": {
            prob: z * std / np.sqrt(n)
            for prob, z in Z_VALUES.items()
        },
    }


results = {
    n: calculate_metrics(x[:n])
    for n in SIZES
}


# print result
for n, values in results.items():
    print(f"\nn = {n}")

    for name, value in values.items():
        if name == "ci":
            for probability, margin in value.items():
                print(f"{name}_{probability:.0%}: (+-){margin:.3f}")
        else:
            print(f"{name}: {value:.3f}")

print("\nОтносительное отклонение значений выборки от эталонного (n=300):")
reference = results[300]

deviations = {
    name: [
        (results[n][name] / reference[name] - 1) * 100
        for n in SIZES
    ]
    for name in ("mean", "variance", "std", "variation")
}

for probability in Z_VALUES:
    name = f"ci_{probability:.0%}"
    deviations[name] = [
        (results[n]["ci"][probability] / reference["ci"][probability] - 1) * 100
        for n in SIZES
    ]

for i, n in enumerate(SIZES):
    print(f"\nn = {n}")

    for name, values in deviations.items():
        print(f"{name}: {values[i]:+.3f}%")


# график для наглядности 
plot_deviations(deviations, SIZES)

# график значений последовательности
plot_sequence(x)

print("\n=== АВТОКОРЕЛЛЯЦИОННЫЙ АНАЛИЗ ===\n")


def autocorrelation(x, max_lag=10):
    centered = x - np.mean(x)
    denominator = np.sum(centered ** 2)

    result = {}

    for lag in range(1, max_lag + 1):
        numerator = np.sum(centered[:-lag] * centered[lag:])
        result[lag] = numerator / denominator

    return result


autocorrelations = autocorrelation(x)

for lag, value in autocorrelations.items():
    print(f"lag {lag}: {value:.3f}")

plot_autocorrelation(autocorrelations)

plot_histogram(x)
plot_histogram(x, log=True)

print("\n=== ВЫБОР АППРОКСИМИРУЮЩЕГО ЗАКОНА ===\n")

m1 = np.mean(x)
m2 = np.mean(x ** 2)
variance = m2 - m1 ** 2
std = np.sqrt(variance)
variation = std / m1

p = 0.5 * (1 + np.sqrt((variation ** 2 - 1) / (variation ** 2 + 1)))
lambda1 = 2 * p / m1
lambda2 = 2 * (1 - p) / m1

print(f"первый начальный момент: {m1:.3f}")
print(f"второй начальный момент: {m2:.3f}")
print(f"дисперсия: {variance:.3f}")
print(f"СКО: {std:.3f}")
print(f"коэффициент вариации: {variation:.3f}")
print("закон распределения: гиперэкспоненциальный")
print(f"p: {p:.3f}")
print(f"lambda1: {lambda1:.5f}")
print(f"lambda2: {lambda2:.5f}")

def generate_hyperexponential(n, p, lambda1, lambda2, seed=67):
    rng = np.random.default_rng(seed)
    rates = np.where(rng.random(n) < p, lambda1, lambda2)
    return -np.log(1 - rng.random(n)) / rates


generated = generate_hyperexponential(
    len(x), p, lambda1, lambda2
)

generated_results = {
    n: calculate_metrics(generated[:n])
    for n in SIZES
}

print("\n=== СГЕНЕРИРОВАННАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ ===")

for name, value in generated_results[300].items():
    if name != "ci":
        print(f"{name}: {value:.3f}")


# comparison

comparison = {
    n: {
        name: (
            generated_results[n][name] / results[n][name] - 1
        ) * 100
        for name in ("mean", "variance", "std", "variation")
    }
    for n in SIZES
}

generated_autocorrelations = autocorrelation(generated)

correlation = np.corrcoef(x, generated)[0, 1]

print(
    "\nКорреляция исходной и сгенерированной "
    f"последовательностей: {correlation:.3f}"
)

print("\n=== СРАВНЕНИЕ ХАРАКТЕРИСТИК ===")

for n in SIZES:
    print(f"\nn = {n}")

    for name, percent in comparison[n].items():
        value = generated_results[n][name]
        print(f"{name}: {value:.3f}, {percent:+.3f}%")

print("\n=== СРАВНЕНИЕ АВТОКОРРЕЛЯЦИИ ===")

for lag in autocorrelations:
    print(
        f"lag {lag}: "
        f"исходная {autocorrelations[lag]:+.3f}, "
        f"сгенерированная {generated_autocorrelations[lag]:+.3f}"
    )


plot_distribution_fit(x, p, lambda1, lambda2)
plot_sequence(generated, "generated_sequence")

plot_autocorrelation_comparison(
    autocorrelations,
    generated_autocorrelations,
)

test = generate_hyperexponential(
    100_000, p, lambda1, lambda2
)

test_mean = np.mean(test)
test_variance = np.var(test)
test_std = np.std(test)

print("\n=== ПРОВЕРКА ГЕНЕРАТОРА ===")
print(f"mean: {test_mean:.3f}")
print(f"variance: {test_variance:.3f}")
print(f"std: {test_std:.3f}")
print(f"variation: {test_std / test_mean:.3f}")