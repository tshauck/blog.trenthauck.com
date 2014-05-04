title: Bibliography
summary: Papers and books of note.
slug: bibliography

#A Biterm Topic Model for Short Texts

* [Paper][biterm]
* NLP, Topic Models

This papers attempts to deal with the sparsity issue of other topic models such
as [LDA][lda_wiki]. It does this my modeling the likelihood of topics for given
biterms then uses the conditional probability of those biterms in the document
to determine the conditional probability of the topic given the document.

It ends up looking something like:

$$\color{black}{P(z|d) = \sum_d P(z|b)P(b|d)}$$


[biterm]: http://www2013.wwwconference.org/proceedings/p1445.pdf
[lda_wiki]: http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation
