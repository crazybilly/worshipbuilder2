---
title: "Worship"
output:
  slidy_presentation:
    css: /media/storage/worship-frontend/www/slide-style.css
---
  

```{r, include=FALSE}
knitr::opts_knit$set(root.dir = '../../') 
```

   
```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = FALSE, results = 'asis')
source('utils/01-functions.R')


{% block %}

{{ the_rmd }}

{% endblock %}



## Communion

For I received from the Lord what I also passed on to you:<br><br>
The Lord Jesus, on the night he was betrayed, took bread, and when he had given thanks, he broke it and said, “This is my body, which is for you; do this in remembrance of me.”<br><br>
In the same way, after supper he took the cup, saying, “This cup is the new covenant in my blood; do this, whenever you drink it, in remembrance of me.”<br><br>
For whenever you eat this bread and drink this cup, you proclaim the Lord’s death until he comes.


```{r eval=FALSE, message=FALSE, warning=FALSE, include=FALSE}
   # the lectionary link below gets str_replaced in 01-functions/make_worship_rmd()
```
## Talking Time
Talking Time

[lectionary](https://lectionary.library.vanderbilt.edu/texts/?y=384&z=s&d=51)
