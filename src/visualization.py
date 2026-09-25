import matplotlib.pyplot as plt


def plot_prices(df, title, save_path):
    plt.figure(figsize=(12,5))

    for col in df.columns:
        plt.plot(df.index, df[col], label=col)

    plt.legend()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()