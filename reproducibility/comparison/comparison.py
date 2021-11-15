import random
import numpy as np
import umap
import phate
from sklearn.manifold import TSNE
from multiprocessing import Pool as ThreadPool
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

from scivae import VAE
import timeit


# pip install umap-learn phate
gene_id = 'entrezgene_id'
gene_name = 'external_gene_name'
input_dir = ''
output_dir = 'output_6/'


# -----------------------------------------------------------------------------------
#                         Set the input data space
# -----------------------------------------------------------------------------------


def get_input_data(df: pd.DataFrame, label_col: str):
    scaler = MinMaxScaler(copy=True)
    """ Here we define the data for the VAE we choose to log2 the signal """
    cols_bin = []
    tmp_df = pd.DataFrame()
    non_nan_df = df.copy()
    non_nan_df = non_nan_df.fillna(0)
    for c in df.columns:
        if 'H3K27me3' in c and 'signal' in c and 'brain' in c:
            v = np.log2(non_nan_df[c].values + 1)
            nn_min = np.nanmin(v)
            nn_max = np.nanmax(v)
            tmp_df[f'{c}_log2'] = (v-nn_min) / (nn_max - nn_min)
            cols_bin.append(f'{c}_log2')
        elif ('merged-rep' not in c) and ('log2FoldChange' in c or 'wt' in c or 'ko' in c):
            cols_bin.append(c)
            v = non_nan_df[c].values
            nn_min = np.nanmin(v)
            nn_max = np.nanmax(v)
            tmp_df[c] = (v-nn_min) / (nn_max - nn_min)
    vae_values = tmp_df[cols_bin].values
    vae_values = np.nan_to_num(vae_values)
    tmp_df[label_col] = df[label_col].values
    return vae_values, tmp_df, df[label_col].values


df_training = pd.read_csv(f'{input_dir}df-consistent_epi-2500_20210124.csv')  # Consistently affected
df_sig = pd.read_csv(f'{input_dir}df-significant_epi-2500_20210124.csv') # all affected genes

hist_metric = 'signal'
labels = df_training[gene_name].values

"""
--------------------------------------------------------
                    Merge replicates for vis
--------------------------------------------------------
"""

# Smooth out the columns in the data frame i.e. for the clones we only put in the mean of the two replicates
cols_to_merge = [c for c in df_training.columns if 'wt' in c or 'ko' in c]
i = 0
while (i < len(cols_to_merge)):
    df_training[f'{cols_to_merge[i][:-1]}_merged-rep'] = 0.5 * (df_training[cols_to_merge[i]].values +
                                                                df_training[cols_to_merge[i + 1]].values)
    print("merged", cols_to_merge[i], cols_to_merge[i + 1])
    i += 2

"""
--------------------------------------------------------
                     Merge sig. Dataset
--------------------------------------------------------
"""
cols_to_merge = [c for c in df_sig.columns if 'wt' in c or 'ko' in c]
i = 0
while (i < len(cols_to_merge)):
    df_sig[f'{cols_to_merge[i][:-1]}_merged-rep'] = 0.5 * (df_sig[cols_to_merge[i]].values +
                                                           df_sig[cols_to_merge[i + 1]].values)
    print("merged", cols_to_merge[i], cols_to_merge[i + 1])
    i += 2

# Do the same as we did in the paper
c_aff_input_values, caff_df_input, c_aff_gene_names = get_input_data(df_training, gene_name) # Consistently affected dataset
sig_input_values, sig_df_input, sig_gene_names = get_input_data(df_sig, gene_name) # Significantly affected dataset


def get_shallow_vae(values, num_nodes, r_seed):
    config = {'loss': {'loss_type': 'mse', 'distance_metric': 'mmd', 'mmd_weight': 1.0},
              'encoding': {'layers': []},
              'decoding': {'layers': []},
              'latent': {'num_nodes': num_nodes}, 'optimiser': {'params': {}, 'name': 'adam'},
              'seed': r_seed}  # ensure there is a random seed just like in UMAP and TSNE

    vae_shallow = VAE(values, values, ['l']*len(values), config, f'vae_{num_nodes}')
    vae_shallow.encode('default', epochs=100, batch_size=50)
    # Encode the same using the linear vae
    vae_data_shallow = vae_shallow.encode_new_data(values)
    return vae_data_shallow, vae_shallow


def get_deep_vae(values, num_nodes, r_seed):
    config = {'loss': {'loss_type': 'mse', 'distance_metric': 'mmd', 'mmd_weight': 1.0,
                       'mmcd_method': 'k'},
              'encoding': {'layers': [{'num_nodes': 64, 'activation_fn': 'selu'},
                                      {'num_nodes': 32, 'activation_fn': 'relu'}
                                      ]},
              'decoding': {'layers': [
                  {'num_nodes': 32, 'activation_fn': 'relu'},
                  {'num_nodes': 64, 'activation_fn': 'selu'}]},
              'latent': {'num_nodes': num_nodes}, 'optimiser': {'params': {}, 'name': 'adam'},
              'seed': r_seed}

    vae_mse = VAE(values, values, ['l']*len(values), config, f'runs')
    vae_mse.encode('default', epochs=100, batch_size=50)
    vae_data = vae_mse.encode_new_data(values)
    return vae_data, vae_mse


def run_compare(param):
    r_seed, num_nodes = param[0], param[1]
    random.seed(r_seed)
    np.random.seed(r_seed)

    # Time each tool
    times = []
    nodes = []
    tools = []
    datasets = []

    start = timeit.default_timer()
    # PHATE: Fit each of the models to the consistently affected dataset
    phate_op = phate.PHATE(n_components=num_nodes, random_state=r_seed)
    phate_data = phate_op.fit_transform(c_aff_input_values)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('PHATE')
    datasets.append('consistently affected')

    # UMAP
    start = timeit.default_timer()
    umap_op = umap.UMAP(n_components=num_nodes, random_state=r_seed, transform_seed=r_seed)
    umap_data = umap_op.fit_transform(c_aff_input_values)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('UMAP')
    datasets.append('consistently affected')

    # PCA
    start = timeit.default_timer()
    pca_op = PCA(n_components=num_nodes)
    pca_data = pca_op.fit_transform(c_aff_input_values) # Doesn't enable for fit transform
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('PCA')
    datasets.append('consistently affected')

    # Run on each VAE
    start = timeit.default_timer()
    deep_vae_data, d_vae = get_deep_vae(c_aff_input_values, num_nodes, r_seed)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('Deep VAE')
    datasets.append('consistently affected')

    start = timeit.default_timer()
    shallow_vae_data, s_vae = get_shallow_vae(c_aff_input_values, num_nodes, r_seed)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('Shallow VAE')
    datasets.append('consistently affected')

    # tSNE
    start = timeit.default_timer()
    if num_nodes == 3:
        tsne_op = TSNE(n_components=num_nodes, random_state=r_seed)
    else:
        tsne_op = TSNE(n_components=num_nodes, random_state=r_seed, method='exact')
    tsne_data = tsne_op.fit_transform(c_aff_input_values)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('tSNE')
    datasets.append('consistently affected')

    # Save to csv file
    caff_df = pd.DataFrame()
    caff_df['external_gene_name'] = c_aff_gene_names
    for i in range(0, num_nodes):
        caff_df[f'VAE_deep_{i}'] = deep_vae_data[:, i]
        caff_df[f'VAE_lin_{i}'] = shallow_vae_data[:, i]
        caff_df[f'PCA_{i}'] = pca_data[:, i]
        caff_df[f'UMAP_{i}'] = umap_data[:, i]
        caff_df[f'PHATE_{i}'] = phate_data[:, i]
        caff_df[f'tSNE_{i}'] = tsne_data[:, i]

    # Save to csv for later
    caff_df.to_csv(f'{output_dir}caff_{num_nodes}_{r_seed}.csv', index=False)
    print(f'Done consistently affected {num_nodes} {r_seed}')

    # Do the same on the significantly affected dataset
    # PHATE: Fit each of the models to the consistently affected dataset
    start = timeit.default_timer()
    phate_op = phate.PHATE(n_components=num_nodes, random_state=r_seed)
    phate_data = phate_op.fit_transform(sig_input_values)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('PHATE')
    datasets.append('Significantly affected')

    # UMAP
    start = timeit.default_timer()
    umap_op = umap.UMAP(n_components=num_nodes, random_state=r_seed, transform_seed=r_seed)
    umap_data = umap_op.fit_transform(sig_input_values)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('UMAP')
    datasets.append('Significantly affected')

    # PCA
    start = timeit.default_timer()
    pca_op = PCA(n_components=num_nodes)
    pca_data = pca_op.fit_transform(sig_input_values) # Doesn't enable for fit transform
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('PCA')
    datasets.append('Significantly affected')

    # Run on each VAE
    start = timeit.default_timer()
    deep_vae_data, d_vae = get_deep_vae(sig_input_values, num_nodes, r_seed)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('Deep VAE')
    datasets.append('Significantly affected')

    start = timeit.default_timer()
    shallow_vae_data, s_vae = get_shallow_vae(sig_input_values, num_nodes, r_seed)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('Shallow VAE')
    datasets.append('Significantly affected')

    print("starting TSNE")
    # tSNE
    start = timeit.default_timer()
    if num_nodes == 3:
        tsne_op = TSNE(n_components=num_nodes, random_state=r_seed)

    else:
        #Here we had to comment out this for n = 6 sig. print("Skipping tSNE...")
        tsne_op = TSNE(n_components=num_nodes, random_state=r_seed, method='exact')

    tsne_data = tsne_op.fit_transform(sig_input_values)
    stop = timeit.default_timer()
    times.append(stop - start)
    nodes.append(num_nodes)
    tools.append('tSNE')
    datasets.append('Significantly affected')
    print("finished tSNE")
    print(stop - start)
    # Save to csv file
    sig_df = pd.DataFrame()
    sig_df['external_gene_name'] = sig_gene_names
    for i in range(0, num_nodes):
        sig_df[f'VAE_deep_{i}'] = deep_vae_data[:, i]
        sig_df[f'VAE_lin_{i}'] = shallow_vae_data[:, i]
        sig_df[f'PCA_{i}'] = pca_data[:, i]
        sig_df[f'UMAP_{i}'] = umap_data[:, i]
        sig_df[f'PHATE_{i}'] = phate_data[:, i]
        sig_df[f'tSNE_{i}'] = tsne_data[:, i]

    # Save to csv for later
    sig_df.to_csv(f'{output_dir}sig_{num_nodes}_{r_seed}.csv', index=False)

    # Save the timing also to a CSV
    time_df = pd.DataFrame()
    time_df['Tools'] = tools
    time_df['Runtime'] = times
    time_df['Dataset'] = datasets
    time_df['Nodes'] = nodes
    time_df.to_csv(f'{output_dir}runtime_{num_nodes}_{r_seed}.csv', index=False)

    print(f'Done sig {num_nodes} {r_seed}')


def run_pool():
    # Seeds were generated using random, have saved them here for reproducibility sake
    rand_seeds = [43, 41, 66, 52, 44, 76, 49, 82, 38, 32, 90, 13, 93, 53, 14, 78, 94, 35, 45, 72]
    pool = ThreadPool(len(rand_seeds))
    params = []
    for seed in rand_seeds:
        params.append([seed, 3]) # Run the same seed on 3 nodes and 6 nodes
        params.append([seed, 6])
    results = pool.map(run_compare, params)
    print('Done')

run_pool()
