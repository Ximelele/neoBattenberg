# Battenberg

This repository contains code modified version for the whole genome sequencing subclonal copy number caller Battenberg,
as described in [Nik-Zainal, Van Loo, Wedge, et al. (2012), Cell](https://www.ncbi.nlm.nih.gov/pubmed/22608083).

## Installation instructions

### Docker instalation

```
docker pull ximardo/rbatt:v3.1
docker run --name Battenberg -v /your/desired/volume:/data ximardo/rbatt:v3.1
docker start Battenberg
docker exec -it Battenberg bash
```

### Manual installation instructions

Installing from Github requires devtools and Battenberg requires the modified copynumber package from "
igordot/copynumber" and readr, gtools, splines, ggplot2, gridExtra, RColorBrewer, GenomicRanges and ASCAT. The pipeline
requires parallel and doParallel. Thi is only needed when you dont want to use Docker version.

```
R -q -e 'BiocManager::install(c("devtools", "splines", "readr", "doParallel", "ggplot2", "RColorBrewer", "gridExtra", "gtools", "parallel", "igordot/copynumber", "GenomicRanges"))'
R -q -e 'devtools::install_github("VanLoo-lab/ascat/ASCAT")'
R -q -e 'devtools::install_github("Wedge-Oxford/battenberg")'
```

#### Required reference files

`GRCh37` reference files may downloaded from
here: https://ora.ox.ac.uk/objects/uuid:2c1fec09-a504-49ab-9ce9-3f17bac531bc

The bundle contains the following files:

* battenberg_1000genomesloci2012_v3.tar.gz
* battenberg_impute_1000G_v3.tar.gz
* probloci_270415.txt.gz
* battenberg_wgs_gc_correction_1000g_v3.tar.gz
* battenberg_wgs_replic_correction_1000g_v3.tar.gz
* battenberg_snp6_exe.tgz (SNP6 only)
* battenberg_snp6_ref.tgz (SNP6 only)

`GRCh38` reference files may be downloaded from
here: https://ora.ox.ac.uk/objects/uuid:08e24957-7e76-438a-bd38-66c48008cf52

The bundle contains the following files:

* 1000G_loci_hg38.zip
* imputation.zip
* beagle5.zip
* probloci.zip
* GC_correction_hg38.zip
* RT_correction_hg38.zip
* README.txt

## Description of the output

### Output structure

```
[tumourname]/
├── Alle_counts/
│   ├── [normalname]_alleleFrequencies_*.txt
│   ├── [tumourname]_alleleFrequencies_*.txt
│   └── [tumourname]_alleleCounts.tab 
│
├── Impute/
│   ├── [tumourname]_beagle5_input_*.txt
│   ├── [tumourname]_beagle5_output_*.txt.vcf.gz
│   ├── [tumourname]_impute_output_*_allHaplotypeInfo.txt
│   ├── [tumourname]_heterozygousMutBAFs_haplotyped.txt
│   ├── [tumourname]_*_heterozygousMutBAFs_haplotyped.txt
│   └── [tumourname]_beagle5_output_*.txt.log 
│
├── Plots/
│   ├── [tumourname]_*_heterozygousData.png
│   ├── [tumourname]_RAFseg_*.png
│   ├── [tumourname]_segment_*.png
│   ├── [tumourname]_nonroundedprofile.png 
│   ├── [tumourname]_distance.png 
│   ├── [tumourname]_copynumberprofile.png
│   ├── [tumourname]_second_copynumberprofile.png
│   ├── [tumourname]_second_distance.png
│   └── [tumourname]_second_nonroundedprofile.png 
│ 
├── [tumourname]_copynumber.txt
└── [tumourname]_rho_and_psi.txt
```

### Key output files

* `[samplename]__copynumber.txt` contains the copy number data (see table below)
* `[samplename]_rho_and_psi.txt` contains the purity estimate (make sure to use the FRAC_genome, rho field in the second
  row, first column)
* `[samplename]_BattenbergProfile*png` shows the profile (the two variants show subclonal copy number in a different
  way)
* `[samplename]_subclones_chr*.png` show detailed figures of the copy number calls per chromosome
* `[samplename]_distance.png` This shows the purity and ploidy solution space and can be used to pick alternative
  solutions

The copy number profile saved in the `[samplename]_subclones.txt` is a tab delimited file in text format. Within this
file there is a line for each segment in the tumour genome.
Each segment will have either one or two copy number states:

* If there is one state that line represents the clonal copy number (i.e. all tumour cells have this state)
* If there are two states that line represents subclonal copy number (i.e. there are two populations of cells, each with
  a different state)

A copy number state consists of a major and a minor allele and their frequencies, which together add give the total copy
number for that segment and an estimate fraction of tumour cells that carry each allele.

The following columns are available in the Battenberg output:

| Column        | Description                                                                                                                                                                   |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| chr           | The chromosome of the segment                                                                                                                                                 |
| startpos      | Start position on the chromosome                                                                                                                                              |
| endpos        | End position on the chromosome                                                                                                                                                |
| BAF           | The B-allele frequency of the segment                                                                                                                                         |
| pval          | P-value that is obtained when testing whether this segment should be represented by one or two states. A low p-value will result in the fitting of a second copy number state |
| LogR          | The log ratio of normalised tumour coverage versus its matched normal sequencing sample                                                                                       |
| ntot          | An internal total copy number value used to determine the priority of solutions. NOTE: This is not the total copy number of this segment!                                     |
| nMaj1_A       | The major allele copy number of state 1 from solution A                                                                                                                       |
| nMin1_A       | The minor allele copy number of state 1 from solution A                                                                                                                       |
| frac1_A       | Fraction of tumour cells carrying state 1 in solution A                                                                                                                       |
| nMaj2_A       | The major allele copy number of state 2 from solution A. This value can be NA                                                                                                 |
| nMin2_A       | The minor allele copy number of state 2 from solution A. This value can be NA                                                                                                 |
| frac2_A       | Fraction of tumour cells carrying state 2 in solution A. This value can be NA                                                                                                 |
| SDfrac_A      | Standard deviation on the BAF of SNPs in this segment, can be used as a measure of uncertainty                                                                                |
| SDfrac_A_BS   | Bootstrapped standard deviation                                                                                                                                               |
| frac1_A_0.025 | Associated 95% confidence interval of the bootstrap measure of uncertainty                                                                                                    |

Followed by possible equivalent solutions B to F with the same columns as defined above for solution A (due to the way a
profile is fit Battenberg can generate a series of equivalent solutions that are reported separately in the output).

### Plots for QC

It also produces a number plots that show the raw data and are useful for QC (and their raw data files denoted by *.tab)

* `[samplename].tumour.png` and `[samplename].germline.png` show the raw BAF and logR
* `[samplename]_coverage.png` contains coverage divided by the mean coverage of both tumour and normal
* `[samplename]_alleleratio.png` shows BAF*logR, a rough approximation of what the data looks like shortly before copy
  number calling

### Intermediate figures

Finally, a range of plots show intermediate steps and can occasionally be useful

* `[samplename]_chr*_heterozygousData.png` shows reconstructed haplotype blocks in the characteristic Battenberg cake
  pattern
* `[samplename]_RAFseg_chr*.png` and `[samplename]_segment_chr*.png` contains segmentation data for step 1 and step 2
  respectively
* `[samplename]_nonroundedprofile.png` shows the copy number profile without rounding to integers
* `[samplename]_copynumberprofile.png` shows the copy number profile with (including subclonal copy number) rounding to
  integers

```