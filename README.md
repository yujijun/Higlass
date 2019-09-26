# Higlass
This is a repository for higlass analysis 

Cistrome DB data visualization flow：
1. To do QC locally
2. Gather bigwig data in iris(ssh -p 33001 jjyu@cistrome.org) server (optional)
3. Transfer bigwig data and summit from iris server to kraken(jjyu@kraken.dfci.harvard.edu)
4. Extract the chr22 data and conver them to bedfile with different resolution in kraken 
5. Extrate the chr peak position information and generate peak postion matrix in kraken 
6. Cluster all samples by peak position matrix and visulation in kraken or locally
7. Select sample by cluster visulization result and generate 
8.1 Generate whole genomes bedfile with the specific resolution
8.2 Cluster selected samples again by peak_pos_chr22.csv and generate seleted sample name file with clustered order(Visulation)
9. Sort samples order by new cluster labels in whole genomes bedfile (8.1)
10. Transmit file from kraken to local folder(higlass-tmp)
11. Generate mv5 data by higlass docker locally 
11.1 open docker 
11.2 conda activate higlassv2
11.3 higlass-manage start --version v0.6.17
11.4 clodius convert bedfile-to-multivec bedfile_16_20.csv --chromsizes-filename chromInfo.txt.allchr --starting-resolution 16 --num-rows 20 --row-infos-filename cluster_sample_name_20.txt 
12. Visulization 
12.1 open docker 
12.2 conda activate higlass
12.3 higlass-manage start --version v0.6.17
12.4 higlass-manage view --tracktype horizontal-multivec --datatype multivec --filetype multivec --position center --assembly hg38 --chromsizes-filename chromInfo.txt.allchr bedfile_200_sort.multires.mv5
