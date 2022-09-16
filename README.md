[1.2]: http://i.imgur.com/wWzX9uB.png
[1]: http://www.twitter.com/AswendtMarkus
<!--social icon from https://github.com/carlsednaoui/gitsocial -->
<img align="right" src="https://github.com/maswendt/AIDAhisto/blob/master/logo.png"><h1>AIDA<i>histo</i></h1>***Atlas-based imaging data analysis tool for quantitative mouse brain histology***
<p align="justify"> Software to automatically <b>detect cells</b> in histological <b>mouse brain</b> and <b>spinal cord</b> sections. Tested for different immunostainings (e.g., GFAP, Iba1, and MAP2) and histological stainings (e.g., Nissl). The Allen Mouse Brain/Spinal Cord Atlas is used to register the microscopy files. Cell counting results are reported as cells per brain region.</p>
<img align="center" src="https://github.com/maswendt/AIDAhisto/blob/master/AIDAhisto_Overview.png">

Information about [Version 1.2](https://github.com/maswendt/AIDAhisto/releases/tag/v1.2) / [Version 1.1](https://github.com/maswendt/AIDAhisto/releases/tag/v1.1) / [Version 1.0](https://github.com/maswendt/AIDAhisto/releases/tag/v1.0)</b>

<h3><b>FEATURES</h3></b>

- Includes a custom version of the Allen Mouse Brain/Spinal Cord Atlas with a list of annotations

- Instruction on how to register the atlas with microscopy files using ImageJ

- Automated cell counting implemented in Matlab (preferred) and Python

- Cell counting works for immunostainings and histological stainings; the cell nuclei position (e.g. based on a DAPI staining) can be used to improve the cell counting (only cells with a cell nuclei will be counted)

<h3><b>GET STARTED</h3></b>

Download the modified atlas files and the test images (including representative results) [here](https://doi.org/10.12751/g-node.25jp6z). For details on installation and use, see the step-by-step guide in the [Manual v1.2](https://github.com/maswendt/AIDAhisto/AIDAhisto_Manual.pdf) 


<h3><b>CITATION</h3></b>

When applying or modifying AIDAhisto, please always cite the original reference: [Pallast, N., et al. "Atlas-based imaging data analysis tool for quantitative mouse brain histology (AIDAhisto)" Journal of Neuroscience Methods, 2019](https://www.sciencedirect.com/science/article/pii/S0165027019302511?via%3Dihub)

<h3><b>CONTACT</h3></b>

Markus Aswendt (markus.aswendt@uk-koeln.de)[![alt text][1.2]][1]

Need help? Chat with us and find FAQs in the AIDA_Tools Gitter room: [![Gitter](https://badges.gitter.im/AIDA_tools/community.svg)](https://gitter.im/AIDA_tools/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
___
LICENSE
CC BY-NC-SA 4.0
<details>
<summary>REFERENCES</summary></b>

+ Allen Institute for Brain Science (2004). Allen Mouse Brain Atlas and Allen Mouse Spinal Cord Atlas. Available from mouse.brain-map.org. Allen Institute for Brain Science (2011). Source: [Allen Mouse Brain Atlas](https://mouse.brain-map.org/static/atlas), [Allen Mouse Spinal Cord Atlas](https://mousespinal.brain-map.org)
+ Allen Brain Reference Atlas: [Lein, E.S. et al. (2007). Genome-wide atlas of gene expression in the adult mouse brain, Nature 445: 168-176. ](https://doi:10.1038/nature05453), [Harris, J. A. et al. (2019). Hierarchical organization of cortical and thalamic connectivity. Nature 575, 195-202](https://doi:10.1038/s41586-019-1716-z), [Oh, Seung Wook, et al. "A mesoscale connectome of the mouse brain." Nature, 2014](https://www.nature.com/articles/nature13186)
+ AIDA<i>histo [Pallast, N., et al. "Atlas-based imaging data analysis tool for quantitative mouse brain histology (AIDAhisto)" Journal of Neuroscience Methods, 2019](https://www.sciencedirect.com/science/article/pii/S0165027019302511?via%3Dihub)
+ AIDA<i>mri [Pallast, N., et al. "Processing pipeline for Atlas-based Imaging Data Analysis (AIDA) of structural and functional mouse brain MRI" Frontiers in Neuroinformatics, 2019](https://www.frontiersin.org/articles/10.3389/fninf.2019.00042/full)
+ Incremental cell search [Meruvia-Pastor, Oscar E., et al. "Estimating cell count and distribution in labeled histological samples using incremental cell search" Journal of Biomedical Imaging, 2011](https://www.hindawi.com/journals/ijbi/2011/874702/)
