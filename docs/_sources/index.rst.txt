*******************************************************************************************************************************
Variational autoencoding of gene landscapes during mouse CNS development uncovers layered roles of Polycomb Repressor Complex 2
*******************************************************************************************************************************

Information
===========
This site hosts the information associated with the paper: **Deep Learning Decodes Multi-layered Roles of Polycomb Repressor Complex 2 During Mouse CNS Development**.
Here we provide the code and data used for all the analyses in the paper and link to the packages we developed as part of
producing the paper.

Links to analyses and data
--------------------------

- Preprint: `bioRxiv <https://doi.org/10.1101/2021.06.22.449386>`_
- HTML outputs are available on the left panel
- Code and processed data is available at: `mouseCNS_vae <https://github.com/ArianeMora/mouseCNS_vae>`_
- Raw RNA-seq files are available at the NCBI/Gene Expression Omnibus under the accession GSE123331

Links to developed packages and tutorials
-----------------------------------------
- Reproducible Variational autoencoder: `scivae <https://arianemora.github.io/scivae/>`_
- Epigenetic annotation to genes in python `scie2g <https://arianemora.github.io/sciepi2gene/>`_
- Biomart python wrapper `scibiomart <https://arianemora.github.io/scibiomart/>`_
- Visualisation library for chart formatting `sciviso <https://github.com/ArianeMora/sciviso/>`_

Updates since review
--------------------
We've just been through our first round of revisions (November 2021), and we have updated several things:

1) We created an `interactive website <http://bioinf.scmb.uq.edu.au:81/cnsvae/static/>`_ where you can interact with the data.
2) Made the `data easier to download <https://github.com/ArianeMora/mouseCNS_vae/blob/main/data/results/3_node_consistent_genes/vae/DF_Visualisation_VAE.csv>`_ without having to run anything.
3) Added all **marked anterior** genes (121) to the analysis where we test for conservation of tissue specificity between mouse and humans
4) Added a comparison to identify if there are more blood vessel staining under *Eed-cKO*.
5) The manuscript also has some nice updates where we put everything in context a bit better and highlighted the novelty :)


Places where this (or a package we developed for this) has been presented
-------------------------------------------------------------------------

.. list-table::
   :widths: 15 30 15
   :header-rows: 1

   * - Date
     - Conference
     - Type
   * - 28 April 2021
     - Melbourne bioinformatics seminar series
     - Presentation
   * - 25 May 2021
     - `ISDN International Society for Developmental Neuroscience <http://www.isdn-conference.elsevier.com/>`_
     - Poster
   * - 25 July 2021
     - `ISDN International Society for Developmental Neuroscience <http://www.isdn-conference.elsevier.com/>`_
     - Poster
   * - 10 November 2021
     - `EMBL EAPS EMBL Australia Postgraduate Symposium <https://www.emblaustralia.org/student-opportunities/embl-australia-postgraduate-symposium>`_
     - Lightning talk
   * - 18 November 2021
     - `OAMLS/ACML The 13th Asian Conference on Machine Learning <http://www.acml-conf.org/2021/>`_
     - Poster
   * - 19 November 2021
     - `SCMB School of Chemistry and Molecular Biosciences symposium <https://scmb.uq.edu.au/event/2548/scmb-research-students-symposium>`_
     - Presentation
   * - 22 November 2021
     - `ABACBS Australian Bioinformatics And Computational Biology Society <https://www.abacbs.org/conference2021>`_
     - Lightning talk

Authors
=======

Ariane Mora1, Jonathan Rakar3, Ignacio Monedero Cobeta3*, Behzad Yaghmaeian Salmani3#, Annika Starkenberg3, Stefan Thor2,3$, Mikael Bodén1

1) School of Chemistry and Molecular Biosciences
2), and School of Biomedical Sciences, University of Queensland, St Lucia QLD 4072, Australia.
3) Department of Clinical and Experimental Medicine, Linkoping University, SE-58185, Linkoping, Sweden.

Current addresses: #) Department of Cell and Molecular Biology, Karolinska Institute, SE-171 65, Stockholm, Sweden.
*Department of Physiology, Universidad Autonoma de Madrid, Madrid, Spain.
$) School of Biomedical Sciences, University of Queensland, St Lucia QLD 4072, Australia

Abstract
========
A prominent aspect of most, if not all, central nervous systems (CNSs) is that anterior regions (brain) are
larger than posterior ones (spinal cord). Studies in Drosophila and mouse have revealed that the Polycomb Repressor Complex 2 (PRC2)
acts by several mechanisms to promote anterior CNS expansion. However, it is unclear if PRC2 acts directly and/or indirectly
upon key downstream genes, what the full spectrum of PRC2 action is during embryonic CNS development and how PRC2 integrates
with the epigenetic landscape. We removed PRC2 function from the developing mouse CNS, by mutating the key gene Eed, and
generated spatio-temporal transcriptomic data. We developed a bioinformatics workflow that incorporates standard
statistical analyses with machine learning to integrate the transcriptomic response to PRC2 inactivation with epigenetic
information from ENCODE. This multi-variate analysis corroborates the central involvement of PRC2 in anterior CNS expansion,
and reveals layered regulation via PRC2. These findings uncover a differential logic for the role of PRC2 upon functionally
distinct gene categories that drive CNS anterior expansion. To support the analysis of emerging multi-modal datasets,
we provide a novel bioinformatics package that can disentangle regulatory underpinnings of heterogeneous biological processes.
Code for our scivae package is available at `sci-vae <https://github.com/ArianeMora/scivae>`_.


.. figure:: _static/ISDN_poster_AM.png
   :width: 800
   :align: center


Getting in touch
=================

Please contact ST (s.thor@uq.edu.au), MB (m.boden@uq.edu.au), and AM (a.mora@uq.edu.au)


Citing the preprint
===================
Link to preprint


.. toctree::
   :caption: Package info
   :maxdepth: 1

   about
   installing/index


.. toctree::
   :caption: Reproducibility
   :maxdepth: 1

   examples/apAxis_datasetGeneration
   examples/apAxis_between-cond-time
   examples/apAxis_between-cond-tissue
   examples/apAxis_between-time
   examples/apAxis_between-tissue

   examples/consistently_affected_3_nodes
   examples/comparison


.. toctree::
   :caption: About
   :maxdepth: 1

   faq
   changelog
   references
