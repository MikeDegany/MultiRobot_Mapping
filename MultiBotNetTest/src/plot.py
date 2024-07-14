#!/usr/bin/env python3

#Maintainer: Mike Degany (mike.degany@gmail.com)

# Copyright 2024 Mike Degany.
# Licensed under the Attribution-Only License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://example.com/license/attribution-only-v1.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import rclpy
from rclpy.node import Node
# from packets_msgs.msg import Packet
import matplotlib.pyplot as plt
from std_msgs.msg import String
import os
import signal
import seaborn as sns
import numpy as np
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from datetime import datetime
import json


def plot_jitter_profiles(output_folder, dict_of_lists):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for category, times in dict_of_lists.items():
        plt.figure()
        plt.scatter(range(len(times)), times, marker='o', color='b', alpha=0.5)
        plt.xlabel('Packet Index')
        plt.ylabel('Time Delay (sec)')
        plt.title(f'Jitter plot - Category {category}')

        # Calculate average time delay
        avg_delay = np.mean(times)

        # Plot average line
        plt.axhline(y=avg_delay, color='r', linestyle='--', label=f'Average: {avg_delay:.6f} sec')
        plt.legend()

        plt.savefig(os.path.join(output_folder, f'jitter_plot_category_{category}.pdf'), format='pdf')
        plt.close()


def generate_histogram(output_folder, latency_lists):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for Frequency, data in latency_lists.items():
        plt.figure(figsize=(10, 6))  # Adjust the figure size
        sns.set_theme(style="whitegrid")   # Set seaborn style

        # Plot histogram
        sns.histplot(data, bins=50, alpha=0.5, color='skyblue')

        # Add mean and standard deviation lines
        mean = np.mean(data)
        std_dev = np.std(data)
        plt.axvline(mean, color='r', linestyle='--', linewidth=2, label=f'Mean: {mean:.6f}')
        plt.axvline(mean - std_dev, color='g', linestyle='--', linewidth=2, label=f'Std Dev: {std_dev:.6f}')
        plt.axvline(mean + std_dev, color='g', linestyle='--', linewidth=2)

        # Add labels and title
        plt.xlabel('Latency (sec)', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)
        plt.title(f'Jitter Histogram - Frequency: {Frequency} Hz', fontsize=16)

        # Add legend
        plt.legend()

        # Save the plot
        plt.savefig(os.path.join(output_folder, f'jitter_histogram_Frequency_{Frequency}.pdf'), format='pdf')
        plt.close()

def plot_boxplot(output_folder, latency_lists):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # packet_loss_rates_trimmed = {key: value for i, (key, value) in enumerate(packet_loss_rates.items()) if i <= 2}

    latency_lists_trimmed = {key: value for key, value in latency_lists.items() if int(key) <= 500}
    latency_lists_trimmed = {key: [num for num in value if num <= 0.01] for key, value in latency_lists_trimmed.items()}

    data = [times for times in latency_lists_trimmed.values()]
    labels = list(latency_lists_trimmed.keys())

    # Set seaborn style
    sns.set_theme(style="whitegrid")

    # Plot boxplot
    plt.figure(figsize=(10, 6))  # Adjust the figure size
    sns.boxplot(data=data, palette="Set3")
    # Add labels and title
    plt.xlabel('Frequency', fontsize=14)
    plt.ylabel('Latency (sec)', fontsize=14)
    plt.title('Boxplot of Latency for Different Frequencies', fontsize=16)

    # Rotate x-axis labels for better readability
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=45)

    # Save the plot
    plt.savefig(os.path.join(output_folder, 'Jitter_Boxplot.pdf'), format='pdf')
    plt.close()


def plot_packet_loss(output_folder, packet_loss_rates):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    categories = packet_loss_rates.keys()
    loss_rates = packet_loss_rates.values()

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(categories, loss_rates, marker='o', linestyle='-')
    plt.title('Packet Loss Rates')
    plt.xlabel('Frequency (hz)')
    plt.ylabel('Loss Rate (%)')
    plt.xscale('log')  # Logarithmic scale for x-axis
    plt.grid(True, which="both", ls="--", alpha=0.5)
    # Annotate each point with its percentage value
    for category, loss_rate in zip(categories, loss_rates):
        plt.text(category, loss_rate, f'{loss_rate:.2f}%\n{category}', ha='right', va='bottom')
    # plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'packet_loss_vs_frequency.pdf'), format='pdf')  # Save figure
    plt.close()


def load_data(data_path):
    with open(data_path, 'r') as f:
        data = json.load(f)
    return data


def main():
    if sys.argv[1] is not None:
        data_path = sys.argv[1]
        packetloss_path = os.path.join(data_path, "Data/packet_loss_rates.json")
        latency_path = os.path.join(data_path, "Data/latency_lists.json")

        packet_loss_rates = load_data(packetloss_path)
        latency_lists = load_data(latency_path)
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # begining timestamp
        run_path = os.path.join("/home/Plots/", ts)

        boxplot_path = os.path.join(run_path, "boxplot")
        hists_path = os.path.join(run_path, "hists")
        plots_path = os.path.join(run_path, "plots")
        PLR_path = os.path.join(run_path, "PLR")
        Data_path = os.path.join(run_path, "Data")
        os.makedirs(boxplot_path)
        os.makedirs(hists_path)
        os.makedirs(plots_path)
        os.makedirs(PLR_path)
        os.makedirs(Data_path)
        generate_histogram(hists_path, latency_lists)
        plot_boxplot(boxplot_path, latency_lists)  # Call plot_boxplot function here
        plot_jitter_profiles(plots_path, latency_lists)
        # print("Packet Loss Rates:", packet_loss_rates)
        plot_packet_loss(PLR_path,packet_loss_rates)

    else:
        sys.exit("Please provide the path to the data folder")

if __name__ == '__main__':
    main()

