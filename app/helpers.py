import matplotlib.pyplot as plt
import mplfinance as mpf

from io import BytesIO
import base64
def plot_helper(df, window_size):
    
    # Create a figure and axes for the main plot
    plt.switch_backend('Agg')
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(15, 15))

    # Plot the main data on the first subplot
    ax1.plot(df[f'{window_size}_MA_Difference_Difference'], label=f'{window_size} Period MA Difference Difference', color='b')
    ax1.plot(df['Upper_Band'], label='Upper Band', color='g')
    ax1.plot(df['Lower_Band'], label='Lower Band', color='r')
    ax1.axhline(0, color='red', linestyle='--')
    ax1.set_ylabel('Difference Difference')
    ax1.legend(loc='upper left')

    # Plot the additional data on the second subplot
    ax2.plot(df['Difference'], label='Actual Difference', color='orange')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Actual Difference')
    ax2.legend(loc='upper right')
    ax2.grid(True)
    # Add marks for when the conditions are true on the bottom subplot
    ax2.scatter(df.index[df['position']==-1], df['Difference'][df['position']==-1], color='red', label='Outside Upper')
    ax2.scatter(df.index[df['position']==1], df['Difference'][df['position']==1], color='green', label='Outside Lower')
    
    ax2.plot(df[f'{window_size}_MA_Difference'], label=f'{window_size} Period MA Difference', color='b')

    ax3.plot((1+df['return']).cumprod(), label='Cumulative Return', color='green')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Cumulative Return')
    ax3.legend(loc='upper left')
    ax3.grid(True)

    # Adjust layout
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


def ml_plot_helper(df):
    # plot cumulative return
    plt.figure(figsize=(15, 7))
    plt.plot((df['return_strat']).cumprod(), label='Cumulative Return (Strategy)', color='green')
    plt.plot((df['return']).cumprod(), label='Cumulative Return (Buy & Hold)', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.legend(loc='upper left')
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data