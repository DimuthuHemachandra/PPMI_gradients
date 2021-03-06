import pandas as pd
import os
import glob
import io 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

sns.set()

def make_out_dir(out_path):

	#Make subdirectories to save files
	filename = out_path
	if not os.path.exists(os.path.dirname(filename)):
	    try:
	        os.makedirs(os.path.dirname(filename))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	          raise

def remove_outliers(df):
	z_scores = zscore(df)

	abs_z_scores = np.abs(z_scores)
	filtered_entries = (abs_z_scores < 2).all(axis=1)
	new_df = df[filtered_entries]

	return new_df

from scipy import stats

def drop_numerical_outliers(df, z_thresh=2):
    # Constrains will contain `True` or `False` depending on if it is a value below the threshold.
    constrains = df.select_dtypes(include=[np.number]) \
        .apply(lambda x: np.abs(stats.zscore(x)) < z_thresh, result_type='reduce') \
        .all(axis=1)
    # Drop (inplace) values set to be rejected
    df.drop(df.index[~constrains], inplace=True)

#make_out_dir(snakemake.params.stat_out_path)

#hcp_dir = snakemake.input.hcp_path
grad_12_dir = snakemake.input.grad_12_csv_path
grad_24_dir = snakemake.input.grad_24_csv_path
subj = snakemake.params.subj
out_path = snakemake.params.out_path



#myelin_lh = pd.read_csv("test_materials/hcp_360/sub-CT01/CT01_mean_myelin_R.txt", names = ['myelin'])

#print(myelin_lh)


#subj = ['3118','3119','3120']
m12_L= []
m24_L= []

m12_R= []
m24_R= []

#grad_12_dir='/home/dimuthu1/scratch/PPMI_project2/derivatives/analysis/cortex/aligned_gradients/month12'
#grad_24_dir='/home/dimuthu1/scratch/PPMI_project2/derivatives/analysis/cortex/aligned_gradients/month24'
#out_path='/home/dimuthu1/scratch/PPMI_project2/derivatives/analysis/cortex'


for subjects in subj:

	
	grads12 = pd.read_csv(grad_12_dir+"/sub-"+subjects+"_L_gradients.csv")
	gradient12_lh = grads12[['ctx_L_grad_1','ctx_L_grad_2','ctx_L_grad_3']]
	gradient12_rh = grads12[['ctx_R_grad_1','ctx_R_grad_2','ctx_R_grad_3']]
	gradient12_lh = gradient12_lh.drop([0]).reset_index(drop=True)
	gradient12_rh = gradient12_rh.drop([0]).reset_index(drop=True)
	
	
	#gradient_lh = remove_outliers(gradient_lh)
	m12_L.append(gradient12_lh)
	gradient12_lh['month'] = 'm12'

	m12_R.append(gradient12_rh)
	gradient12_rh['month'] = 'm12'
	
	grads24 = pd.read_csv(grad_24_dir+"/sub-"+subjects+"_L_gradients.csv")
	gradient24_lh = grads24[['ctx_L_grad_1','ctx_L_grad_2','ctx_L_grad_3']]
	gradient24_rh = grads24[['ctx_R_grad_1','ctx_R_grad_2','ctx_R_grad_3']]
	gradient24_lh = gradient24_lh.drop([0]).reset_index(drop=True)
	gradient24_rh = gradient24_rh.drop([0]).reset_index(drop=True)
	
	#gradient_lh = remove_outliers(gradient_lh)
	m24_L.append(gradient24_lh)
	gradient24_lh['month'] = 'm24'

	m24_R.append(gradient24_rh)
	gradient24_rh['month'] = 'm24'
	
	df_subj = gradient24_lh.append(gradient12_lh)
	sns_plot = sns.scatterplot(data = df_subj, x='ctx_L_grad_1',y='ctx_L_grad_2', hue="month")
	plt.savefig(out_path+"/group_"+subjects+"_stat_L_ctx.png")
	plt.close()

	df_subj = gradient24_rh.append(gradient12_rh)
	sns_plot = sns.scatterplot(data = df_subj, x='ctx_R_grad_1',y='ctx_R_grad_2', hue="month")
	plt.savefig(out_path+"/group_"+subjects+"_stat_R_ctx.png")
	plt.close()



df_12_L = pd.concat(m12_L)
#df_12_L = remove_outliers(df_12_L)
df_12_L['month'] = 'm12'
df_24_L = pd.concat(m24_L)
#df_24_L = remove_outliers(df_24_L)
df_24_L['month'] = 'm24'
print(df_12_L)
df_all_L = df_24_L.append(df_12_L)
print(df_all_L)
df_all_L.to_csv(out_path+'/all_stat_L_ctx.csv', index=False)



df_12_R = pd.concat(m12_R)
#df_12_L = remove_outliers(df_12_L)
df_12_R['month'] = 'm12'
df_24_R = pd.concat(m24_R)
#df_24_L = remove_outliers(df_24_L)
df_24_R['month'] = 'm24'
print(df_12_R)
df_all_R = df_24_R.append(df_12_R)
print(df_all_R)
df_all_R.to_csv(out_path+'/all_stat_R_ctx.csv', index=False)


#print(df_R)
#sns.color_palette("viridis", as_cmap=True)
sns_plot_L = sns.pairplot(df_all_L,plot_kws={"s": 5}, hue="month")
#sns_plot_R = sns.pairplot(df_R, plot_kws={"s": 8}, hue="group")
#plt.show()
sns_plot_L.savefig(out_path+"/group_stat_L_ctx.png")
#sns_plot_R.savefig(out_path+"/group_stat_R.png")
#plt.show()


#sns.color_palette("viridis", as_cmap=True)
sns_plot_R = sns.pairplot(df_all_R,plot_kws={"s": 5}, hue="month")
#sns_plot_R = sns.pairplot(df_R, plot_kws={"s": 8}, hue="group")
#plt.show()
sns_plot_R.savefig(out_path+"/group_stat_R_ctx.png")
#sns_plot_R.savefig(out_path+"/group_stat_R.png")
#plt.show()


"""
plt.clf()

#sns.color_palette("viridis", as_cmap=True)
ct_df = df_L.loc[df_L['group'] == 'CT']
ct_df = ct_df.drop(['group'], axis = 1)
sns_plot_ct = sns.heatmap(ct_df.corr(), annot=True)
sns_plot_ct.figure.savefig(out_path+"/ct_L_heatmap.png")

plt.clf()


PD_df = df_L.loc[df_L['group'] == 'PD']
PD_df = PD_df.drop(['group'], axis = 1)
sns_plot_PD = sns.heatmap(PD_df.corr(), annot=True)
sns_plot_PD.figure.savefig(out_path+"/PD_L_heatmap.png")
"""










