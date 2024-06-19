import ROOT
import argparse
import os

def extract_1d_histogram_data(histogram):
    # Extract the data from the 1D histogram
    n_bins = histogram.GetNbinsX()
    data = []

    for i in range(1, n_bins + 1):
        bin_center = histogram.GetBinCenter(i)
        bin_content = histogram.GetBinContent(i)
        bin_error = histogram.GetBinError(i)
        data.append((bin_center, bin_content, bin_error))

    return data

def extract_2d_histogram_data(histogram):
    # Extract the data from the 2D histogram
    n_bins_x = histogram.GetNbinsX()
    n_bins_y = histogram.GetNbinsY()
    data = []

    for i in range(1, n_bins_x + 1):
        for j in range(1, n_bins_y + 1):
            bin_center_x = histogram.GetXaxis().GetBinCenter(i)
            bin_center_y = histogram.GetYaxis().GetBinCenter(j)
            bin_content = histogram.GetBinContent(i, j)
            bin_error = histogram.GetBinError(i, j)
            data.append((bin_center_x, bin_center_y, bin_content, bin_error))

    return data

def save_1d_data_to_file(data, output_file):
    with open(output_file, 'w') as f:
        f.write("Bin Center\tBin Content\tBin Error\n")
        for bin_center, bin_content, bin_error in data:
            f.write(f"{bin_center}\t{bin_content}\t{bin_error}\n")

def save_2d_data_to_file(data, output_file):
    with open(output_file, 'w') as f:
        f.write("X\tY\tValue\tError\n")
        for bin_center_x, bin_center_y, bin_content, bin_error in data:
            f.write(f"{bin_center_x}\t{bin_center_y}\t{bin_content}\t{bin_error}\n")

def main():
    parser = argparse.ArgumentParser(description='Extract histogram data from a ROOT file and save to a text file.')
    parser.add_argument('rootfile', help='Path to the input ROOT file')
    parser.add_argument('histname', help='Name of the histogram')

    args = parser.parse_args()
    file_name = args.rootfile
    hist_name = args.histname

    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_name, "READ")

    # Check if the file is open
    if not root_file or root_file.IsZombie():
        print(f"Error: Could not open file {file_name}")
        return

    # Get the histogram from the file
    histogram = root_file.Get(hist_name)

    # Check if the histogram exists
    if not histogram:
        print(f"Error: Histogram {hist_name} not found in file {file_name}")
        root_file.Close()
        return

    # Determine the type of histogram and extract data accordingly
    data = None
    if isinstance(histogram, ROOT.TH1) and not isinstance(histogram, ROOT.TH2):
        data = extract_1d_histogram_data(histogram)
        output_file = f"{hist_name}_{os.path.splitext(os.path.basename(file_name))[0]}.txt"
        save_1d_data_to_file(data, output_file)
    elif isinstance(histogram, ROOT.TH2):
        data = extract_2d_histogram_data(histogram)
        output_file = f"{hist_name}_{os.path.splitext(os.path.basename(file_name))[0]}.txt"
        save_2d_data_to_file(data, output_file)
    else:
        print(f"Error: {hist_name} is not a recognized 1D or 2D histogram type")

    # Close the ROOT file
    root_file.Close()

    if data:
        print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
