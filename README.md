# Parallel machine scheduling problem with a common server

This set of instances was generated using the method described by Kim and Lee (2012, doi: https://doi.org/10.1016/j.cor.2011.12.011).

In particular, the instances are randomly generated using the combination of four parameters ( $n, m, \alpha, \rho$ ), 
where $n$ is the number of jobs, $m$ is the number of machines, $\alpha$ is the diversity factor for the range of setup ( $s_j$ ) and processing ( $p_j$ )
times, and parameter $\rho$ is the setup time severity factor. Please [click here](https://doi.org/10.1016/j.cor.2011.12.011) for a detailed explanation
about the instance generation procedure.

## Folders

The instance files are divided into folders according to the number of jobs.

## Files

The instances were generated using a combination of the values $\alpha = [0.1, 0.3, 0.5]$ and $\rho = [0.5, 0.7, 1.0]$.

In the files, these values are also identified by an id, for example, values $\alpha = 0.1$, $\alpha=0.3$, 
and $\alpha=0.5$ has $\alpha$ ids 1, 2, and 3, respectivelly. The same is true for the values of $\rho$.

### File name 

The file names follow the pattern: [*nº of jobs*] n [*nº of machines*] m [ $\alpha$ *id*] a.txt
> Example: The 10n2m2a.txt file contains instances with 10 jobs and 2 machines generated with parameter $\alpha=0.5$.


### File structure

Each file contains five instances for each combination of $\alpha$ and $\rho$ values.
* The instance is identified by *Ins: [instance id]*.
* Setup times of each value of $\rho$ are identified by *level [* $\rho$ *id]*.

The files have the following structure:
```
n
m
alpha value
 
Ins: [instance id]

p_1 p_2 p_3 ... p_n

level 1: s_1 s_2 s_3 ... s_n
level 2: s_1 s_2 s_3 ... s_n
level 3: s_1 s_2 s_3 ... s_n

...
```
> Example: Instance number 4 with 10 jobs, 2 machines, $\alpha = 0.3$, and $\rho=1.0$ can be found in the 10n2m2a.txt. 
>> The processing and setup (level 3) times are just below the line *Ins: 4*. 
