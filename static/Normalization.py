import pandas as pd 
import numpy as np
#defind a normalization function
def mean_normalization(x):
    """
    This script is to do mean normalization for DataFrame
    
    Parameter:
        x: format: DataFrame
        rows:feature 
        columns:samples
    
    Returns:
        output:DataFrame; after mean normalization.
        rows:feature 
        columns:samples
    """
    for i in range(x.shape[1]):
        x_i = x.iloc[:,i]
        Whole_mean = sum(x_i)/len(x_i)
        new_i = [ij/Whole_mean for ij in x_i]
        x.iloc[:,i] = new_i
    return (x)

def quantilenormalize(df_input):
    """
    This script is to do quantile normalization for DataFrame.
    
    Parameter:
        x: format: DataFrame
        rows:feature 
        columns:samples
    
    Returns:
        output:DataFrame; after quantile normalization.
        rows:feature 
        columns:samples
    """
    df = df_input.copy()
    dic = {}
    for col in df:
        dic.update({col : sorted(df[col])})
    sorted_df = pd.DataFrame(dic)
    rank = sorted_df.mean(axis = 1).tolist()
    #sort
    for col in df:
        t = np.searchsorted(np.sort(df[col]), df[col])
        df[col] = [rank[i] for i in t]
    return (df)

if __name__ == '__main__':
    input_name = "/Users/yujijun/Documents/01-Work/02-HiglassProject/02-Higlass/03-Output/12072019/bigwig_filter_0.6.tsv"
    pd_input = pd.read_csv(input_name, sep='\t', index_col=None, header=0)
    pd_input = pd_input.fillna(0)
    print("Input matrix:", pd_input.shape)
    pd_value = pd_input.iloc[:,3:]
    print("pd value matrix:", pd_value.shape)
    
    pd_value_mean = mean_normalization(pd_value)
    pd_value_quan = quantilenormalize(pd_value)
    
    pd_output_mean = pd.concat([pd_input.iloc[:,0:3],pd_value_mean], axis=1)
    pd_output_quan = pd.concat([pd_input.iloc[:,0:3],pd_value_quan],axis=1)
    
    #Output
    output_path = '/Users/yujijun/Documents/01-Work/02-HiglassProject/02-Higlass/03-Output/12072019/'
    pd_output_mean.to_csv('%s/bigwig_filter_0.6_mean.tsv' %output_path, sep='\t', index=False, header=True)
    pd_output_quan.to_csv('%s/bigwig_filter_0.6_quan.tsv' %output_path, sep='\t', index=False, header=True)
    print("This is the end!")